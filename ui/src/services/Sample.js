import { API_URL } from "src/config/const";
import GetService from "src/utils/http/GetService";
import PostService from "src/utils/http/PostService";
import DeleteService from "src/utils/http/DeleteService";

export const getSamples = () => {
  return GetService(API_URL + "/sql/list")
}

export const saveSamples = (sampleId, data) => {
  let apiURL = "/sql/create";
  if (sampleId) {
    apiURL = `/sql/update/${sampleId}`;
  }

  return PostService(API_URL + apiURL, {
    connector_id: data.connect_id,
    description: data.question,
    sql_metadata: {
      query: data.query,
      metadata: data.metadata
    }
  })
}

export const deleteSample = (sampleId) => {
  return DeleteService(API_URL + `/api/v1/sqldelete/${sampleId}`);
}
