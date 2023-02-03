import { Divider, Table } from "semantic-ui-react";
import { useStore } from "../../../app/store/store";
import CorrelationTable from "../correlation/correlationTable";
import CoefficientRows from "./coeficientRows";
import ConstTable from "./constTable";
import ModelTable from "./modelTable";
import RatioHeader from "./ratioHeader";
import StatsRows from "./statsRows";


export default function ModelViewRemovedCorr() {
    const { modelStore } = useStore();
    const { modelResultRemovedCorr } = modelStore;
    console.log(modelResultRemovedCorr?.variables.const)
    return (
        <>
            <Table stackable>
                <Table.Header>
                    <Table.Row >
                        <Table.HeaderCell>Independent Varible</Table.HeaderCell>
                        <Table.HeaderCell textAlign='right'>Coefficients (P-Value)</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>

                <Table.Body>

                    <ConstTable variable={modelResultRemovedCorr?.variables.const} />
                    <RatioHeader variable={"Financial Ratios"} />
                    <RatioHeader variable={"Profitability Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.financial} />
                    <RatioHeader variable={"Liquidity Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.liquidity} />
                    <RatioHeader variable={"Solvency Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.solvency} />
                    <RatioHeader variable={"Activity Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.activity} />
                    <RatioHeader variable={"Structure Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.structure} />
                    <RatioHeader variable={"Other Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.other} />
                </Table.Body>
            </Table>
            <Table stackable>

                <Table.Body>
                    <RatioHeader variable={"Economic Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.economic} />
                </Table.Body>
            </Table>
            <Table stackable>

                <Table.Body>
                    <RatioHeader variable={"Sector Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.industry} />
                </Table.Body>
            </Table>
            <Table stackable>

                <Table.Body>
                    <RatioHeader variable={"Sector Ratios"} />
                    <ModelTable variable={modelResultRemovedCorr?.variables.nonfinancial} />
                </Table.Body>
            </Table>
            <Divider horizontal />
            <Table stackable>
                <Table.Body>
                    <Table.Row >
                        <Table.Cell>{"Number Of Observations"}</Table.Cell>
                        <Table.Cell textAlign='right'>
                            {modelResultRemovedCorr?.numObs}
                        </Table.Cell>
                    </Table.Row>
                    <StatsRows variable={modelResultRemovedCorr?.trainPred.nonBankruptTrue} statName={"Percentage of the model's correctly classified non-bankrupt enterprises for training data"} />
                    <StatsRows variable={modelResultRemovedCorr?.trainPred.bankruptTrue} statName={"Percentage of the model's correctly classified bankrupt enterprises for training data"} />
                    <StatsRows variable={modelResultRemovedCorr?.trainPred.avgAcc} statName={"Percentage of the model's correctly classified bankrupt and non-bankrupt enterprises for training data"} />
                    <StatsRows variable={modelResultRemovedCorr?.testPred.nonBankruptTrue} statName={"Percentage of the model's correctly classified non-bankrupt enterprises for testing data"} />
                    <StatsRows variable={modelResultRemovedCorr?.testPred.bankruptTrue} statName={"Percentage of the model's correctly classified bankrupt enterprises for testing data"} />
                    <StatsRows variable={modelResultRemovedCorr?.testPred.avgAcc} statName={"Percentage of the model's correctly classified bankrupt and non-bankrupt enterprises for testing data"} />
                    <CoefficientRows variable={modelResultRemovedCorr?.chiSquare} statName={"Chi-Square p-value"} />
                    <CoefficientRows variable={modelResultRemovedCorr?.coxSnell} statName={"Cox and Snell R-Square"} />
                    <CoefficientRows variable={modelResultRemovedCorr?.macFadden} statName={"McFadden's R-Square"} />
                    <CoefficientRows variable={modelResultRemovedCorr?.negelkerke} statName={"Negelkerke R-Square"} />
                </Table.Body>
            </Table>
            <CorrelationTable correlationData={modelResultRemovedCorr?.correlation} />
        </>
    )
}