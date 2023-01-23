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
    chiSquare: number;
    coxSnell: number;
    macFadden: number;
    negelkerke: number;
    testPred: Confusion;
    trainPred: Confusion;
    variables: VariablesByRatioTypes;
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
}