import React from 'react';
import { motion } from 'framer-motion';
import { Target, Shield, BookOpen, Activity } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const ScoreTab = ({ data }) => {
    if (!data) return <div className="p-4 text-medical-muted">No score data available.</div>;

    const { overall_repurposing_score, verdict, efficacy_score, safety_score, mechanism_confidence, literature_support_score } = data;

    const scoreData = [
        { name: 'Score', value: overall_repurposing_score },
        { name: 'Remaining', value: 100 - overall_repurposing_score },
    ];

    const COLORS = overall_repurposing_score >= 70 ? ['#0f766e', '#f1f5f9'] : // Teal for high
        overall_repurposing_score >= 50 ? ['#eab308', '#f1f5f9'] : // Yellow for mid
            ['#ef4444', '#f1f5f9']; // Red for low

    return (
        <div className="flex flex-col items-center">
            {/* Main Score Circle */}
            <div className="relative w-64 h-64 mb-8">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={scoreData}
                            cx="50%"
                            cy="50%"
                            innerRadius={80}
                            outerRadius={100}
                            startAngle={180}
                            endAngle={0}
                            paddingAngle={0}
                            dataKey="value"
                            stroke="none"
                        >
                            {scoreData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                    </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center pt-10">
                    <span className="text-6xl font-bold text-medical-text tracking-tighter">{overall_repurposing_score.toFixed(0)}</span>
                    <span className="text-xs text-medical-muted uppercase tracking-widest mt-2 font-semibold">Overall Score</span>
                </div>
            </div>

            {/* Verdict */}
            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className={`px-10 py-4 rounded-full text-lg font-bold shadow-sm mb-12 border ${overall_repurposing_score >= 70 ? 'bg-teal-50 text-teal-800 border-teal-100' :
                        overall_repurposing_score >= 50 ? 'bg-yellow-50 text-yellow-800 border-yellow-100' :
                            'bg-red-50 text-red-800 border-red-100'
                    }`}
            >
                Verdict: {verdict}
            </motion.div>

            {/* Detailed Scores */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full max-w-3xl">
                {[
                    { label: 'Efficacy Score', value: efficacy_score, icon: Activity, color: 'text-blue-600', bg: 'bg-blue-50' },
                    { label: 'Safety Score', value: safety_score, icon: Shield, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                    { label: 'Mechanism Confidence', value: mechanism_confidence, icon: Target, color: 'text-purple-600', bg: 'bg-purple-50' },
                    { label: 'Literature Support', value: literature_support_score, icon: BookOpen, color: 'text-amber-600', bg: 'bg-amber-50' },
                ].map((item, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ x: idx % 2 === 0 ? -20 : 20, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center justify-between hover:border-gray-200 transition-colors"
                    >
                        <div className="flex items-center gap-4">
                            <div className={`p-2 rounded-lg ${item.bg}`}>
                                <item.icon className={`w-5 h-5 ${item.color}`} />
                            </div>
                            <span className="font-medium text-medical-text">{item.label}</span>
                        </div>
                        <span className="font-bold text-lg text-medical-text">{item.value.toFixed(0)}</span>
                    </motion.div>
                ))}
            </div>
        </div>
    );
};

export default ScoreTab;
