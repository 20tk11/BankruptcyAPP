import { Table } from "semantic-ui-react";
import { SignificatVariables, VariableSpecifications } from "../../../app/models/variableSpecs";
import { getName } from "../../../app/variables/variables";

interface Props {
    variable: number | undefined
    statName: string
}
export default function StatsRows({ variable, statName }: Props) {

    return (


        <Table.Row >
            <Table.Cell>{statName}</Table.Cell>
            <Table.Cell textAlign='right'>
                {variable?.toFixed(2)} %
            </Table.Cell>
        </Table.Row>

        // <Table.Row>
        //     <Table.Cell>{variable.variable}</Table.Cell>
        //     <Table.Cell>
        //         {variable.coefficient}<br />
        //         ({variable.significance})
        //     </Table.Cell>
        // </Table.Row>

    )
}