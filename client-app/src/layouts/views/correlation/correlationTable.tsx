import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import CorrelationBodyRow from "./correlationBodyRow";
import CorrelationHeader from "./correlationHeader";
import CorrelationTableBody from "./correlationTableBody";


interface Props {
    correlationData: CorrelationData[] | undefined;
}
export default function CorrelationTable({ correlationData }: Props) {

    return (
        <Table definition>
            <CorrelationHeader correlationData={correlationData} />

            <CorrelationTableBody correlationData={correlationData} />
        </Table >
    )

}
