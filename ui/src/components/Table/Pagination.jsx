import style from "./Table.module.css"

const Pagination = (props)=>{

    let totalButtons = Math.floor(props.rowCount/props.rowsPerPage) + 1 ?? 0
  
    let starting = (props.currentPage - 1) * props.rowsPerPage
    let ending = props.rowCount

    let buttonStartFrom = totalButtons > 10 ? parseInt(props.currentPage) : 1;

    if (buttonStartFrom > (totalButtons - 10) && totalButtons > 10){
        buttonStartFrom = totalButtons - 9
    }

    const onPageInputChange = (e)=>{
        if(isNaN(e.key) && e.keyCode != 8){
            e.preventDefault()
        }
    }


    return(
        <>
            <div className={style.Pagination}>
                { totalButtons > 10  && (<>
                                    <button className={`${style.opPaginationButton} `} disabled={props.currentPage == 1}  style={{width: "auto"}} onClick={()=>props.onChangePage(1)}>First</button>
                                    <button className={`${style.opPaginationButton} `} disabled={props.currentPage == 1} style={{width: "auto"}} onClick={()=>props.onChangePage( props.currentPage - 1)}>Previous</button>
                            </>)} 
                            {/* <div> */}
                            {
                                 new Array(totalButtons > 10 ? 10 : totalButtons).fill(0).map((item,index)=>{
                                    return(
                                        <button key={index} 
                                        className={`${style.PaginationButton}  ${(buttonStartFrom + index) == props.currentPage ? style.PaginationButtonSelected:""}`} 
                                        onClick={()=>props.onChangePage(buttonStartFrom + index)}>{buttonStartFrom  + index}</button>)
                                    
                                })
                            } 
                            {/* </div> */}

                           { totalButtons > 10 && (<>
                                <button className={`${style.opPaginationButton} `} disabled={props.currentPage == totalButtons} style={{width: "auto"}} onClick={()=>props.onChangePage( props.currentPage + 1)}>Next</button>
                                <button className={`${style.opPaginationButton} `} disabled={props.currentPage == totalButtons} style={{width: "auto"}} onClick={()=>props.onChangePage(totalButtons)}>Last</button>
                           </>) }
            </div>
        </>
    )
}

export default Pagination