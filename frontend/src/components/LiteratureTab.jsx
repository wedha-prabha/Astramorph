import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, AlertTriangle, FileText } from 'lucide-react';

const LiteratureTab = ({ data }) => {
    if (!data) return <div className="p-4 text-medical-muted">No literature data available.</div>;

    const { evidence, gaps, support_score } = data;

    return (
        <div className="space-y-8">

            {/* Evidence Strength Score */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-semibold text-medical-text">Evidence Strength</h3>
                    <p className="text-sm text-medical-muted">Based on analyzed studies</p>
                </div>
                <div className="flex items-center gap-4">
                    <div className="text-4xl font-bold text-medical-text">{support_score}</div>
                    <div className="h-16 w-16 rounded-full flex items-center justify-center relative">
                        <svg className="absolute w-full h-full transform -rotate-90">
                            <circle
                                cx="32"
                                cy="32"
                                r="28"
                                stroke="#f1f5f9"
                                strokeWidth="6"
                                fill="transparent"
                            />
                            <motion.circle
                                cx="32"
                                cy="32"
                                r="28"
                                stroke="currentColor"
                                strokeWidth="6"
                                fill="transparent"
                                strokeDasharray={175.9}
                                strokeDashoffset={175.9 - (175.9 * support_score) / 100}
                                className={`${support_score >= 70 ? 'text-medical-primary' : 'text-blue-400'}`}
                                transition={{ duration: 1.5, ease: "easeOut" }}
                                strokeLinecap="round"
                            />
                        </svg>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Supporting Evidence */}
                <div>
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-medical-text">
                        <BookOpen className="w-5 h-5 text-blue-500" />
                        Supporting Evidence
                    </h3>
                    <div className="space-y-4">
                        {evidence && evidence.length > 0 ? (
                            evidence.map((item, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="bg-white p-5 rounded-lg border border-gray-100 shadow-sm hover:shadow-md transition-all group"
                                >
                                    <div className="flex gap-3">
                                        <FileText className="w-5 h-5 text-medical-muted group-hover:text-medical-primary transition-colors flex-shrink-0 mt-0.5" />
                                        <p className="text-sm text-medical-text leading-relaxed">{item}</p>
                                    </div>
                                </motion.div>
                            ))
                        ) : (
                            <p className="text-medical-muted italic">No specific evidence found.</p>
                        )}
                    </div>
                </div>

                {/* Research Gaps */}
                <div>
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-medical-text">
                        <AlertTriangle className="w-5 h-5 text-amber-500" />
                        Evidence Gaps
                    </h3>
                    <div className="space-y-4">
                        {gaps && gaps.length > 0 ? (
                            gaps.map((gap, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="bg-amber-50 p-5 rounded-lg border border-amber-100"
                                >
                                    <div className="flex gap-3">
                                        <div className="h-1.5 w-1.5 rounded-full bg-amber-400 mt-2 flex-shrink-0" />
                                        <p className="text-sm text-amber-900 leading-relaxed">{gap}</p>
                                    </div>
                                </motion.div>
                            ))
                        ) : (
                            <p className="text-medical-muted italic">No significant gaps identified.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LiteratureTab;
