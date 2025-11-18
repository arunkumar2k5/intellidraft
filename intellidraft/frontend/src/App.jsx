import { useState } from 'react'
import TemplateUpload from './components/TemplateUpload'
import SingleComponent from './components/SingleComponent'
import BatchProcessing from './components/BatchProcessing'
import { FileText } from 'lucide-react'

function App() {
  const [activeTab, setActiveTab] = useState('single')
  const [templateInfo, setTemplateInfo] = useState(null)

  const handleTemplateUpload = (info) => {
    setTemplateInfo(info)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <FileText className="w-8 h-8 text-indigo-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">IntelliDraft</h1>
              <p className="text-sm text-gray-600">Component Documentation System</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Template Upload Section */}
        <div className="mb-8">
          <TemplateUpload onUploadSuccess={handleTemplateUpload} />
        </div>

        {/* Tabs Section */}
        {templateInfo && (
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Tab Headers */}
            <div className="border-b border-gray-200">
              <nav className="flex -mb-px">
                <button
                  onClick={() => setActiveTab('single')}
                  className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === 'single'
                      ? 'border-indigo-600 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Single Component
                </button>
                <button
                  onClick={() => setActiveTab('batch')}
                  className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === 'batch'
                      ? 'border-indigo-600 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Batch Processing
                </button>
              </nav>
            </div>

            {/* Tab Content */}
            <div className="p-6">
              {activeTab === 'single' && (
                <SingleComponent templateInfo={templateInfo} />
              )}
              {activeTab === 'batch' && (
                <BatchProcessing templateInfo={templateInfo} />
              )}
            </div>
          </div>
        )}

        {/* Instructions when no template */}
        {!templateInfo && (
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              Get Started
            </h3>
            <p className="text-gray-600">
              Upload a template document to begin processing components
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 text-center text-gray-600 text-sm">
        <p>IntelliDraft v1.0.0 - Phase 1</p>
      </footer>
    </div>
  )
}

export default App
