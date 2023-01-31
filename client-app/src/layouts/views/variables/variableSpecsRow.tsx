import { Table } from "semantic-ui-react";
import { VariableSpecifications } from "../../../app/models/variableSpecs";
import { getName } from "../../../app/variables/variables";

interface Props {
    variable: VariableSpecifications
}
export default function VariableSpecsRow({ variable }: Props) {

    return (



        <Table.Row>
            <Table.Cell>{getName(variable.column)}</Table.Cell>
            {variable.missingPercent >= 20 ?
                <Table.Cell negative>{variable.missingPercent.toFixed(2)}</Table.Cell> :
                <Table.Cell>{variable.missingPercent.toFixed(2)}</Table.Cell>}
            <Table.Cell>{variable.ksstatistic.toFixed(2)}</Table.Cell>
            <Table.Cell>{variable.kspvalue.toFixed(2)}</Table.Cell>
            <Table.Cell>{variable.Conc1}</Table.Cell>
            <Table.Cell>{variable.testStatistic.toFixed(2)}</Table.Cell>
            {variable.testPValue >= 0.05 ?
                <Table.Cell negative>{variable.testPValue.toFixed(2)}</Table.Cell> :
                <Table.Cell>{variable.testPValue.toFixed(2)}</Table.Cell>}
            <Table.Cell>{variable.significance}</Table.Cell>
            <Table.Cell>{variable.singleValue.toFixed(2)}</Table.Cell>
            <Table.Cell>{variable.singleConstant.toFixed(2)}</Table.Cell>
            <Table.Cell>{variable.singleValueStatistic.toFixed(2)}</Table.Cell>
            <Table.Cell>{variable.singleConstantStatistic.toFixed(2)}</Table.Cell>
            <Table.Cell>{variable.singleValuePValue.toFixed(2)}</Table.Cell>
            <Table.Cell>{variable.singleConstantPValue.toFixed(2)}</Table.Cell>
        </Table.Row>

    )
}