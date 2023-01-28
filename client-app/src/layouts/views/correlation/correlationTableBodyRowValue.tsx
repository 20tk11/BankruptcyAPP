import { match } from "assert";
import { redirect } from "react-router-dom";
import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import CorrelationHeader from "./correlationHeader";




interface Props {
    data: number;
}
export default function CorrelationTableBodyRowValue({ data }: Props) {

    const setColor = () => {
        if (Math.abs(data) >= 0.9) {
            return 'red'
        }
        else if (Math.abs(data) >= 0.7) {
            return 'orange'
        }
        else if (Math.abs(data) >= 0.5) {
            return 'yellow'
        }
        else if (Math.abs(data) >= 0.3) {
            return 'chartreuse'
        }
        else {
            return 'lime'
        }
    };


    return (
        <Table.Cell bgcolor={setColor()}>
            {data.toFixed(3)}
        </Table.Cell >

    )

}
