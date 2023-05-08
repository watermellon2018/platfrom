import axios from 'axios';

export const login = async (values) => {

    try {
        const res = await axios.get("http://127.0.0.1:8005/health/login/",
            {params: values});
        return res.data;
    } catch (err) {
        throw err.response.data;
    }
};

