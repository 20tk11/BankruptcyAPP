
import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import CorrelationHeader from "./correlationHeader";


interface Props {
    label: string;
}
export default function CorrelationTableBodyRowName({ label }: Props) {

    return (
        <Table.Cell>{label}</Table.Cell>



    )

}
