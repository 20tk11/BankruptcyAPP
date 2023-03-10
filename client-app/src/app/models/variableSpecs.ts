export interface VariableSpecifications {
    column: string;
    missingPercent: number;
    ksstatistic: number;
    kspvalue: number;
    Conc1: string;
    testStatistic: number;
    testPValue: number;
    significance: string;
    singleValue: number;
    singleConstant: number;
    singleValueStatistic: number;
    singleConstantStatistic: number;
    singleValuePValue: number;
    singleConstantPValue: number;
}

export interface Result {
    numObs: number;
    chiSquare: number;
    coxSnell: number;
    macFadden: number;
    negelkerke: number;
    testPred: Confusion;
    trainPred: Confusion;
    variables: VariablesByRatioTypes;
    correlation: Array<CorrelationData>;

}
export interface Confusion {
    avgAcc: number;
    bankruptTrue: number;
    nonBankruptTrue: number;
}
export interface VariablesSpecs {
    data: Array<VariableSpecifications>
    fileName: string
    result: Result;
    correalation: Correalation;
    removedCorrModel: Result;
}
export interface SignificatVariables {
    coefficient: number;
    significance: number;
    variable: string;
}

export interface VariablesByRatioTypes {
    activity: Array<SignificatVariables>;
    financial: Array<SignificatVariables>;
    liquidity: Array<SignificatVariables>;
    other: Array<SignificatVariables>;
    solvency: Array<SignificatVariables>;
    structure: Array<SignificatVariables>;
    const: SignificatVariables;
    economic: Array<SignificatVariables>;
    industry: Array<SignificatVariables>;
    nonfinancial: Array<SignificatVariables>;
}
export interface Correalation {
    activity: Array<CorrelationData>;
    economic: Array<CorrelationData>;
    financial: Array<CorrelationData>;
    industry: Array<CorrelationData>;
    liquidity: Array<CorrelationData>;
    nonfinancial: Array<CorrelationData>;
    other: Array<CorrelationData>;
    solvency: Array<CorrelationData>;
    structure: Array<CorrelationData>;
}

export interface CorrelationData {
    column: string;
    correlations: Array<number>;
}