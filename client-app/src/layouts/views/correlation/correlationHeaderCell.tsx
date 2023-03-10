import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import { getName } from "../../../app/variables/variables";

interface Props {
    corr: CorrelationData;
}
export default function CorrelationHeaderCell({ corr }: Props) {

    return (

        <Table.HeaderCell>
            {getName(corr.column)}
        </Table.HeaderCell>

    )
}
