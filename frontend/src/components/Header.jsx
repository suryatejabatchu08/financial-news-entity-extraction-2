import { Link } from 'react-router-dom'
import { TrendingUp } from 'lucide-react'

function Header() {
    return (
        <header className="bg-slate-900/50 backdrop-blur-sm border-b border-slate-700/50 sticky top-0 z-50">
            <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-3 group">
                        <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg group-hover:scale-110 transition-transform">
                            <TrendingUp className="w-6 h-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-white">Financial NER</h1>
                            <p className="text-xs text-slate-400">Entity Extraction System</p>
                        </div>
                    </Link>

                    <nav className="flex gap-6">
                        <Link
                            to="/"
                            className="text-slate-300 hover:text-white transition-colors font-medium"
                        >
                            Extract
                        </Link>
                    </nav>
                </div>
            </div>
        </header>
    )
}

export default Header
