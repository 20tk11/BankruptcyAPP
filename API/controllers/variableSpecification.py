class VariableSpecification:
    """
    Description
    -------
    A class Object for storing DataFrame column's specification

    ...

    Attributes
    ----------
    name: str
        name of DataFrame's column
    dataType: str
        type of data stored in DataFrame column
    ratioGroup: str
        Ratio group that DataFrame's column belongs to
    missingPercent: float64
        number of missing nan records in dataset
    ksStatistic: float64
        Kolmogorov-Smirnov test Statistic value
    ksPValue: float64
        Kolmogorov-Smirnov test p-value
    suitabilityStatistic: float64
        Mann-Whitney U or t-test Statistic value
    suitabilityPValue: float64
        Mann-Whitney U or t-test p-value
    coefficientValue: float64
        single factor logistic regression value coefficient
    coefficientConstant: float64
        single factor logistic regression constant coefficient
    statisticValue: float64
        single factor logistic regression value significance Statistic value
    statisticConstant: float64
        single factor logistic regression constant significance Statistic value
    PValueValue: float64
        single factor logistic regression value significance p-value
    PValueConstant: float64
        single factor logistic regression constant significance p-value
    testType: str
        Test type used after Kolmogorov-Smirnov test
    significance: str
        Indicates if data's column is significant for the model    
    Methods
    -------
    toJson()
        gets dictionary type object formed from VariableSpecification
    """

    def __init__(self, name, dataType, ratioGroup, missingPercent, ksStatistic,
                 ksPValue, suitabilityStatistic, suitabilityPValue, coefficientValue,
                 coefficientConstant, statisticValue, statisticConstant, PValueValue,
                 PValueConstant):
        self.name = name
        self.dataType = dataType
        self.ratioGroup = ratioGroup
        self.missingPercent = missingPercent
        self.ksStatistic = ksStatistic
        self.ksPValue = ksPValue
        self.testType = self.getTestType(ksPValue)
        self.suitabilityStatistic = suitabilityStatistic
        self.suitabilityPValue = suitabilityPValue
        self.significance = self.getSignificance(suitabilityPValue)
        self.coefficientValue = float(coefficientValue)
        self.coefficientConstant = float(coefficientConstant)
        self.statisticValue = float(statisticValue)
        self.statisticConstant = float(statisticConstant)
        self.PValueValue = float(PValueValue)
        self.PValueConstant = float(PValueConstant)

    def toJson(self):
        """
        Description
        -------
        gets dictionary type object formed from VariableSpecification
        ...

        Returns
        ----------
        dict: Dictionary
            Dictionary type object of VariableSpecification
        """
        return {"name": self.name, "dataType": str(self.dataType), "ratioGroup": self.ratioGroup,
                "missingPercent": self.missingPercent, "ksStatistic": self.ksStatistic, "ksPValue": self.ksPValue,
                "suitabilityStatistic": self.suitabilityStatistic, "suitabilityPValue": self.suitabilityPValue,
                "coefficientValue": self.coefficientValue, "coefficientConstant": self.coefficientConstant,
                "statisticValue": self.statisticValue, "statisticConstant": self.statisticConstant, "PValueValue": self.PValueValue,
                "PValueConstant": self.PValueConstant, "significance": self.significance, "testType": self.testType}

    def getTestType(self, ksPValue):
        """
        Description
        -------
        gets what test to use after Kolmogorov-Smirnof test
        ...

        Returns
        ----------
        test: str
            return "Mann-Whitney U Test" or "T=Test" test type
        """
        if (ksPValue < 0.05):
            return "Mann-Whitney U Test"
        else:
            return "T=Test"

    def getSignificance(self, suitabilityPValue):
        """
        Description
        -------
        gets if the DataFrame's column is significant
        ...

        Returns
        ----------
        significance: str
            returns if DataFrame's column is Significant or Non Significant
        """
        if (suitabilityPValue < 0.05):
            return "Significant"
        else:
            return "Non Significant"
