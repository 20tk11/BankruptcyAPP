import { Divider, Table } from "semantic-ui-react";
import { useStore } from "../../../app/store/store";
import CorrelationTable from "../correlation/correlationTable";
import CoefficientRows from "./coeficientRows";
import ConstTable from "./constTable";
import ModelTable from "./modelTable";
import RatioHeader from "./ratioHeader";
import StatsRows from "./statsRows";


export default function ModelView() {
    const { modelStore } = useStore();
    const { modelResult } = modelStore;
    console.log(modelResult?.variables.const)
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
                    
                    <ConstTable variable={modelResult?.variables.const} />
                    <RatioHeader variable={"Financial Ratios"} />
                    <RatioHeader variable={"Profitability Ratios"} />
                    <ModelTable variable={modelResult?.variables.financial} />
                    <RatioHeader variable={"Liquidity Ratios"} />
                    <ModelTable variable={modelResult?.variables.liquidity} />
                    <RatioHeader variable={"Solvency Ratios"} />
                    <ModelTable variable={modelResult?.variables.solvency} />
                    <RatioHeader variable={"Activity Ratios"} />
                    <ModelTable variable={modelResult?.variables.activity} />
                    <RatioHeader variable={"Structure Ratios"} />
                    <ModelTable variable={modelResult?.variables.structure} />
                    <RatioHeader variable={"Other Ratios"} />
                    <ModelTable variable={modelResult?.variables.other} />
                </Table.Body>
            </Table>
            <Table stackable>

                <Table.Body>
                    <RatioHeader variable={"Economic Ratios"} />
                    <ModelTable variable={modelResult?.variables.economic} />
                </Table.Body>
            </Table>
            <Table stackable>

                <Table.Body>
                    <RatioHeader variable={"Sector Ratios"} />
                    <ModelTable variable={modelResult?.variables.industry} />
                </Table.Body>
            </Table>
            <Table stackable>

                <Table.Body>
                    <RatioHeader variable={"Sector Ratios"} />
                    <ModelTable variable={modelResult?.variables.nonfinancial} />
                </Table.Body>
            </Table>
            <Divider horizontal />
            <Table stackable>
                <Table.Body>
                    <Table.Row >
                        <Table.Cell>{"Number Of Observations"}</Table.Cell>
                        <Table.Cell textAlign='right'>
                            {modelResult?.numObs}
                        </Table.Cell>
                    </Table.Row>
                    <StatsRows variable={modelResult?.trainPred.nonBankruptTrue} statName={"Percentage of the model's correctly classified non-bankrupt enterprises for training data"} />
                    <StatsRows variable={modelResult?.trainPred.bankruptTrue} statName={"Percentage of the model's correctly classified bankrupt enterprises for training data"} />
                    <StatsRows variable={modelResult?.trainPred.avgAcc} statName={"Percentage of the model's correctly classified bankrupt and non-bankrupt enterprises for training data"} />
                    <StatsRows variable={modelResult?.testPred.nonBankruptTrue} statName={"Percentage of the model's correctly classified non-bankrupt enterprises for testing data"} />
                    <StatsRows variable={modelResult?.testPred.bankruptTrue} statName={"Percentage of the model's correctly classified bankrupt enterprises for testing data"} />
                    <StatsRows variable={modelResult?.testPred.avgAcc} statName={"Percentage of the model's correctly classified bankrupt and non-bankrupt enterprises for testing data"} />
                    <CoefficientRows variable={modelResult?.chiSquare} statName={"Chi-Square p-value"} />
                    <CoefficientRows variable={modelResult?.coxSnell} statName={"Cox and Snell R-Square"} />
                    <CoefficientRows variable={modelResult?.macFadden} statName={"McFadden's R-Square"} />
                    <CoefficientRows variable={modelResult?.negelkerke} statName={"Negelkerke R-Square"} />
                </Table.Body>
            </Table>
            <CorrelationTable correlationData={modelResult?.correlation} />
        </>
    )
}