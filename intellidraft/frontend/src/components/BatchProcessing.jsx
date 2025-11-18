import { FileText } from 'lucide-react'

function BatchProcessing({ templateInfo }) {
  return (
    <div className="text-center py-12">
      <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
      <h3 className="text-xl font-semibold text-gray-700 mb-2">
        Batch Processing
      </h3>
      <p className="text-gray-600 mb-4">
        This feature will be available in Phase 2
      </p>
      <div className="max-w-md mx-auto text-left bg-gray-50 rounded-lg p-4">
        <h4 className="font-semibold text-gray-800 mb-2">Planned Features:</h4>
        <ul className="space-y-2 text-sm text-gray-600">
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Upload CSV file with multiple part numbers</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Process all components automatically</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Generate individual documents for each component</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Download all documents as a ZIP file</span>
          </li>
        </ul>
      </div>
    </div>
  )
}

export default BatchProcessing
