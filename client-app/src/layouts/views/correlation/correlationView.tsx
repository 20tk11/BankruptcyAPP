import { Divider, Table } from "semantic-ui-react";
import { CorrelationData } from "../../../app/models/variableSpecs";
import { useStore } from "../../../app/store/store";
import CorrelationTable from "./correlationTable";



export default function CorrelationView() {
    const { modelStore } = useStore();
    const { correlationResult } = modelStore;


    return (
        <>
            <CorrelationTable correlationData={correlationResult?.financial} />
            <CorrelationTable correlationData={correlationResult?.liquidity} />
            <CorrelationTable correlationData={correlationResult?.solvency} />
            <CorrelationTable correlationData={correlationResult?.activity} />
            <CorrelationTable correlationData={correlationResult?.structure} />
            <CorrelationTable correlationData={correlationResult?.other} />
            <CorrelationTable correlationData={correlationResult?.nonfinancial} />
            <CorrelationTable correlationData={correlationResult?.economic} />
            <CorrelationTable correlationData={correlationResult?.industry} />
        </>
    )

}
