import axios, { AxiosResponse } from "axios"
import { VariableSpecifications, VariablesSpecs } from "./../models/variableSpecs"

const sleep = (delay: number) => {
    return new Promise((resolve) => {
        setTimeout(resolve, delay)
    })
}

axios.defaults.baseURL = 'http://192.168.8.177:5000';

axios.interceptors.response.use(async response => {
    try {
        await sleep(1000);
        return response;

    } catch (error) {
        console.log(error);
        return await Promise.reject(error);
    }
})

const responseBody = <T>(response: AxiosResponse<T>) => response.data;

const requests = {
    post: <T>(url: string, body: {}) => axios.post<T>(url, body).then(responseBody),
    get: (url: string) => axios.get(url).then(responseBody),
}

const VariableSpecs = {
    specs: (formData: FormData) => requests.post<VariablesSpecs>('/logit', formData),
    file: (fileName: string) => requests.get(`/file/${fileName}`),
}

const agent = {
    VariableSpecs
}

export default agent;