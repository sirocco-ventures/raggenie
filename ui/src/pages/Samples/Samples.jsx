import DashboardBody from "src/layouts/dashboard/DashboadBody"
import EmptySample from "./EmptySample"
import Modal from "src/components/Modal/Modal"
import { useEffect, useState } from "react"
import SampleForm from "./SampleForm"
import { getSamples } from "src/services/Sample"
import { deleteSamples } from "src/services/Sample"
import SampleList from "./SampleList"
import { BsInfoCircle } from "react-icons/bs"
import confirmDialog from "src/utils/ConfirmDialog"


const Samples = ()=>{

    const [sampleList, setSampleList] = useState([])
    const [showSampleModal, setSampleModal] = useState(false)
    const [editSample, setEditSample] = useState({})

    const  getAllSamples = ()=>{
        getSamples().then(response=>{
            setSampleList(response.data?.data?.sql ?? [])
        })
    }

    const onEdit = (sampleData)=>{
        setSampleModal(true)
        setEditSample(sampleData)
    }
    
    const onDelete = (sampleData)=>{
        confirmDialog(
            "Confirmation",
            "Are you sure you want to delete this?",
            {
                onConfirm: () => {
                    deleteSamples(sampleData.id);
                    setTimeout(() => {
                        getAllSamples()
                    },100) }
            },
            
          );

    }

     

    const onCreateNew = ()=>{
        setSampleModal(true)
        setEditSample({})
        
    }


    useEffect(()=>{
        getAllSamples()
    }, [])

    return(
       <DashboardBody title="Samples">

        { sampleList?.length == 0 && <EmptySample onCreateClick={()=>setSampleModal(true)} /> }
        { sampleList?.length > 0 && <SampleList data={sampleList} onCreate={onCreateNew} onEdit={onEdit} onDelete={onDelete}/> }

        <Modal title={Object.keys(editSample).length > 0 ? "Edit Sample" : "Create Sample"} show={showSampleModal} onClose={()=>setSampleModal(false)} >
            <SampleForm sample={editSample} afterCreate={getAllSamples} onCancel={()=>setSampleModal(false)} />
        </Modal>
        
       </DashboardBody>
    )
}

export default Samples