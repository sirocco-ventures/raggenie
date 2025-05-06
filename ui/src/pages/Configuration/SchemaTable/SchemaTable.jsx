import React, { useState, useRef, useMemo } from "react";
import style from "./SchemaTable.module.css";
import expandIcon from "./assets/tableExpandIcon.svg";
import collapseIcon from "./assets/tableCollapseIcon.svg";
import tableIcon from "./assets/table.svg";
import columnIcon from "./assets/rows.svg";
import pencilIcon from "./assets/pencil.svg";
import leftIcon from "./assets/ChevronLeft.svg";
import rightIcon from "./assets/ChevronRight.svg";

function SchemaTable({ data, itemsPerPage = 8 }) {
  const [expandedRows, setExpandedRows] = useState({});
  const [expandedColRows, setExpandedColRows] = useState({});
  const [currentPage, setCurrentPage] = useState(1);
  const textAreaRefs = useRef({});
  const colTextAreaRefs = useRef({});

  // Pagination logic
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return data.slice(startIndex, startIndex + itemsPerPage);
  }, [data, currentPage, itemsPerPage]);

  const totalPages = Math.ceil(data.length / itemsPerPage);

  const toggleRow = (id, event) => {
    setExpandedRows((prev) => ({
      ...Object.fromEntries(Object.keys(prev).map((k) => [k, false])),
      [id]: !prev[id],
    }));

    const items = document.querySelectorAll(`[data-key]`);
    items.forEach((item) => {
      if (item.getAttribute("data-key") === id) {
        item.style.display = item.style.display === "block" ? "none" : "block";
      } else {
        item.style.display = "none";
      }
    });
    if (event) {
      event.target.parentNode.nextElementSibling.firstChild.lastChild.focus();
      event.stopPropagation();
    }
  };

  const toggleColRow = (id, event) => {
    setExpandedColRows((prev) => ({
      ...Object.fromEntries(Object.keys(prev).map((k) => [k, false])),
      [id]: !prev[id],
    }));
    const items = document.querySelectorAll(`[data-col-key]`);

    items.forEach((item) => {
      if (item.getAttribute("data-col-key") === id) {
        item.style.display = item.style.display === "block" ? "none" : "block";
      } else {
        item.style.display = "none";
      }
    });
    if (event) {
      event.target.parentNode.nextElementSibling.lastChild.focus();
      event.stopPropagation();
    }
  };

  const handleDescriptionChange = (event, id, colId) => {
    const newDescription = event.target.value;
    const dbSchema = JSON.parse(localStorage.getItem("dbschema") || "{}");
    if (colId) {
      if (dbSchema[id]) {
        console.log(newDescription);
        dbSchema[id].columns[colId].description = newDescription;
        localStorage.setItem("dbschema", JSON.stringify(dbSchema));
      }
    } else if (dbSchema[id]) {
      dbSchema[id].description = newDescription;
      localStorage.setItem("dbschema", JSON.stringify(dbSchema));
    }
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    setExpandedRows({});
    setExpandedColRows({});
    const rowItems = document.querySelectorAll(`[data-key]`);
    const colItems = document.querySelectorAll(`[data-col-key]`);
    [...rowItems, ...colItems].forEach((item) => {
      item.style.display = "none";
    });
  };

  const getPaginationButtons = (currentPage, totalPages) => {
    const pages = [];

    if (totalPages <= 5) {
      // Show all pages if there are 5 or fewer
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Always show page 1
      pages.push(1);

      // Show first 4 pages if current page is within them
      if (currentPage <= 3) {
        pages.push(2, 3, 4, "...");
      }
      // Show last 4 pages if current page is near the end
      else if (currentPage >= totalPages - 2) {
        pages.push("...", totalPages - 3, totalPages - 2, totalPages - 1);
      }
      // Show middle pages around current page
      else {
        pages.push("...", currentPage - 1, currentPage, currentPage + 1, "...");
      }

      // Always show the last page
      pages.push(totalPages);
    }

    return pages;
  };

  return (
    <div className={style.tableContainer}>
      <div className={style.tableHeader}>NAME</div>
      {paginatedData.map((item, index) => (
        <div key={item.table_id}>
          <div
            className={`${style.rowTitle} ${
              expandedRows[item.table_id] ? style.tdOnfocus : ""
            }`}
            onClick={() => toggleRow(item.table_id)}
          >
            <div>
              <img
                src={expandedRows[item.table_id] ? collapseIcon : expandIcon}
              />
              <img src={tableIcon} />
              {item.table_name}
            </div>
            <img
              src={pencilIcon}
              onClick={(event) => toggleRow(item.table_id, event)}
            />
          </div>
          <div>
            <div
              className={style.descriptionContainer}
              data-key={item.table_id}
              style={{ display: "none" }}
            >
              <span>Description</span>
              <textarea
                ref={(el) => (textAreaRefs.current[index] = el)}
                className={style.descriptionTextarea}
                defaultValue={item.description}
                onChange={(event) =>
                  handleDescriptionChange(event, item.table_id)
                }
              />
            </div>
            {item.columns.map((column, colIndex) => (
              <div
                className={style.dbColumnContainer}
                key={colIndex}
                data-key={item.table_id}
                style={{ display: "none" }}
              >
                <div
                  className={`${style.dbColumnTd} ${style.rowTitle} ${
                    expandedColRows[column.column_id] ? style.colOnfocus : ""
                  }`}
                  onClick={() => toggleColRow(column.column_id)}
                >
                  <div className={style.columnIndent}>
                    <img
                      src={
                        expandedColRows[column.column_id]
                          ? collapseIcon
                          : expandIcon
                      }
                    />
                    <img src={columnIcon} />
                    {column.column_name}
                  </div>
                  <img
                    src={pencilIcon}
                    onClick={(event) => toggleColRow(column.column_id, event)}
                  />
                </div>
                <div
                  className={`${style.descriptionContainer} ${style.coldescription}`}
                  data-col-key={column.column_id}
                  style={{ display: "none" }}
                >
                  <span>Description</span>
                  <textarea
                    ref={(el) => (colTextAreaRefs.current[colIndex] = el)}
                    className={style.descriptionTextarea}
                    defaultValue={column.description}
                    onChange={(event) =>
                      handleDescriptionChange(
                        event,
                        item.table_id,
                        column.column_id
                      )
                    }
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Pagination Controls */}
      <div className={style.paginationContainer}>
        <button
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          <img src={leftIcon}></img>
        </button>

        {/* Render Pagination Buttons */}
        {getPaginationButtons(currentPage, totalPages).map((page, index) => (
          <button
            key={index}
            onClick={() => typeof page === "number" && handlePageChange(page)}
            className={currentPage === page ? style.activePage : ""}
            disabled={page === "..."}
          >
            {page}
          </button>
        ))}

        <button
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          <img src={rightIcon}></img>
        </button>
      </div>
    </div>
  );
}

export default SchemaTable;
