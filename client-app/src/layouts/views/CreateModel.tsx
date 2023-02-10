import React, { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Button, Container, Dropdown, Form, Icon, Label, Menu, Segment, Table } from "semantic-ui-react";
import csvToJson from 'csvtojson';
import Papa from "papaparse";
import axios from "axios";
import agent from "../../app/api/agent";
import { useStore } from "../../app/store/store";
import { observer } from "mobx-react-lite";
import { toJS } from "mobx";
import VariablesSpecsTable from "./variables/variablesSpecsTable";
import saveAs from "file-saver";
import { act } from "@testing-library/react";
import ModelView from "./model/modelView";
import CorrelationView from "./correlation/correlationView";
import ModelViewRemovedCorr from "./model/modelViewRemovedCorr";

const fileType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

const options = [
    { key: "0", text: 'None Correlation', value: "0" },
    { key: "1", text: 'Grouped Correlation', value: "1" },
    { key: "2", text: 'Full Correlation', value: "2" },
]
const options1 = [
    { key: "0", text: 'Normal', value: "0" },
    { key: "1", text: 'Normal + Divided', value: "1" },
    { key: "2", text: 'Normal + Subtracted', value: "2" },
    { key: "3", text: 'Normal + Subtracted + Divided', value: "3" },
]
export default observer(function CreateModel() {

    const { modelStore } = useStore();
    const { generatedFile, generatedFileName, loadFile, loadVariablesSpecs, variables, setSelectedFile, selectedFile, setFileIsSelected, isFilePicked } = modelStore;
    const [activeState, setActive] = useState("variables");
    const [checkboxState, setcheckboxState] = useState<string>("type1");
    const [correlationState, setcorrelationState] = useState<string>("0");
    const [usedDataState, setusedDataState] = useState<string>("0");
    const [fileName, setfileName] = useState<string>("Select file")
    const fileReader = new FileReader();

    const handleOnChange = (e: any) => {
        console.log(e.target.files[0].name)
        setfileName(e.target.files[0].name)
        setSelectedFile(e.target.files[0]);
        setFileIsSelected(true);
    };

    const handleItemClick = (e: any, { name }: any) => setActive(name)
    const handleCorrelationChange = (e: any, { value }: any) => {
        console.log(value)
        setcorrelationState(value)
    }
    const handleUsedDataChange = (e: any, { value }: any) => {
        console.log(value)
        setusedDataState(value)
    }
    const handleCheckBoxChange = (e: any, { value }: any) => {
        console.log(value)
        setcheckboxState(value)
    }
    function handleExport() {
        saveAs("http://192.168.8.177:5000/file/" + generatedFileName, generatedFileName + ".xlsx")
    }
    useEffect(() => {
        // variables.map(variable => (
        //     // console.log(variable.column)
        // ))
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [variables])



    // variables.map(variable => (
    //     // console.log(variable.column)
    // ))
    // eslint-disable-next-line react-hooks/exhaustive-deps

    const handleOnSubmit = (e: any) => {
        e.preventDefault();
        if (selectedFile) {
            fileReader.onload = function (event) {
                if (event.target) {
                    loadVariablesSpecs(checkboxState, correlationState, usedDataState, "Financial");
                    // variables.map(variable => (
                    //     console.log(variable.column)
                    // ))
                }
            };
            fileReader.readAsText(selectedFile)
        }
    };
    function TableSwitch() {
        if (variables.length > 0) {
            console.log(activeState)
            if (activeState === 'variables') {
                return <VariablesSpecsTable />;
            }
            else if (activeState === 'model') {
                return <ModelView />;
            }
            else if (activeState === "correlation") {
                return <CorrelationView />;
            }
            else if (activeState === 'modelAfterCorr') {
                return <ModelViewRemovedCorr />
            }
        }
        return <div />;
    }
    return (
        <Container textAlign='justified' >

            <Form >

                <Form>
                    <div className="inlineForm" >
                        <label className="ui icon button">
                            <i className="file icon"></i>
                            {fileName}
                            <input type="file" id="csvFileInput" onChange={handleOnChange} hidden />
                        </label>

                    </div>
                    <Form.Select
                        fluid
                        width={5}
                        label='Correlation'
                        onChange={handleCorrelationChange}
                        options={options}
                        value={correlationState}

                    />
                    <Form.Select
                        fluid
                        width={5}
                        label='Used Data'
                        value={usedDataState}
                        onChange={handleUsedDataChange}
                        options={options1}
                    />
                    <Form.Group inline>

                        <label>Data Groups Uses</label>
                        <Form.Radio
                            label='Type 1'
                            value='type1'
                            checked={checkboxState === 'type1'}
                            onChange={handleCheckBoxChange}
                        />
                        <Form.Radio
                            label='Type 2'
                            value='type2'
                            checked={checkboxState === 'type2'}
                            onChange={handleCheckBoxChange}
                        />
                        <Form.Radio
                            label='Type 3'
                            value='type3'
                            checked={checkboxState === 'type3'}
                            onChange={handleCheckBoxChange}
                        />
                        <Form.Radio
                            label='Type 4'
                            value='type4'
                            checked={checkboxState === 'type4'}
                            onChange={handleCheckBoxChange}
                        />
                    </Form.Group>
                    <Button
                        onClick={handleOnSubmit}
                        disabled={!isFilePicked}
                    >
                        Generate Model
                    </Button>
                </Form>

            </Form>
            {variables.length > 0 ? (<Menu tabular>
                <Menu.Item
                    name='variables'
                    active={activeState === 'variables'}
                    onClick={handleItemClick}
                />
                <Menu.Item
                    name='correlation'
                    active={activeState === 'correlation'}
                    onClick={handleItemClick}
                />
                <Menu.Item
                    name='model'
                    active={activeState === 'model'}
                    onClick={handleItemClick}
                />
                <Menu.Item
                    name='modelAfterCorr'
                    active={activeState === 'modelAfterCorr'}
                    onClick={handleItemClick}
                />
            </Menu>) : <></>}
            <TableSwitch />

        </Container>
    )
})