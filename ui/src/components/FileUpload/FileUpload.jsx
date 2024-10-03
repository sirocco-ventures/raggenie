import React from 'react';
import TitleDescription from '../TitleDescription/TitleDescription';
import style from './FileUpload.module.css';
import FolderIcon from './assets/folderIcon.svg';
import FileIcon from './assets/fileIcon.svg';
import closeIcon from "./assets/closeIcon.svg"

const FileUpload = ({
    title = "",
    description = "",
    accept = "*",
    progressPrecentage = '',
    progressTime = "",
    files = [],
    onAddFileOnDrag = () => { },
    onFileChange = () => { },
    onRemoveFile = () => { },
    pdfUploadRef = null,
    showProgressBar = false,
    SupportedFileMessage = "",
    DragMessage = "",
    multipleFileSupport = false
}) => {
    return (
        <div>
            <TitleDescription title={title} description={description} descriptionStyle={{paddingBottom:"23px"}} />
            <div className={style.DragContainer} onDragOver={(e) => e.preventDefault()} onDragEnter={(e) => e.preventDefault()} onDrop={onAddFileOnDrag}>
                <img src={FolderIcon} alt="Folder Icon" />
                <h4 className={style.DragMessage}>{DragMessage}</h4>

                <input
                    type="file"
                    name="documentLoader"
                    className={style.FileUploader}
                    multiple={multipleFileSupport}
                    onChange={onFileChange}
                    accept={accept}
                    ref={pdfUploadRef}
                />

                <div className={style.OptionDefault}> <h5>OR</h5> </div>

                <button type='button' className={style.UploadButton} onClick={() => pdfUploadRef.current.click()}>
                    Browse file
                </button>
            </div>
            <p>{SupportedFileMessage}</p>

            <div>


                {showProgressBar ? (
                    <div className={style.ProgressContainer}>
                        <div className={style.ProgressAnalzer}>
                            <div className={style.ProgressBarContent}>
                                <div className={style.ProgressText}>
                                    <span>Uploading...</span>
                                    <span>{progressPrecentage}% • {progressTime} remaining</span>
                                </div>
                            </div>
                            <div className={style.ProgressBar}>
                                <span
                                    className={style.ProgressLine}
                                    style={{ width: `${progressPrecentage}%` }}
                                ></span>
                            </div>
                        </div>
                    </div>
                ) : (
                    files.map((fileItem, index) => (
                      <div key={index} className={style.ProgressContainer}>
                        <div className={style.FileInfo}>
                          <img src={FileIcon} alt="File Icon" className={style.FileIcon} />
                          <div className={style.FileName}>
                            <span className={style.FilesName}>{fileItem.file_name}</span>
                            <span className={style.FileSize}>{fileItem.file_size} MB</span> 
                          </div>
                        </div>
                        <div className={style.CloseProgress} onClick={() => onRemoveFile(fileItem.file_id)}>
                          <img src={closeIcon} width={24}/>
                        </div>
                      </div>
                    ))
                  )
                  }
            </div>
        </div>
    );
};

export default FileUpload;
