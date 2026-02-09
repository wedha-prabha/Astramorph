import React from 'react';
import { motion } from 'framer-motion';
import { Target, CheckCircle, Activity, Info } from 'lucide-react';

const MechanismTab = ({ data }) => {
    if (!data) return <div className="p-4 text-medical-muted">No mechanism data available.</div>;

    const { summary, steps, targets, confidence } = data;

    return (
        <div className="space-y-8">
            {/* Summary Section */}
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-medical-secondary/50 p-6 rounded-lg border border-medical-secondary"
            >
                <div className="flex items-start gap-4">
                    <div className="bg-white p-2 rounded-full shadow-sm">
                        <Info className="w-5 h-5 text-medical-primary" />
                    </div>
                    <div>
                        <h3 className="font-semibold text-medical-primary mb-2">Mechanism Summary</h3>
                        <p className="text-medical-text text-sm leading-relaxed">{summary}</p>
                    </div>
                </div>
            </motion.div>

            {/* Steps Section */}
            <div>
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-medical-text">
                    <Activity className="w-5 h-5 text-medical-primary" />
                    Mechanistic Steps
                </h3>
                <div className="space-y-4">
                    {steps && steps.map((step, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="flex gap-5 p-4 bg-white rounded-lg border border-gray-100 hover:border-medical-secondary transition-all shadow-sm"
                        >
                            <span className="flex-shrink-0 w-8 h-8 rounded-full bg-medical-secondary text-medical-primary flex items-center justify-center font-bold text-sm">
                                {index + 1}
                            </span>
                            <p className="text-medical-text text-sm pt-1.5 leading-relaxed">{step}</p>
                        </motion.div>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Targets Section */}
                <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-medical-text">
                        <Target className="w-5 h-5 text-medical-accent" />
                        Molecular Targets
                    </h3>
                    <div className="flex flex-wrap gap-2">
                        {targets && targets.length > 0 ? (
                            targets.map((target, idx) => (
                                <span key={idx} className="bg-red-50 text-red-700 px-3 py-1.5 rounded-md text-sm font-medium border border-red-100">
                                    {target}
                                </span>
                            ))
                        ) : (
                            <p className="text-medical-muted text-sm italic">No targets identified.</p>
                        )}
                    </div>
                </div>

                {/* Confidence Section */}
                <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-medical-text">
                        <CheckCircle className="w-5 h-5 text-medical-primary" />
                        Confidence Level
                    </h3>
                    <div className="relative pt-2">
                        <div className="bg-gray-100 rounded-full h-3 w-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${confidence}%` }}
                                transition={{ duration: 1, ease: "easeOut" }}
                                className={`h-full ${confidence >= 70 ? 'bg-medical-primary' : confidence >= 50 ? 'bg-yellow-500' : 'bg-medical-accent'}`}
                            />
                        </div>
                        <div className="flex justify-between text-xs font-medium mt-2 text-medical-muted">
                            <span>Low</span>
                            <span>High</span>
                        </div>
                    </div>
                    <div className="text-right text-2xl font-bold mt-2 text-medical-text">
                        {confidence}%
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MechanismTab;
