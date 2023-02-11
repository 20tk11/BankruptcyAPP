
from controllers.variableSpecification import VariableSpecification
from variables.variables import informationalColumns, profitabilityRatios, liquidityRatios, solvencyRatios, activityRatios, structureRatios, otherRatios, nonfinancialColumns, economicColumns, industryBranchColumns
from controllers.variablesSpecifications import VariablesSpecifications


class Variables:
    """
    Description
    -------
    A class used to store DataFrame with file data and perform actions with data

    ...

    Attributes
    ----------
    variables : pd.DataFrame
        DataFrame which stores data from a file
    variableSpecifications: VariableSpecifications
        Stores Specifications for data
    Methods
    -------
    setData(file)
        Set DataFrame with data from a file
    determineVariableSuitability()
        Assigns variables to groups which indicate variable suitability
    getUniqueVariableCount()
        Gets the number of unique values in DataFrame column
    prepareData()
        Prepares specific columns to analyze data, changes column data with substitutes
    analyzeVariables()
        Analyzes variables of DataFrame
    findRatioGroup()
        finds for which ratio group a variable belongs to
    """

    def __init__(self):
        self.variableSpecifications = VariablesSpecifications()
        self.variables = None

    def setData(self, dataFrame):
        """
        Description
        -------
        Sets DataFrame

        ...


        Parameters
        -------
        dataFrame: pd.DataFrame
            DataFrame that contains data from file
        """
        self.variables = dataFrame

    def determineVariableSuitability(self):
        """
        Description
        -------
        Assigns variables to groups which indicate variable suitability
        ...


        """
        for i in self.variables.columns:
            if self.variables[i].dtype in ['int64', 'float64']:
                if i not in informationalColumns:
                    self.variableSpecifications.addValidColumn(i)
                else:
                    self.variableSpecifications.addNonValidColumn(i)
            elif self.getUniqueVariableCount(i) < 3:
                self.variableSpecifications.addBoolColumn(i)
            else:
                self.variableSpecifications.addNonValidColumn(i)

    def getUniqueVariableCount(self, column):
        """
        Description
        -------
        Gets the number of unique values in DataFrame column
        ...

        Parameters 
        -------
        column: string
            DataFrame column name

        Returns
        -------
        count: int64
            number of unique values in DataFrame column
        """
        return self.variables[column].nunique()

    def prepareData(self):
        """
        Description
        -------
        Prepares specific columns to analyze data, changes column data with substitutes
        ...

        """
        for i in self.variableSpecifications.boolColumns:

            self.variables.loc[self.variables[i] == 'T', i] = 1
            self.variables.loc[self.variables[i] == 'N', i] = 0
            self.variables[i] = self.variables[i].astype('float64')
            self.variableSpecifications.addValidColumn(i)

    def analyzeVariables(self):
        """
        Description
        -------
        Analyzes variables of DataFrame
        ...

        """
        for i in self.variableSpecifications.validColumns:
            dataType = self.variables[i].dtype
            ratioGroup = self.findRatioGroup(i)
            specification = VariableSpecification(i, dataType, ratioGroup)
            self.variableSpecifications.addVariableSpecification(
                specification.toJson())

    def findRatioGroup(self, column):
        """
        Description
        -------
        Finds for which ratio group a variable belongs to
        ...

        Parameters
        -------
        column: string
            name of DataFrame column

        Returns
        -------
        RatioGroup: str
            Name of Ratio group for DataFrame column
        """
        if any(i in column for i in profitabilityRatios):
            return "Profitability"
        elif any(i in column for i in liquidityRatios):
            return "Liquidity"
        elif any(i in column for i in solvencyRatios):
            return "Solvency"
        elif any(i in column for i in activityRatios):
            return "Activity"
        elif any(i in column for i in structureRatios):
            return "Structure"
        elif any(i in column for i in otherRatios):
            return "Other"
        elif column in nonfinancialColumns:
            return "NonFinancial"
        elif column in economicColumns:
            return "Economic"
        elif column in industryBranchColumns:
            return "IndustrySector"
        elif column == "IsBankrupt":
            return "ResultVariable"
        else:
            return "NoNSpecified"
