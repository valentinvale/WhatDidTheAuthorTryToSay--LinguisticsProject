import axios from 'axios';

export const predict_t5_small = async (text) => {
    try{
        const response = await axios.post("http://localhost:5000/predict_t5_small", {
            text: text,
        });
        return response.data;
    }
    catch(e){
        console.log(e);
    }
    
};

export const predict_t5_base = async (text) => {
    try{
        const response = await axios.post("http://localhost:5000/predict_t5_base", {
            text: text,
        });
        return response.data;
    }
    catch(e){
        console.log(e);
    }
};