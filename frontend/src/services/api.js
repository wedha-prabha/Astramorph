import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const analyzeDrug = async (drugName, diseaseName) => {
    try {
        const response = await axios.post(`${API_URL}/analyze`, {
            drug_name: drugName,
            disease_name: diseaseName,
        });
        return response.data;
    } catch (error) {
        console.error("Error analyzing drug:", error);
        throw error;
    }
};
