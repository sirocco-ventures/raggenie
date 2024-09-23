

import style from "../style.module.css"

const Table = ({data = [], dataLength = 10})=>{


    let tableHeader = [];

    const getTableHeader = ()=>{
        if(data.length > 0){
            let tempData = data[0];
            let keys = Object.keys(tempData).map(item=>item.replaceAll("_", " "));
            tableHeader = keys
        }
    }
   
    getTableHeader()

    return(
        <>
            <div className={style.ChartTableContainer}>
                <table cellSpacing={0} className={style.ChatTable}>
                    <thead>
                        <tr>
                            {tableHeader.map((item, index)=><th key={index}>{item}</th>)}
                        </tr>
                    </thead>
                    <tbody>
                        {data?.slice(0, dataLength)?.map((item, dIndex)=>{
                            return(
                                <tr key={dIndex}>
                                    { Object.values((item)).map(value=><td>{value}</td>) }
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        </>
    )

}


export default Table