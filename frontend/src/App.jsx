import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Pill, Activity, BookOpen, User, Star, Menu, X, Rocket } from 'lucide-react';
import MechanismTab from './components/MechanismTab';
import LiteratureTab from './components/LiteratureTab';
import DigitalTwinTab from './components/DigitalTwinTab';
import ScoreTab from './components/ScoreTab';
import { analyzeDrug } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('mechanism');
  const [drugName, setDrugName] = useState('Montelukast');
  const [diseaseName, setDiseaseName] = useState('COPD');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleRunAnalysis = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await analyzeDrug(drugName, diseaseName);
      setResults(data);
    } catch (err) {
      setError("Failed to run analysis. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'mechanism', label: 'BioMechanism', icon: Activity },
    { id: 'literature', label: 'Literature', icon: BookOpen },
    { id: 'digital_twin', label: 'Digital Twin', icon: User },
    { id: 'score', label: 'Score', icon: Star },
  ];

  return (
    <div className="min-h-screen bg-medical-bg text-medical-text font-sans transition-colors duration-300">

      {/* Header */}
      <header className="bg-medical-surface shadow-sm border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-medical-primary/10 p-2 rounded-lg text-medical-primary">
              <Pill className="w-6 h-6" />
            </div>
            <h1 className="text-xl font-bold text-medical-primary tracking-tight">
              AstraMorph
            </h1>
          </div>
          <div className="text-sm text-medical-muted hidden sm:block font-medium">AI-Powered Drug Repurposing</div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

        {/* Input Section */}
        <section className="bg-medical-surface rounded-xl shadow-sm border border-gray-200 p-8 mb-10 max-w-4xl mx-auto">
          <h2 className="text-lg font-semibold text-medical-text mb-6">Start Analysis</h2>
          <form onSubmit={handleRunAnalysis} className="flex flex-col md:flex-row items-end gap-6">
            <div className="flex-1 w-full">
              <label className="block text-sm font-medium text-medical-muted mb-2">Drug Name</label>
              <div className="relative">
                <input
                  type="text"
                  value={drugName}
                  onChange={(e) => setDrugName(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-primary/20 focus:border-medical-primary bg-gray-50 focus:bg-white transition-all outline-none"
                  placeholder="e.g. Metformin"
                  required
                />
                <Pill className="absolute right-4 top-3.5 h-5 w-5 text-gray-400" />
              </div>
            </div>
            <div className="flex-1 w-full">
              <label className="block text-sm font-medium text-medical-muted mb-2">Disease Name</label>
              <div className="relative">
                <input
                  type="text"
                  value={diseaseName}
                  onChange={(e) => setDiseaseName(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-primary/20 focus:border-medical-primary bg-gray-50 focus:bg-white transition-all outline-none"
                  placeholder="e.g. Alzheimer's"
                  required
                />
                <Activity className="absolute right-4 top-3.5 h-5 w-5 text-gray-400" />
              </div>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full md:w-auto px-8 py-3 bg-medical-primary text-white rounded-lg font-medium hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-medical-primary disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </>
              ) : (
                <>
                  <Rocket className="w-5 h-5" />
                  Analyze
                </>
              )}
            </button>
          </form>
        </section>

        {error && (
          <div className="bg-red-50 border border-red-100 p-4 mb-8 rounded-lg max-w-4xl mx-auto flex items-center gap-3">
            <div className="bg-red-100 p-1 rounded-full">
              <X className="h-4 w-4 text-red-600" />
            </div>
            <p className="text-sm text-red-700 font-medium">{error}</p>
          </div>
        )}

        {/* Results Section */}
        <AnimatePresence>
          {results && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="max-w-5xl mx-auto"
            >
              {/* Tabs */}
              <div className="border-b border-gray-200 mb-8">
                <nav className="-mb-px flex space-x-6 overflow-x-auto" aria-label="Tabs">
                  {tabs.map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`
                                        whitespace-nowrap py-4 px-2 border-b-2 font-medium text-sm flex items-center gap-2 transition-all
                                        ${activeTab === tab.id
                          ? 'border-medical-primary text-medical-primary'
                          : 'border-transparent text-medical-muted hover:text-medical-text hover:border-gray-300'}
                                    `}
                    >
                      <tab.icon className={`w-4 h-4 ${activeTab === tab.id ? 'text-medical-primary' : 'text-gray-400'}`} />
                      {tab.label}
                    </button>
                  ))}
                </nav>
              </div>

              {/* Content */}
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className="bg-medical-surface rounded-xl shadow-sm border border-gray-200 p-8 min-h-[400px]"
              >
                {activeTab === 'mechanism' && <MechanismTab data={results.mechanism} />}
                {activeTab === 'literature' && <LiteratureTab data={results.literature} />}
                {activeTab === 'digital_twin' && <DigitalTwinTab data={results.simulation} />}
                {activeTab === 'score' && <ScoreTab data={results.score} />}
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {!results && !loading && (
          <div className="text-center py-20 opacity-60">
            <div className="bg-gray-100 w-20 h-20 rounded-full mx-auto flex items-center justify-center mb-4">
              <Pill className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-medical-text">Ready to Explore</h3>
            <p className="max-w-md mx-auto mt-2 text-medical-muted text-sm">Enter a drug and disease combination to view the mechanism, literature, digital twin simulation, and final score.</p>
          </div>
        )}

      </main>
    </div>
  );
}

export default App;
