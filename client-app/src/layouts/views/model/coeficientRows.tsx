import { Table } from "semantic-ui-react";
import { SignificatVariables, VariableSpecifications } from "../../../app/models/variableSpecs";

interface Props {
    variable: number | undefined
    statName: string | undefined
}
export default function CoefficientRows({ variable, statName }: Props) {

    return (


        <Table.Row>
            <Table.Cell>{statName}</Table.Cell>
            <Table.Cell textAlign='right'>
                {variable?.toFixed(2)}
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