import Button from "src/components/Button/Button"
import { HiOutlinePlusCircle } from "react-icons/hi";
import { FaPen, FaTrashCan } from "react-icons/fa6"
import { BsQuestionSquare } from "react-icons/bs";
import Table from "src/components/Table/Table"
import style from "./Samples.module.css"
import TitleDescription from "src/components/TitleDescription/TitleDescription";


const SampleList = ({data, onCreate=()=>{}, onEdit = ()=>{},onDelete = ()=>{}})=>{


    const tableColums = [
        {
            name: 'Question List',
            selector: row =><div className="flex flex-align-center flex-gap-10"> <span> <BsQuestionSquare color="#BEBEBE" size={18}/></span> <span> {row.description}</span> </div>  ,
            grow: 1,
        },
        {
            name: '',
            selector: row => <><span onClick={()=>onEdit(row)}> <FaPen color="#84BCFF" size={16}/> </span></> ,
            width: "50px"
        },
        {
            name: '',
            selector: row => <><span onClick={()=>onDelete(row)}> <FaTrashCan color="#FF7F6D" size={16}/> </span></> ,
            width: "80px"
        },

    ]

    const rowExpandComponent = (row)=>{
        return(
             <div className={style.SampleExpandContaner}>
                <div className={style.SampleExpandRow}>
                    <span className={style.SampleRowLabel}>Query :</span> <span>{row.data?.sql_metadata?.query}</span>
                </div>
                <div className={style.SampleExpandRow}>
                    <span className={style.SampleRowLabel} style={{marginRight: "5px"}}>Metadata :</span><span>{row.data?.sql_metadata?.metadata}</span>
                </div>
            </div>
        )
    }


    return(
        <div>
            <div className="text-align-right" style={{marginBottom: "41px"}}>
                <Button onClick={onCreate}>Create Sample <HiOutlinePlusCircle/></Button>
            </div>
            <div>
                <TitleDescription title="Samples List" description="Please provide additional samples to enhance the accuracy and effectiveness of the results. More examples will help improve the quality of analysis and ensure better outcomes." />
            </div>
            <div>
                <Table columns={tableColums} data={data} expandableRows={true} expandableRowsComponent={rowExpandComponent} />
            </div>
        </div>
    )

}

export default SampleList