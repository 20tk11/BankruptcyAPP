import { Divider, Table } from "semantic-ui-react";
import { useStore } from "../../../app/store/store";



export default function CorrelationView() {
    const { modelStore } = useStore();
    const { modelResult } = modelStore;
    console.log(modelResult?.variables.const)
    Dosmth();
    function Dosmth() {
        
    }
    return (
        <>
            <Table stackable>
                <Table.Header>
                    <Table.Row >
                        <Table.HeaderCell>Independent Varible</Table.HeaderCell>
                        <Table.HeaderCell textAlign='right'>Coefficients (P-Value)</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>

            </Table>
        </>
    )
}