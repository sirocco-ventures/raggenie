import DashboardBody from "src/layouts/dashboard/DashboadBody"
import EmptySample from "./EmptySample"
import Modal from "src/components/Modal/Modal"
import { useEffect, useState } from "react"
import SampleForm from "./SampleForm"
import { getSamples } from "src/services/Sample"
import SampleList from "./SampleList"
import { useNavigate } from "react-router-dom";


const Samples = ()=>{
    const navigate = useNavigate()
    const [sampleList, setSampleList] = useState([])
    const [showSampleModal, setSampleModal] = useState(false)
    const [editSample, setEditSample] = useState({})

    const  getAllSamples = ()=>{
        getSamples().then(response=>{
            setSampleList(response.data?.data?.sql ?? [])
        }).catch(() => {
            navigate('/error')
        })
    }

    const onEdit = (sampleData)=>{
        setSampleModal(true)
        setEditSample(sampleData)
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
        { sampleList?.length > 0 && <SampleList data={sampleList} onCreate={onCreateNew} onEdit={onEdit} /> }

        <Modal title="Create Sample" show={showSampleModal} onClose={()=>setSampleModal(false)} >
            <SampleForm sample={editSample} afterCreate={getAllSamples} onCancel={()=>setSampleModal(false)} />
        </Modal>
       </DashboardBody>
    )
}

export default Samples