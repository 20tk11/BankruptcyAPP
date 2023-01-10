import React, { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Button, Container, Dropdown, Icon, Menu, Segment, Table } from "semantic-ui-react";
import csvToJson from 'csvtojson';
import Papa from "papaparse";
import axios from "axios";
import agent from "../../app/api/agent";
import { useStore } from "../../app/store/store";
import { observer } from "mobx-react-lite";
import { toJS } from "mobx";
import VariablesSpecsTable from "./variables/variablesSpecsTable";
import saveAs from "file-saver";

const fileType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

export default observer(function CreateModel() {

    const { modelStore } = useStore();
    const { generatedFile, generatedFileName, loadFile, loadVariablesSpecs, variables, setSelectedFile, selectedFile, setFileIsSelected } = modelStore;



    const fileReader = new FileReader();

    const handleOnChange = (e: any) => {
        setSelectedFile(e.target.files[0]);
        setFileIsSelected(true);
    };


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
            <div style={{ textAlign: "center" }}>
                <h1>REACTJS CSV IMPORT EXAMPLE </h1>
                <form>
                    <input
                        type={"file"}
                        id={"csvFileInput"}
                        accept={".csv"}
                        onChange={handleOnChange}
                    />

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
                </form>
            </div>
            <VariablesSpecsTable />
        </Container>
    )
})