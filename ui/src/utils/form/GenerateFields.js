export const GenerateFields = (type, item, index) => {
  switch(item.config_type){
    case 1: return <Input key={index} type="text" label={item.name} placeholder={item.description}  required={item.required}   hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: item.required ? "This is required": false})}  onChange={onChangesOption}/>     
    case 2: return <Input key={index} type="password" label={item.name} placeholder={item.description}  required={item.required}  hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message}  {...register(item.slug, {required: item.required ? "This is required": false})} onChange={onChangesOption}/>  
    case 3: return <Input key={index} type="number" label={item.name} placeholder={item.description}  required={item.required}  hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: item.required ? "This is required": false})}  onChange={onChangesOption}/>  
    case 4: return <Input key={index} type="url" label={ <> {item.name} <span style={{color: "#C8C8C8"}}>(Include http or https in the url)</span> </>} required={item.required} placeholder="https://www.raggenie.com" hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required:  item.required ? "This is required": false})}  onChange={onChangesOption}/>
    case 5: return <Input key={index} type="email" label={`${item.name}  `}  required={item.required}  placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required:  item.required ? "This is required": false})}  onChange={onChangesOption}/> 
    case 6: return (
        <div className={style.SelectDropDown}>
            <label className={style.SelectDropDownLabel}>{item.name} {item.required && <span className="span-important"></span>} </label>
            <select name="selectOption"  key={index}  className={`${errors[item.slug]?.message ? style.SelectHasError : ""}`}  {...register(item.slug, { required: "This is required" })}  onChange={(e) => onChangesOption(e)}>
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
    case 7: return <Textarea key={index} rows="5" label={item.name}  required={item.required} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: item.required ?  "This is required" : false})}  onChange={onChangesOption}/>  
    case 8: return(
        <FileUpload
        pdfUploadRef={pdfUploadRef}
        title="Upload your files"
        description="You can upload up to 5 files, with each file having a maximum size of 10 MB."
        accept=".pdf,.yaml,.txt,.docx"
        dragMessage="Drag your files to start uploading"
        progressPrecentage={progressPrecentage}
        showProgressBar={showProgressBar}
        progressTime={progressTime}
        onAddFileOnDrag={onAddFileOnDrag}
        onFileChange={onFileChange}
        onRemoveFile={onRemoveFile}
        files={files}
        supportedFileMessage={providerConfig[0]?.description}
        multipleFileSupport={false}
      />
    )
    default : return <Input key={index} type="text" label={item.name} required={item.required} placeholder={item.description}  hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required:  item.required ? "This is required": false})}  onChange={onChangesOption}/>     
}
};
