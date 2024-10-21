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
    const deleteIcon = (
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M10.6667 4.00016V3.46683C10.6667 2.72009 10.6667 2.34672 10.5213 2.06151C10.3935 1.81063 10.1895 1.60665 9.93865 1.47882C9.65344 1.3335 9.28007 1.3335 8.53333 1.3335H7.46667C6.71993 1.3335 6.34656 1.3335 6.06135 1.47882C5.81046 1.60665 5.60649 1.81063 5.47866 2.06151C5.33333 2.34672 5.33333 2.72009 5.33333 3.46683V4.00016M6.66667 7.66683V11.0002M9.33333 7.66683V11.0002M2 4.00016H14M12.6667 4.00016V11.4668C12.6667 12.5869 12.6667 13.147 12.4487 13.5748C12.2569 13.9511 11.951 14.2571 11.5746 14.4488C11.1468 14.6668 10.5868 14.6668 9.46667 14.6668H6.53333C5.41323 14.6668 4.85318 14.6668 4.42535 14.4488C4.04903 14.2571 3.74307 13.9511 3.55132 13.5748C3.33333 13.147 3.33333 12.5869 3.33333 11.4668V4.00016" stroke="#FF7F6D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    )

    const deleteFunction = () => {
      deleteSample(sampleData.id).then(() => {
        getAllSamples()
        toast.success("Sample deleted successfully")
      }).catch(error => {
        console.error("Error deleting sample:", error)
        toast.error("Failed to delete sample. Please try again.")
      })
    }

    confirmDialog(
      "Are you sure you want to delete this sample?",
      "",
      deleteIcon,
      null,
      "Delete",
      deleteFunction
    )
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
