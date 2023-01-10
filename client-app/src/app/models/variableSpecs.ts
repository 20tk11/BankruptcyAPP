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

export interface VariablesSpecs {
    data: Array<VariableSpecifications>
    fileName: string
}