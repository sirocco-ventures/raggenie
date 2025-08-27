from loguru import logger
import os
from pathlib import Path
from urllib.parse import quote
import fitz #PyMuPDF


class DoclingParser:
    def __init__(self, static_root="static/doc-images", dpi=300):
        try:
            from docling.document_converter import DocumentConverter, PdfFormatOption
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
            from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
        except ImportError as e:
            raise RuntimeError(
                "Docling dependencies are not installed. "
                "Install with `pip install docling` to use DoclingParser."
            ) from e

        self.static_root = static_root
        self.dpi = dpi
        os.makedirs(self.static_root, exist_ok=True)

        pipeline_options = PdfPipelineOptions()
        pipeline_options.ocr_options = RapidOcrOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True


        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                    backend=DoclingParseV4DocumentBackend,
                )
            }
        )

    def document_ocr(self, path):
        """
        Returns a list with one item:
        {
          "content": [markdown_content],
          "images": [ {page, url, file, caption}, ... ],
          "metadata": {"path": path}
        }
        """
        metadata = {"path": path}
        pdf_stem = Path(path).stem
        
        logger.info(f"Processing document: {path}")
        
        # Convert document with Docling
        try:
            result = self.converter.convert(path)
            doc_structure = result.document
        except Exception as e:
            logger.error(f"Docling conversion failed: {e}")
            return [{"content": [], "images": [], "metadata": metadata}]
        
        # Convert to markdown
        markdown_content = result.document.export_to_markdown()
        
        # Extract images
        images = self._extract_and_save_images(path, doc_structure, pdf_stem)
        
        output = {
            "content": [markdown_content],
            "images": images,
            "metadata": metadata
        }
        
        logger.info(f"Extracted {len(images)} images and converted to markdown")
        return [output]
    
    
    def _get_picture_caption(self, picture, doc_structure):
        """Extract caption text for a picture"""
        if not picture.captions:
            return None
        
        # Get the first caption reference
        caption_ref = picture.captions[0]
        if not caption_ref.cref.startswith('#/texts/'):
            return None
        
        try:
            text_idx = int(caption_ref.cref.split('/')[-1])
            if text_idx < len(doc_structure.texts):
                caption_item = doc_structure.texts[text_idx]
                return caption_item.text.strip()
        except (ValueError, IndexError):
            pass
        
        return None
    
    
    def _extract_and_save_images(self, pdf_path, doc_structure, pdf_stem):
        """Extract and save images using Docling locations and PyMuPDF"""
        saved_images = []
        
        if not doc_structure.pictures:
            return saved_images
        
        # Open PDF with PyMuPDF
        try:
            pdf_doc = fitz.open(pdf_path)
        except Exception as e:
            logger.error(f"Failed to open PDF with PyMuPDF: {e}")
            return saved_images
        
        try:
            for pic_idx, picture in enumerate(doc_structure.pictures):
                if not picture.prov:
                    continue
                
                # Get bounding box from Docling
                prov = picture.prov[0]
                bbox = prov.bbox
                page_no = prov.page_no - 1  # Convert to 0-based indexing
                
                if page_no >= pdf_doc.page_count:
                    logger.warning(f"Page {page_no + 1} out of range")
                    continue
                
                # Skip very small images (likely logos or decorative elements)
                width = bbox.r - bbox.l
                height = bbox.t - bbox.b
                if width < 50 or height < 50:  # Skip images smaller than 50x50 points
                    logger.debug(f"Skipping small image {pic_idx + 1}: {width}x{height}")
                    continue
                
                logger.info(f"Extracting image {pic_idx + 1} from page {page_no + 1}")
                
                # Get the page
                page = pdf_doc[page_no]
                page_height = page.rect.height
                
                # Convert from Docling (bottom-left) to PyMuPDF (top-left) coordinates
                top = page_height - bbox.t
                bottom = page_height - bbox.b
                left = bbox.l
                right = bbox.r
                
                # Add padding to avoid cropping edges
                pad = 4  # points
                rect = fitz.Rect(
                    max(0, left - pad),
                    max(0, top - pad),
                    min(page.rect.width, right + pad),
                    min(page.rect.height, bottom + pad)
                )
                
                # Extract image with specified DPI
                mat = fitz.Matrix(self.dpi / 72.0, self.dpi / 72.0)
                pix = page.get_pixmap(matrix=mat, clip=rect, alpha=False)
                
                # Generate filename
                fname = f"{pdf_stem}_p{page_no + 1}_f{pic_idx + 1}.png"
                fpath = os.path.join(self.static_root, fname)
                
                # Save the image
                pix.save(fpath)
                pix = None  # Free memory
                
                # Get caption
                caption = self._get_picture_caption(picture, doc_structure)
                
                saved_images.append({
                    "page": page_no + 1,
                    "url": f"/{self.static_root}/{quote(fname)}",
                    "file": fpath,
                    "caption": caption
                })
                
                logger.info(f"Saved image: {fname}")
        
        finally:
            pdf_doc.close()
        
        return saved_images
