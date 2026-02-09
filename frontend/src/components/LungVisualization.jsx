import React from 'react';
import { motion } from 'framer-motion';

const LungVisualization = ({ inflammationBefore, inflammationAfter, fev1Before, fev1After }) => {

    return (
        <div className="flex flex-col md:flex-row justify-center items-center gap-16 py-10">
            {/* Before State */}
            <div className="text-center relative group">
                <div className="mb-6">
                    <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-semibold uppercase tracking-wider rounded-full">Before Treatment</span>
                </div>
                <div className="relative w-48 h-48 mx-auto transition-transform group-hover:scale-105 duration-300">
                    {/* SVG Lung Shape */}
                    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-xl">
                        <path d="M30,30 Q20,50 30,80 Q40,90 50,80 Q60,90 70,80 Q80,50 70,30 Q50,10 30,30 Z" fill="#ffe4e6" />
                        <motion.path
                            d="M30,30 Q20,50 30,80 Q40,90 50,80 Q60,90 70,80 Q80,50 70,30 Q50,10 30,30 Z"
                            fill="#ef4444"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: inflammationBefore / 100 }}
                            transition={{ duration: 1 }}
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-3xl font-bold text-white drop-shadow-md">{fev1Before.toFixed(1)}%</span>
                        <span className="text-xs text-white drop-shadow-md font-medium">FEV1</span>
                    </div>
                </div>
                <div className="mt-6 space-y-2">
                    <p className="text-sm font-semibold text-medical-accent bg-red-50 inline-block px-3 py-1 rounded-md">Inflammation: {inflammationBefore.toFixed(0)}%</p>
                </div>
            </div>

            {/* Arrow */}
            <div className="flex flex-col items-center relative z-10">
                <div className="w-px h-12 bg-gray-200 mb-2 md:hidden"></div>
                <motion.div
                    initial={{ x: -10, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.5, duration: 0.5 }}
                    className="text-medical-primary bg-teal-50 p-3 rounded-full border border-teal-100"
                >
                    <svg className="w-6 h-6 transform rotate-90 md:rotate-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                    </svg>
                </motion.div>
            </div>

            {/* After State */}
            <div className="text-center relative group">
                <div className="mb-6">
                    <span className="px-3 py-1 bg-teal-50 text-medical-primary text-xs font-semibold uppercase tracking-wider rounded-full">After Treatment</span>
                </div>
                <div className="relative w-48 h-48 mx-auto transition-transform group-hover:scale-105 duration-300">
                    {/* SVG Lung Shape */}
                    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-xl">
                        <path d="M30,30 Q20,50 30,80 Q40,90 50,80 Q60,90 70,80 Q80,50 70,30 Q50,10 30,30 Z" fill="#ffe4e6" />
                        <motion.path
                            d="M30,30 Q20,50 30,80 Q40,90 50,80 Q60,90 70,80 Q80,50 70,30 Q50,10 30,30 Z"
                            fill="#ef4444"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: inflammationAfter / 100 }}
                            transition={{ duration: 1, delay: 0.2 }}
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-3xl font-bold text-white drop-shadow-md">{fev1After.toFixed(1)}%</span>
                        <span className="text-xs text-white drop-shadow-md font-medium">FEV1</span>
                    </div>
                </div>
                <div className="mt-6 space-y-2">
                    <p className="text-sm font-semibold text-medical-primary bg-teal-50 inline-block px-3 py-1 rounded-md">Inflammation: {inflammationAfter.toFixed(0)}%</p>
                </div>
            </div>
        </div>
    );
};

export default LungVisualization;
