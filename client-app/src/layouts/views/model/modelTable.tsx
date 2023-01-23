import { Table } from "semantic-ui-react";
import { SignificatVariables, VariableSpecifications } from "../../../app/models/variableSpecs";

interface Props {
    variable: SignificatVariables[] | undefined
}
export default function ModelTable({ variable }: Props) {

    return (

        <>
            {variable ?
                variable.map((variable: SignificatVariables) => (
                    <Table.Row >
                        <Table.Cell>{variable.variable}</Table.Cell>
                        <Table.Cell textAlign='right'>
                            {variable.coefficient.toFixed(2)}<br />
                            ({variable.significance.toFixed(2)})
                        </Table.Cell>
                    </Table.Row>
                ))
                : <div>NONE</div>}
        </>
        // <Table.Row>
        //     <Table.Cell>{variable.variable}</Table.Cell>
        //     <Table.Cell>
        //         {variable.coefficient}<br />
        //         ({variable.significance})
        //     </Table.Cell>
        // </Table.Row>

    )
}