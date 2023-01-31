
import { Divider, Table } from "semantic-ui-react";
import { Correalation, CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import { getName } from "../../../app/variables/variables";
import CorrelationHeader from "./correlationHeader";
import CorrelationTableBodyRowName from "./correlationTableBodyRowName";
import CorrelationTableBodyRowValue from "./correlationTableBodyRowValue";


interface Props {
    correlationData: CorrelationData[] | undefined;
}
export default function CorrelationTableBody({ correlationData }: Props) {

    return (
        <Table.Body>
            {correlationData?.map((corr: CorrelationData) => (
                <Table.Row>
                    <CorrelationTableBodyRowName label={getName(corr.column)} />
                    {corr.correlations.map((data: number) => (
                        <CorrelationTableBodyRowValue data={data} />
                    ))}
                </Table.Row>
            ))
            }

        </Table.Body>

    )

}
