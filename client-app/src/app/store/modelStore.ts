import { makeAutoObservable } from "mobx";
import agent from "../api/agent";
import { VariableSpecifications } from "../models/variableSpecs";

export default class ModelStore {
    variableRegistry = new Map<string, VariableSpecifications>();
    loading = false;
    loadingInitial = false;
    selectedFile = null
    isFilePicked = false
    generatedFileName = null
    generatedFile = null

    constructor() {
        makeAutoObservable(this)
    }

    get variables() {
        return Array.from(this.variableRegistry.values());
    }
    get generateFile() {
        console.log(this.generatedFile)
        return this.generatedFile;
    }

    loadVariablesSpecs = async (type: string) => {
        console.log(type)
        const formData = new FormData();
        if (this.selectedFile) {
            formData.append("file", this.selectedFile);
            formData.append("type", type);
        }
        this.setLoadingInitial(true);
        try {
            if (this.variableRegistry.size > 0) {
                this.variableRegistry.clear();
            }
            const variables = await agent.VariableSpecs.specs(formData)
            console.log(variables);
            this.setGeneratedFileName(variables.fileName)
            variables.data.forEach(element => {
                this.setVariable(element.column, element)
            })
            console.log(this.variableRegistry)
            console.log(this.generatedFileName)
            this.setLoadingInitial(false);
        } catch (error) {
            console.log(error);
            this.setLoadingInitial(false);
        }
    }
    loadFile = async () => {
        this.setLoadingInitial(true);
        try {
            if (this.generatedFileName) {
                const variables = await agent.VariableSpecs.file(this.generatedFileName)
                this.setGeneratedFile(variables)
            }
            this.setLoadingInitial(false);
        } catch (error) {
            console.log(error);
            this.setLoadingInitial(false);
        }
    }
    setLoadingInitial = (state: boolean) => {
        this.loadingInitial = state;
    }
    private setVariable = (name: string, variable: VariableSpecifications) => {
        this.variableRegistry.set(name, variable);
    }

    setSelectedFile = (file: any) => {
        this.selectedFile = file;
    }
    setFileIsSelected = (state: boolean) => {
        this.isFilePicked = state;
    }
    setGeneratedFileName = (fileName: any) => {
        this.generatedFileName = fileName;
    }
    setGeneratedFile = (file: any) => {
        this.generatedFile = file;
    }
}