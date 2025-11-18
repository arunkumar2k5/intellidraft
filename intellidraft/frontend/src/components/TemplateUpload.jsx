import { useState } from 'react'
import { Upload, CheckCircle, AlertCircle } from 'lucide-react'
import { uploadTemplate } from '../services/api'

function TemplateUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.name.endsWith('.docx')) {
      setFile(selectedFile)
      setUploadStatus(null)
    } else {
      setUploadStatus({ type: 'error', message: 'Please select a .docx file' })
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setUploadStatus(null)

    try {
      const result = await uploadTemplate(file)
      setUploadStatus({ type: 'success', message: 'Template uploaded successfully!' })
      onUploadSuccess(result)
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Upload failed. Please try again.',
      })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload Template</h2>
      
      <div className="space-y-4">
        {/* File Input */}
        <div className="flex items-center space-x-4">
          <label className="flex-1">
            <div className="flex items-center justify-center w-full h-32 px-4 transition bg-white border-2 border-gray-300 border-dashed rounded-lg appearance-none cursor-pointer hover:border-indigo-400 focus:outline-none">
              <div className="flex flex-col items-center space-y-2">
                <Upload className="w-8 h-8 text-gray-400" />
                <span className="text-sm text-gray-600">
                  {file ? file.name : 'Click to select .docx template'}
                </span>
              </div>
              <input
                type="file"
                className="hidden"
                accept=".docx"
                onChange={handleFileChange}
              />
            </div>
          </label>
        </div>

        {/* Upload Button */}
        {file && (
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="w-full px-4 py-2 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? 'Uploading...' : 'Upload Template'}
          </button>
        )}

        {/* Status Messages */}
        {uploadStatus && (
          <div
            className={`flex items-center space-x-2 p-3 rounded-lg ${
              uploadStatus.type === 'success'
                ? 'bg-green-50 text-green-800'
                : 'bg-red-50 text-red-800'
            }`}
          >
            {uploadStatus.type === 'success' ? (
              <CheckCircle className="w-5 h-5" />
            ) : (
              <AlertCircle className="w-5 h-5" />
            )}
            <span className="text-sm">{uploadStatus.message}</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default TemplateUpload
