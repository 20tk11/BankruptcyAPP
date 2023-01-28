
import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import CorrelationHeader from "./correlationHeader";
import CorrelationTableBodyRowName from "./correlationTableBodyRowName";


interface Props {
    corr: CorrelationData;
}
export default function CorrelationBodyRow({ corr }: Props) {

    return (
        <Table.Row>
            <CorrelationTableBodyRowName label={corr.column} />
            {corr.correlations.map((data: number) => (
                <Table.Cell bgcolor={'red'}>
                    {data.toFixed(2)}
                </Table.Cell>
            ))}
        </Table.Row>


    )

}
