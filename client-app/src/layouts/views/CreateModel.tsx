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

const fileType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

export default observer(function CreateModel() {

    const { modelStore } = useStore();
    const { generatedFile, generatedFileName, loadFile, loadVariablesSpecs, variables, setSelectedFile, selectedFile, setFileIsSelected } = modelStore;
    const [activeState, setActive] = useState("variables");


    const fileReader = new FileReader();

    const handleOnChange = (e: any) => {
        setSelectedFile(e.target.files[0]);
        setFileIsSelected(true);
    };

    const handleItemClick = (e: any, { name }: any) => setActive(name)
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
                    loadVariablesSpecs();
                    // variables.map(variable => (
                    //     console.log(variable.column)
                    // ))
                }
            };
            fileReader.readAsText(selectedFile)
        }
    };
    return (
        <Container textAlign='justified'>
            <div>
                <label className="ui icon button">
                    <i className="file icon"></i>

                    <input type="file" id="csvFileInput" onChange={handleOnChange} hidden />
                </label>

            </div>
            <Form >


                <button
                    onClick={(e) => {
                        handleOnSubmit(e);
                    }}
                >
                    IMPORT CSV
                </button>
                <button
                    onClick={handleExport}

                >
                    IMPORT CSV
                </button>
            </Form>
            <Menu tabular>
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
            </Menu>
            {variables.length > 0 ? (activeState === 'variables' ? <VariablesSpecsTable /> : <div />) : <div />}

        </Container>
    )
})