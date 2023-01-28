import { Table } from "semantic-ui-react";
import { useStore } from "../../../app/store/store";
import VariableSpecsRow from "./variableSpecsRow";


export default function VariablesSpecsTable() {
    const { modelStore } = useStore();
    const { variables } = modelStore;

    return (
        <Table celled>
            <Table.Header >
                <Table.Row>
                    <Table.HeaderCell>Variable Name</Table.HeaderCell>
                    <Table.HeaderCell>Missing values, %</Table.HeaderCell>
                    <Table.HeaderCell>Kolmogorov Smirnov Statistic</Table.HeaderCell>
                    <Table.HeaderCell>Kolmogorov Smirnov P-Value</Table.HeaderCell>
                    <Table.HeaderCell>Test For Relation</Table.HeaderCell>
                    <Table.HeaderCell>Statistic</Table.HeaderCell>
                    <Table.HeaderCell>P-Value</Table.HeaderCell>
                    <Table.HeaderCell>Significance</Table.HeaderCell>
                    <Table.HeaderCell>Value Coefficient</Table.HeaderCell>
                    <Table.HeaderCell>Constant Coefficient</Table.HeaderCell>
                    <Table.HeaderCell>Value Statistic</Table.HeaderCell>
                    <Table.HeaderCell>Constant Statistic</Table.HeaderCell>
                    <Table.HeaderCell>Value PValue</Table.HeaderCell>
                    <Table.HeaderCell>Constant PValue</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            <Table.Body className="tableScroll">
                {variables.map(variable => (
                    <VariableSpecsRow key={variable.column} variable={variable} />
                ))}
            </Table.Body>
        </Table>
    )
}