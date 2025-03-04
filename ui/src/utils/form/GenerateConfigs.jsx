import React from 'react'
import FileUpload from 'src/components/FileUpload/FileUpload';
import Input from 'src/components/Input/Input'
import Textarea from 'src/components/Textarea/Textarea';
import style from "src/pages/Configuration/ProviderForm/ProviderForm.module.css"


const GenerateConfigs = ({ register = () => { }, errors = " ", configs = " ", fileConfig = {}, restForm = () => { } }) => {
    

    const parseValue = (value = '')=>{
        try{
            return JSON.stringify(value, undefined, 3)
        }
        catch(error){
            console.log({parseValue: error})
            return value
        }
    }


    return (
        <>
            {configs?.map((item, index) => {

                switch (item.config_type) {
                    case 1: return <Input key={index} type="text" label={item.name} placeholder={item.description} defaultValue={ parseValue(item.value)} required={item.required} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, { required: item.required ? "This is required" : false })} onChange={restForm} />
                    case 2: return <Input key={index} type="password" label={item.name} placeholder={item.description} defaultValue={ parseValue(item.value)} required={item.required} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message}  {...register(item.slug, { required: item.required ? "This is required" : false })} onChange={restForm} />
                    case 3: return <Input key={index} type="number" label={item.name} placeholder={item.description} defaultValue={ parseValue(item.value)} required={item.required} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, { required: item.required ? "This is required" : false })} onChange={restForm} />
                    case 4: return <Input key={index} type="url" label={<> {item.name} <span style={{ color: "#C8C8C8" }}>(Include http or https in the url)</span> </>} defaultValue={ parseValue(item.value)} required={item.required} placeholder={item.placeholder || "https://www.raggenie.com"} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, { required: item.required ? "This is required" : false })} onChange={restForm} />
                    case 5: return <Input key={index} type="email" label={`${item.name}  `} defaultValue={ parseValue(item.value)} required={item.required} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, { required: item.required ? "This is required" : false })} onChange={restForm} />
                    case 6: return (
                        <div className={style.SelectDropDown}>
                            <label className={style.SelectDropDownLabel}>{item.name} {item.required && <span className="span-important"></span>} </label>
                            <select name="selectOption" key={index} className={`${errors[item.slug]?.message ? style.SelectHasError : ""}`}  {...register(item.slug, { required: "This is required" })} onChange={(e) => restForm(e)}>
                                {item.value?.map((val, valIndex) => {
                                    return (
                                        <option key={valIndex} value={val.value}>
                                            {val.label}
                                        </option>
                                    );
                                })}
                            </select>

                            {errors[item.slug]?.message != "" && <label className={style.SelectErrorMessage}>{errors[item.slug]?.message}</label>}
                        </div>
                    )
                    case 7: return <Textarea key={index} rows="5" label={item.name} defaultValue={ parseValue(item.value)} required={item.required} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, { required: item.required ? "This is required" : false })} onChange={restForm} />
                    case 8: return (
                        <FileUpload
                            {...fileConfig}
                        />
                    )
                    default: return <Input key={index} type="text" label={item.name} defaultValue={ parseValue(item.value)} required={item.required} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, { required: item.required ? "This is required" : false })} onChange={restForm} />
                }

            })}
        </>
    )
}

export default GenerateConfigs