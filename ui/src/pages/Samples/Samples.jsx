import DashboardBody from "src/layouts/dashboard/DashboadBody"
import EmptySample from "./EmptySample"
import Modal from "src/components/Modal/Modal"
import { useEffect, useState } from "react"
import SampleForm from "./SampleForm"
import { getSamples, deleteSample } from "src/services/Sample"
import SampleList from "./SampleList"
import { confirmDialog } from "src/utils/confirmDialog"
import { toast } from "react-toastify"

const Samples = () => {
  const [sampleList, setSampleList] = useState([])
  const [showSampleModal, setSampleModal] = useState(false)
  const [editSample, setEditSample] = useState({})

  const getAllSamples = () => {
    getSamples().then(response => {
      setSampleList(response.data?.data?.sql ?? [])
    })
  }

  const onEdit = (sampleData) => {
    setSampleModal(true)
    setEditSample(sampleData)
  }

  const onCreateNew = () => {
    setSampleModal(true)
    setEditSample({})
  }

  const onDelete = (sampleData) => {
    confirmDialog({
      title: "Delete Sample",
      message: "Are you sure you want to delete this sample?",
      onConfirm: () => {
        deleteSample(sampleData.id).then(() => {
          getAllSamples()
          toast.success("Sample deleted successfully")
        }).catch(error => {
          console.error("Error deleting sample:", error)
          toast.error("Failed to delete sample. Please try again.")
        })
      }
    })
  }

  useEffect(() => {
    getAllSamples()
  }, [])

  return (
    <DashboardBody title="Samples">
      {sampleList?.length == 0 && <EmptySample onCreateClick={() => setSampleModal(true)} />}
      {sampleList?.length > 0 && (
        <SampleList
          data={sampleList}
          onCreate={onCreateNew}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      )}
      <Modal title="Create Sample" show={showSampleModal} onClose={() => setSampleModal(false)}>
        <SampleForm sample={editSample} afterCreate={getAllSamples} onCancel={() => setSampleModal(false)} />
      </Modal>
    </DashboardBody>
  )
}

export default Samples
