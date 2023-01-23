import { Table } from "semantic-ui-react";
import { SignificatVariables, VariableSpecifications } from "../../../app/models/variableSpecs";

interface Props {
    variable: string
}
export default function RatioHeader({ variable }: Props) {

    return (

        <>
            <Table.Row>
                <Table.Cell colSpan='2'><b>{variable}</b></Table.Cell>

            </Table.Row>
        </>
        // <Table.Row>
        //     <Table.Cell>{variable.variable}</Table.Cell>
        //     <Table.Cell>
        //         {variable.coefficient}<br />
        //         ({variable.significance})
        //     </Table.Cell>
        // </Table.Row><b>{value}</b>

    )
}