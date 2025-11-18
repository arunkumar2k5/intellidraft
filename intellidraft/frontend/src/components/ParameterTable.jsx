import { Edit2 } from 'lucide-react'

function ParameterTable({ parameters, onParameterChange }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800">Component Parameters</h3>
        <p className="text-sm text-gray-600 mt-1">Edit values as needed before generating document</p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Parameter
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Value
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-16">
                Edit
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {Object.entries(parameters).map(([key, value]) => (
              <tr key={key} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {key}
                </td>
                <td className="px-6 py-4 text-sm text-gray-700">
                  <input
                    type="text"
                    value={value}
                    onChange={(e) => onParameterChange(key, e.target.value)}
                    className="w-full px-3 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                  />
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <Edit2 className="w-4 h-4 text-gray-400" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 text-sm text-gray-600">
        Total parameters: {Object.keys(parameters).length}
      </div>
    </div>
  )
}

export default ParameterTable
