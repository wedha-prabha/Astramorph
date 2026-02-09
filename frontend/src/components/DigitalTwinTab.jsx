import React from 'react';
import { motion } from 'framer-motion';
import { Users, Activity, AlertCircle } from 'lucide-react';
import LungVisualization from './LungVisualization';

const DigitalTwinTab = ({ data }) => {
    if (!data) return <div className="p-4 text-medical-muted">No simulation data available.</div>;

    const { summary, patient_sample } = data;
    const patients = patient_sample || [];

    // Calculate averages for visualization
    const avgInflammationBefore = patients.reduce((acc, curr) => acc + curr["Baseline Inflammation"], 0) / patients.length;
    const avgInflammationAfter = avgInflammationBefore - summary.avg_inflammation_reduction_pct;

    const avgFev1Before = patients.reduce((acc, curr) => acc + curr["Baseline FEV1 (%)"], 0) / patients.length;
    const avgFev1After = avgFev1Before + summary.avg_fev1_change_pct;

    return (
        <div className="space-y-8">
            {/* Metrics Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                    { label: 'Virtual Patients', value: summary.n_patients, icon: Users, color: 'text-blue-600', bg: 'bg-blue-50' },
                    { label: 'Avg Inflammation ↓', value: `${summary.avg_inflammation_reduction_pct.toFixed(1)}%`, icon: Activity, color: 'text-medical-primary', bg: 'bg-teal-50' },
                    { label: 'Avg FEV1 Gain ↑', value: `${summary.avg_fev1_change_pct.toFixed(1)}%`, icon: Activity, color: 'text-indigo-600', bg: 'bg-indigo-50' },
                    { label: 'Side Effect Rate', value: `${summary.side_effect_rate_pct.toFixed(1)}%`, icon: AlertCircle, color: 'text-amber-600', bg: 'bg-amber-50' },
                ].map((metric, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ scale: 0.95, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className="bg-white p-5 rounded-xl border border-gray-100 hover:shadow-md transition-shadow"
                    >
                        <div className={`w-10 h-10 rounded-full ${metric.bg} flex items-center justify-center mb-3`}>
                            <metric.icon className={`w-5 h-5 ${metric.color}`} />
                        </div>
                        <div className="text-2xl font-bold text-medical-text">{metric.value}</div>
                        <div className="text-xs text-medical-muted font-medium uppercase tracking-wide">{metric.label}</div>
                    </motion.div>
                ))}
            </div>

            {/* Lung Visualization Section */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
                <h3 className="text-lg font-semibold mb-8 text-center text-medical-text">Patient Response Visualization</h3>
                <LungVisualization
                    inflammationBefore={avgInflammationBefore}
                    inflammationAfter={avgInflammationAfter}
                    fev1Before={avgFev1Before}
                    fev1After={avgFev1After}
                />
            </div>

            {/* Patient Data Chart or List */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-100">
                    <h3 className="text-lg font-semibold text-medical-text">Patient Cohort Sample</h3>
                </div>
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-100">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-medical-muted uppercase tracking-wider">Subtype</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-medical-muted uppercase tracking-wider">Baseline Inflam.</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-medical-muted uppercase tracking-wider">Baseline FEV1</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-medical-muted uppercase tracking-wider">Post-Tx Inflam.</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-medical-muted uppercase tracking-wider">Post-Tx FEV1</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-50">
                            {patients.slice(0, 5).map((p, i) => (
                                <tr key={i} className="hover:bg-gray-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-medical-text">{p["Disease Subtype"]}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-medical-muted">{p["Baseline Inflammation"].toFixed(1)}%</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-medical-muted">{p["Baseline FEV1 (%)"].toFixed(1)}%</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-medical-muted">{p["Post-Treatment Inflammation"].toFixed(1)}%</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-medical-muted">{p["Post-Treatment FEV1 (%)"].toFixed(1)}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default DigitalTwinTab;
