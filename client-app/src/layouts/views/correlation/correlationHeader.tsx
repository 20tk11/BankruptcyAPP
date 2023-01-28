import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import CorrelationHeaderCell from "./correlationHeaderCell";


interface Props {
    correlationData: CorrelationData[] | undefined;
}
export default function CorrelationHeader({ correlationData }: Props) {

    return (
        <Table.Header>
            <Table.Row>
                <Table.HeaderCell />
                {correlationData?.map((corr: CorrelationData) => (
                    <CorrelationHeaderCell corr={corr} />
                ))
                }
            </Table.Row>
        </Table.Header>
    )
}
