import axios from "axios";

const UploadFile = (url, formData, onProgress) => {
  return new Promise((resolve, reject) => {
    const startTime = new Date().getTime(); // Record the start time

    axios.post(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (event) => {
        const { loaded, total } = event;
        const percentage = Math.floor((loaded / total) * 100);

        // Time calculations
        const currentTime = new Date().getTime();
        const elapsedTime = (currentTime - startTime) / 1000; 
        const uploadSpeed = loaded / elapsedTime; 
        const remainingBytes = total - loaded;
        const remainingTime = remainingBytes / uploadSpeed; 

        const remainingTimeFormatted = formatRemainingTime(remainingTime);

        onProgress(percentage, remainingTimeFormatted); 
      },
    })
    .then(response => resolve(response))
    .catch(error => reject(new Error(`File upload failed: ${error.response?.data?.message || error.message}`)));
  });
};


const formatRemainingTime = (timeInSeconds) => {
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = Math.floor(timeInSeconds % 60);
  return `${minutes > 0 ? `${minutes}m ` : ""}${seconds}s`;
};

export default UploadFile;
