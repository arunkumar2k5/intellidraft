import { useState } from 'react'
import { Search, Loader2, Download, AlertCircle } from 'lucide-react'
import { classifyComponent, fetchParameters, generateDocument, downloadDocument } from '../services/api'
import ParameterTable from './ParameterTable'

function SingleComponent({ templateInfo }) {
  const [partNumber, setPartNumber] = useState('')
  const [loading, setLoading] = useState(false)
  const [componentData, setComponentData] = useState(null)
  const [parameters, setParameters] = useState({})
  const [error, setError] = useState(null)
  const [generating, setGenerating] = useState(false)

  const handleSearch = async () => {
    if (!partNumber.trim()) {
      setError('Please enter a part number')
      return
    }

    setLoading(true)
    setError(null)
    setComponentData(null)
    setParameters({})

    try {
      // Step 1: Classify component using OpenAI
      const classification = await classifyComponent(partNumber)
      
      // Step 2: Fetch parameters from Digi-Key
      const paramData = await fetchParameters(partNumber, classification.component_type)
      
      setComponentData({
        partNumber,
        componentType: classification.component_type,
        confidence: classification.confidence,
      })
      
      setParameters(paramData.parameters || {})
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch component data. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleParameterChange = (key, value) => {
    setParameters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const handleGenerateDocument = async () => {
    setGenerating(true)
    setError(null)

    try {
      const result = await generateDocument(
        templateInfo.template_id,
        componentData.partNumber,
        componentData.componentType,
        parameters
      )

      if (result.success) {
        // Download the generated document
        downloadDocument(result.output_filename)
        alert('Document generated successfully!')
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate document. Please try again.')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Search Section */}
      <div className="space-y-4">
        <div className="flex space-x-4">
          <input
            type="text"
            value={partNumber}
            onChange={(e) => setPartNumber(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Enter part number (e.g., GCM1885C1H180JA16D)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Searching...</span>
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                <span>Search</span>
              </>
            )}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="flex items-center space-x-2 p-3 bg-red-50 text-red-800 rounded-lg">
            <AlertCircle className="w-5 h-5" />
            <span className="text-sm">{error}</span>
          </div>
        )}
      </div>

      {/* Component Info */}
      {componentData && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Component Information</h3>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Part Number:</span>
              <p className="font-medium text-gray-900">{componentData.partNumber}</p>
            </div>
            <div>
              <span className="text-gray-600">Type:</span>
              <p className="font-medium text-gray-900 capitalize">{componentData.componentType}</p>
            </div>
            <div>
              <span className="text-gray-600">Confidence:</span>
              <p className="font-medium text-gray-900 capitalize">{componentData.confidence}</p>
            </div>
          </div>
        </div>
      )}

      {/* Parameters Table */}
      {Object.keys(parameters).length > 0 && (
        <>
          <ParameterTable
            parameters={parameters}
            onParameterChange={handleParameterChange}
          />

          {/* Generate Document Button */}
          <div className="flex justify-end">
            <button
              onClick={handleGenerateDocument}
              disabled={generating}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
            >
              {generating ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Generating...</span>
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  <span>Generate Document</span>
                </>
              )}
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default SingleComponent
