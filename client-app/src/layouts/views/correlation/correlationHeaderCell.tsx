import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";

interface Props {
    corr: CorrelationData;
}
export default function CorrelationHeaderCell({ corr }: Props) {

    return (

        <Table.HeaderCell>
            {corr.column}
        </Table.HeaderCell>

    )
}
