import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadTemplate = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/upload-template`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const classifyComponent = async (partNumber) => {
  const response = await api.post('/classify-component', {
    part_number: partNumber,
  });
  return response.data;
};

export const fetchParameters = async (partNumber, componentType) => {
  const response = await api.post('/fetch-parameters', {
    part_number: partNumber,
    component_type: componentType,
  });
  return response.data;
};

export const generateDocument = async (templatePath, partNumber, componentType, parameters, description = '') => {
  const response = await api.post('/generate-document', {
    template_path: templatePath,
    part_number: partNumber,
    component_type: componentType,
    parameters: parameters,
    description: description,
  });
  return response.data;
};

export const downloadDocument = (filename) => {
  window.open(`${API_BASE_URL}/download/${filename}`, '_blank');
};

export default api;
