import Button from "src/components/Button/Button"
import Input from "src/components/Input/Input"
import Textarea from "src/components/Textarea/Textarea"
import { FiCheckCircle, FiXCircle} from "react-icons/fi"
import { Controller, useForm } from "react-hook-form"
import Select from "src/components/Select/Select"
import { useEffect, useState } from "react"
import { getConnectors } from "src/services/Connectors"
import { saveSamples } from "src/services/Sample"
import { toast } from "react-toastify"

const SampleForm = ({ sample = {}, afterCreate = ()=>{}, onCancel = ()=>{}})=>{


    const [connectors, setConnectors] = useState([])
    // const [sampleId, setSampleId] = use

    const { register, handleSubmit, setValue , control, formState , reset: resetForm } = useForm({mode : "all"})
    const { errors, isValid: isFormValid } = formState


    const getAllConnectors = ()=>{
        getConnectors(2).then(response=>{

            let tempOptions = [];
            response.data?.data?.connectors?.map(item=>{
                tempOptions.push({label: item.connector_name, value: item.connector_id})
            })
            setConnectors(tempOptions)
        })
    }


    const saveSample = (data)=>{
        saveSamples(sample.id, {
            connect_id: data.connector,
            metadata: data.metadata,
            query: data.query,
            question: data.question
        }).then(response=>{
            toast.success("Sample saved successfully")
            afterCreate(response.data?.data)
        }).catch(()=>{
            toast.error("Sample saved failed")
        })
    }

    useEffect(()=>{
        resetForm()
        if(sample.id){
            setValue("question", sample.description)
            setValue("query", sample.sql_metadata?.query)
            setValue("metadata", sample.sql_metadata?.metadata)
            setValue("connector", sample.connector_id)
        }
    },[sample])

    useEffect(()=>{
        getAllConnectors()
    },[])

    return(
        <div>
            <form onSubmit={handleSubmit(saveSample)}>
                <div>
                    <Input label={<span className="span-important">Question</span>} hasError={errors["question"]?.message} errorMessage={errors["question"]?.message} {...register("question", {required: "This is required"})} />
                </div>
                <div>
                    <Controller
                        control={control}
                        name="connector"
                        rules={{
                            required: "This field is required"
                        }}
                        render={({ field: { onChange, value, ref } })=>(
                            <Select
                                inputRef={ref}
                                label={ <span className="span-important">Connector</span> }
                                value={connectors.find(c => c.value === value)}
                                options={connectors}
                                onChange={val=>onChange(val.value)} />
                        )}

                    />

                </div>
                <div>
                    <Textarea label={<span className="span-important">Query</span>} rows={6} style={{resize: "vertical"}} hasError={errors["query"]?.message} errorMessage={errors["query"]?.message} {...register("query", {required: "This is required"})}  />
                </div>
                <div>
                    <Textarea label="Metadata" rows={6} style={{resize: "vertical"}} hasError={errors["metadata"]?.message} errorMessage={errors["metadata"]?.message} {...register("metadata")} />
                </div>
                <div className="flex flex-gap-10 justify-content-end">
                    <div>
                        <Button variant="secondary-danger" onClick={onCancel}>Cancel <FiXCircle/></Button>
                    </div>
                    <div>
                        <Button  buttonType="submit" disabled={isFormValid ? false: true} onClick={onCancel}>Save <FiCheckCircle/></Button>
                    </div>
                </div>
            </form>
        </div>
    )

}

export default SampleForm