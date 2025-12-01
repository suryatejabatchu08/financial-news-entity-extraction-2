import { useState } from 'react'
import axios from 'axios'
import { Sparkles, Loader2, AlertCircle, Upload, FileText } from 'lucide-react'
import EntityDisplay from '../components/EntityDisplay'

const SAMPLE_TEXT = "Apple Inc. announced a $50 million acquisition of TechStart on Monday. The deal was finalized in New York and will be completed by December 2024. CEO Tim Cook stated that this represents 15% of their annual investment budget."

function Home() {
    const [text, setText] = useState('')
    const [entities, setEntities] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [fileName, setFileName] = useState(null)
    const [isDragging, setIsDragging] = useState(false)

    const handleExtract = async () => {
        if (!text.trim()) {
            setError('Please enter some text to analyze')
            return
        }

        setLoading(true)
        setError(null)

        try {
            const response = await axios.post('/api/predict', { text })
            setEntities(response.data.entities)
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to extract entities. Make sure the backend is running.')
            console.error('Error:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleUseSample = () => {
        setText(SAMPLE_TEXT)
        setEntities(null)
        setError(null)
        setFileName(null)
    }

    const readFileContent = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader()

            reader.onload = (e) => {
                const content = e.target.result

                // Handle CSV files - extract text from first column or all text
                if (file.name.endsWith('.csv')) {
                    // Simple CSV parsing - join all text content
                    const lines = content.split('\n')
                    const textContent = lines
                        .map(line => line.trim())
                        .filter(line => line.length > 0)
                        .join(' ')
                    resolve(textContent)
                } else {
                    // Handle TXT files - use content as-is
                    resolve(content)
                }
            }

            reader.onerror = () => reject(new Error('Failed to read file'))
            reader.readAsText(file)
        })
    }

    const handleFileUpload = async (file) => {
        if (!file) return

        // Validate file type
        const validExtensions = ['.txt', '.csv']
        const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()

        if (!validExtensions.includes(fileExtension)) {
            setError('Please upload a .txt or .csv file')
            return
        }

        setError(null)
        setFileName(file.name)

        try {
            const content = await readFileContent(file)
            setText(content)
            setEntities(null) // Clear previous results
        } catch (err) {
            setError('Failed to read file. Please try again.')
            console.error('File reading error:', err)
        }
    }

    const handleFileInputChange = (e) => {
        const file = e.target.files?.[0]
        if (file) {
            handleFileUpload(file)
        }
    }

    const handleDragOver = (e) => {
        e.preventDefault()
        setIsDragging(true)
    }

    const handleDragLeave = (e) => {
        e.preventDefault()
        setIsDragging(false)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setIsDragging(false)

        const file = e.dataTransfer.files?.[0]
        if (file) {
            handleFileUpload(file)
        }
    }

    return (
        <div className="container mx-auto px-4 py-8 max-w-6xl">
            {/* Hero Section */}
            <div className="text-center mb-12">
                <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    Financial News Entity Extraction
                </h1>
                <p className="text-slate-400 text-lg max-w-2xl mx-auto">
                    Extract named entities from financial news articles using advanced NLP.
                    Identify companies, people, locations, monetary values, and more.
                </p>
            </div>

            {/* Input Section */}
            <div className="bg-slate-800/50 rounded-2xl p-6 md:p-8 border border-slate-700/50 backdrop-blur-sm mb-8">
                <div className="flex items-center justify-between mb-4">
                    <label className="text-white font-semibold text-lg">
                        Enter Financial News Text
                    </label>
                    <button
                        onClick={handleUseSample}
                        className="text-sm text-blue-400 hover:text-blue-300 transition-colors font-medium"
                    >
                        Use Sample Text
                    </button>
                </div>

                {/* File Upload Area */}
                <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`mb-4 border-2 border-dashed rounded-xl p-6 transition-all ${isDragging
                            ? 'border-blue-500 bg-blue-500/10'
                            : 'border-slate-600 hover:border-slate-500'
                        }`}
                >
                    <div className="flex flex-col items-center gap-3">
                        <div className="bg-slate-700/50 p-3 rounded-lg">
                            <Upload className="w-6 h-6 text-slate-300" />
                        </div>
                        <div className="text-center">
                            <p className="text-slate-300 font-medium mb-1">
                                Drop your file here or{' '}
                                <label className="text-blue-400 hover:text-blue-300 cursor-pointer underline">
                                    browse
                                    <input
                                        type="file"
                                        accept=".txt,.csv"
                                        onChange={handleFileInputChange}
                                        className="hidden"
                                    />
                                </label>
                            </p>
                            <p className="text-slate-500 text-sm">
                                Supports TXT and CSV files
                            </p>
                        </div>
                        {fileName && (
                            <div className="flex items-center gap-2 bg-slate-700/50 px-4 py-2 rounded-lg">
                                <FileText className="w-4 h-4 text-blue-400" />
                                <span className="text-slate-300 text-sm">{fileName}</span>
                            </div>
                        )}
                    </div>
                </div>

                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste your financial news article here or upload a file..."
                    className="w-full h-48 bg-slate-900/50 text-white rounded-xl p-4 border border-slate-700/50 focus:border-blue-500/50 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all resize-none"
                />

                {error && (
                    <div className="mt-4 bg-red-500/10 border border-red-500/50 rounded-lg p-4 flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        <p className="text-red-300 text-sm">{error}</p>
                    </div>
                )}

                <button
                    onClick={handleExtract}
                    disabled={loading || !text.trim()}
                    className="mt-6 w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:from-slate-700 disabled:to-slate-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 flex items-center justify-center gap-3 disabled:cursor-not-allowed shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40"
                >
                    {loading ? (
                        <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Extracting Entities...
                        </>
                    ) : (
                        <>
                            <Sparkles className="w-5 h-5" />
                            Extract Entities
                        </>
                    )}
                </button>
            </div>

            {/* Results Section */}
            {entities && (
                <div className="animate-fadeIn">
                    <h2 className="text-2xl font-bold text-white mb-6">Extracted Entities</h2>
                    <EntityDisplay entities={entities} text={text} />
                </div>
            )}
        </div>
    )
}

export default Home
