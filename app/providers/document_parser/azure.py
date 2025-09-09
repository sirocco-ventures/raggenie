from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentContentFormat
from loguru import logger
import fitz  # PyMuPDF
import io, os
from pathlib import Path
from app.providers.config import configs
from urllib.parse import quote

class AzureParser:
    def __init__(self, endpoint=configs.azure_di_enpoint, key=configs.azure_di_secret_key, static_root="static/doc-images", dpi=300):
        self.endpoint = endpoint
        self.key = key
        self.static_root = static_root
        self.dpi = dpi
        os.makedirs(self.static_root, exist_ok=True)

    def document_ocr(self, path):
        """
        Returns a list with one item:
        {
          "content": [markdown_chunk1, markdown_chunk2, ...],
          "images": [ {page, url, file, caption}, ... ],
          "metadata": {"path": path}
        }
        """
        metadata = {"path": path}
        doc = fitz.open(path)
        num_pages = doc.page_count
        output = {"content": [], "images": [], "metadata": metadata}
        pdf_stem = Path(path).stem

        for i in range(0, num_pages, 2):
            start_page = i        # zero-based
            end_page = min(i + 2, num_pages)  # non-inclusive upper bound

            # Build a 1–2 page in-memory PDF for DI
            sub = fitz.open()
            sub.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)
            pdf_bytes = sub.write()
            sub.close()

            logger.info(f"Analyzing pages {start_page+1}-{end_page}")
            client = DocumentIntelligenceClient(self.endpoint, AzureKeyCredential(self.key))

            poller_md = client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=io.BytesIO(pdf_bytes),
                content_type="application/pdf",
                output_content_format=DocumentContentFormat.MARKDOWN
            )
            result_md = poller_md.result()

            # Save the markdown chunk
            output["content"].append(result_md.content)

            # Extract & save figures
            print(result_md.figures)
            images = self._save_figures_from_result(
                result_obj=result_md,
                original_pdf=doc,
                pdf_stem=pdf_stem,
                batch_start_page=start_page
            )
            output["images"].extend(images)

        return [output]

    # ---------- helpers ----------

    def _save_figures_from_result(self, result_obj, original_pdf, pdf_stem, batch_start_page):
        """
        Convert DI figure polygons to cropped PNGs using PyMuPDF.
        Unit-agnostic: normalizes against DI page width/height, then scales to PDF points.
        """
        saved = []
        if not result_obj or not getattr(result_obj, "figures", None):
            return saved

        di_pages = result_obj.pages or []

        for fig_idx, fig in enumerate(result_obj.figures):
            # skip rga logo
            spans = fig.spans
            length = spans[0].length
            if length == 86:
                continue
            # Caption, if any
            caption = getattr(fig, "caption", None)
            caption_text = getattr(caption, "content", None) if caption else None

            for region_idx, region in enumerate(fig.bounding_regions or []):
                local_page_idx = region.page_number - 1  # zero-based within the batch
                global_page_idx = batch_start_page + local_page_idx

                if local_page_idx < 0 or local_page_idx >= len(di_pages):
                    logger.warning(f"DI page index out of range: {local_page_idx}")
                    continue

                di_page = di_pages[local_page_idx]
                di_w, di_h = float(di_page.width), float(di_page.height)

                pdf_page = original_pdf[global_page_idx]
                pdf_w, pdf_h = pdf_page.rect.width, pdf_page.rect.height  # points

                # Polygon is [x1,y1, x2,y2, ...]
                poly = list(region.polygon or [])

                xs, ys = poly[0::2], poly[1::2]
                if not xs or not ys:
                    continue

                # Normalize to [0..1] against DI page size (unit-agnostic)
                nx0, nx1 = max(0.0, min(xs)/di_w), min(1.0, max(xs)/di_w)
                ny0, ny1 = max(0.0, min(ys)/di_h), min(1.0, max(ys)/di_h)

                # Scale to PDF points
                x0 = nx0 * pdf_w
                y0 = ny0 * pdf_h
                x1 = nx1 * pdf_w
                y1 = ny1 * pdf_h

                # Pad + clamp (avoid chopped edges)
                pad = 4  # points (~0.055 in)
                rect = fitz.Rect(
                    max(0, x0 - pad),
                    max(0, y0 - pad),
                    min(pdf_w, x1 + pad),
                    min(pdf_h, y1 + pad),
                )

                # Render at target DPI
                mat = fitz.Matrix(self.dpi / 72.0, self.dpi / 72.0)
                pix = pdf_page.get_pixmap(matrix=mat, clip=rect, alpha=False)

                # Deterministic filename
                fname = f"{pdf_stem}_p{global_page_idx+1}_f{fig_idx+1}_{region_idx+1}.png"
                fpath = os.path.join(self.static_root, fname)
                pix.save(fpath)

                saved.append({
                    "page": global_page_idx + 1,
                    "url": f"/static/doc-images/{quote(fname)}",   # encoded local URL for your frontend
                    "file": fpath,                      # absolute/relative file path on disk
                    "caption": caption_text
                })

        return saved