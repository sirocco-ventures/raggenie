
import DataTable from "react-data-table-component"
import Pagination from "./Pagination"
import expandIcon from "./assets/tableExpandIcon.svg"
import collapseIcon from "./assets/tableCollapseIcon.svg"
import style from "./Table.module.css"
import "./DatatableCustomTheme.css"

const Table = ({
    columns = [],
    data= [],
    ...props
})=>{

    return(
        <>
            <div className={style.Table}>
                <DataTable 
                    columns={columns} 
                    data={data} 
                    pagination={true} 
                    paginationPerPage={10}
                    paginationComponent={Pagination} 
                    expandableIcon={{collapsed:  <img src={collapseIcon} className={style.TableExpandCollapseIcon} />, expanded: <img src={expandIcon} className={style.TableExpandCollapseIcon} />}}
                    {...props}/>
            </div>
            
        
        </>
    )
}

export default Table