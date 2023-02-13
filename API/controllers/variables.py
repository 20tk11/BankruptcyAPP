
from controllers.variableSpecification import VariableSpecification
from variables.variables import informationalColumns, profitabilityRatios, liquidityRatios, solvencyRatios, activityRatios, structureRatios, otherRatios, nonfinancialColumns, economicColumns, industryBranchColumns
from controllers.variablesSpecifications import VariablesSpecifications
from scipy.stats import kstest
from scipy.stats import mannwhitneyu
import statsmodels.api as sm
import pandas as pd
from sklearn.model_selection import train_test_split


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
    ----------
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

    getMissingPercent(column) 
        find percentage of missing records in DataFrame's column

    ksTest(column) 
        Executes Kolmogorov-Smirnov test

    MWUTest(column, modelType) 
        Executes Mann-Whiteney U test

    singleLogit(column, modelType) 
        Makes a logistic regression model for each suitable DataFrame column

    MWUTestByModelType(modelType) 
        splits dependant DataFrame's column into splits of True and False (1,0)

    logitEndog(modelType, data)
        Get endog for Logistic regression depending if it is Financial or Custom logistic model

    getCorrelation()
        Iterates through Ratio groups and data groups and assigns correlation matrix for associated data and ratio group. Determines restricted variable combinations for each ratio group by the parameters inserted

    getCorrelationForRatioGroup(i, j):
        Gets correlation matrix for ratio and data group combination and forms and returns a list of dictionaries that hold a column name and a list of correlations with other columns

    getColumnCorrelation(corr_matrix):
        Forms and returns a list of dictionaries that hold a column name and a list of correlations with other columns
    """

    def __init__(self):
        self.variableSpecifications = VariablesSpecifications()
        self.variables = None
        self.train = None
        self.test = None
        self.modelColumns = []

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

    def analyzeVariables(self, modelType):
        """
        Description
        -------
        Analyzes variables of DataFrame
        ...

        """
        for i in self.variableSpecifications.validColumns:
            dataType = self.variables[i].dtype
            ratioGroup = self.findRatioGroup(i)
            missingPercent = self.getMissingPercent(i)
            ksResult = self.ksTest(i)
            mw = self.MWUTest(i, modelType)
            if mw[1] < 0.05:
                self.addModelColumn(i)
            self.variableSpecifications.addCorrelationColumn(i, ratioGroup)
            modelConstPValue, modelValuePValue, modelConstStatistic, modelValueStatistic, constant, value = self.singleLogit(
                i, modelType)
            specification = VariableSpecification(i, dataType, ratioGroup, missingPercent, ksResult[0], ksResult[1],
                                                  mw[0], mw[1], value, constant, modelValueStatistic, modelConstStatistic,
                                                  modelValuePValue, modelConstPValue)
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

    def getMissingPercent(self, column):
        """
        Description
        -------
        find percentage of missing records in DataFrame's column
        ...

        Parameters
        -------
        column: string
            name of DataFrame column

        Returns
        -------
        missingPercentage: float64
            Percentage of missing records
        """
        return self.variables[column].isna().sum() * 100 / len(self.variables)

    def ksTest(self, column):
        """
        Description
        -------
        Kolmogorov-Smirnov test
        ...

        Parameters
        -------
        column: string
            name of DataFrame column

        Returns
        -------
        ksTest: [float64, float64] 
            Kolmogorov-Smirnov test Statistic and p-value
        """
        return kstest(self.variables[column].dropna(), 'norm')

    def MWUTest(self, column, modelType):
        """
        Description
        -------
        Mann-Whitney U test
        ...

        Parameters
        -------
        column: string
            name of DataFrame column
        modelType: string -> ['Financial', 'Custom']
            Model type that is being generated

        Returns
        -------
        mwUtest: [float64, float64] 
            Mann-Whitney U test Statistic and p-value
        """
        IsBankrupt_Not, IsBankrupt_Yes = self.MWUTestByModelType(modelType)
        return mannwhitneyu(
            x=IsBankrupt_Yes[column].dropna(), y=IsBankrupt_Not[column].dropna(), alternative='two-sided')

    def singleLogit(self, column, modelType):
        """
        Description
        -------
        Single factor logistic regression
        ...

        Parameters
        -------
        column: string
            name of DataFrame column
        modelType: string -> ['Financial', 'Custom']
            Model type that is being generated

        Returns
        -------
        constantPValue: float64
            Single Factor logistic regression model's significance p-value for column
        valuePValue: float64
            Single Factor logistic regression model's significance p-value for column
        constantStatistic: float64
            Single Factor logistic regression model's significance statistic for column
        valueStatistic: float64
            Single Factor logistic regression model's significance statistic for column
        constant: float64
            Single Factor logistic regression model's coefficient for constant
        value: float64
            Single Factor logistic regression model's coefficient for column
        """
        if "IsBankrupt" == column:
            return "nan", "nan", "nan", "nan", "nan", "nan"
        dftemp = self.variables.dropna(subset=[column])
        exog = sm.add_constant(dftemp[column])
        endog = self.logitEndog(modelType, dftemp)
        model = sm.Logit(endog, exog, missing='drop').fit(
            method="bfgs", maxiter=100)
        constantPValue = model.pvalues[0]
        valuePValue = model.pvalues[1]
        constantStatistic = model.tvalues[0]
        valueStatistic = model.tvalues[1]
        constant = model.params[0]
        value = model.params[1]
        return constantPValue, valuePValue, constantStatistic, valueStatistic, constant, value

    def MWUTestByModelType(self, modelType):
        """
        Description
        -------
        Splits dependant DataFrame's column into splits of True and False (1,0) There is possibility to make different types of models and in this case data is splitted by different column: Financial model has dependent column IsBankrupt and for Custom the dependent column is Y
        ...

        Parameters
        -------
        modelType: string -> ['Financial', 'Custom']
            Model type that is being generated

        Returns
        -------
        IsBankrupt_Not: DataFrame
            Data split for True dependent values
        IsBankrupt_Yes: DataFrame
            Data split for False dependent values
        """
        if modelType == "Financial":
            IsBankrupt_Not = self.variables[self.variables['IsBankrupt'] == 0]
            IsBankrupt_Yes = self.variables[self.variables['IsBankrupt'] == 1]
        elif modelType == "Custom":
            IsBankrupt_Not = self.variables[self.variables['Y'] == 0]
            IsBankrupt_Yes = self.variables[self.variables['Y'] == 1]
        return IsBankrupt_Not, IsBankrupt_Yes

    def logitEndog(self, modelType, data):
        """
        Description
        -------
        Assigns dependent value column for use in logistic regression model. Depending of what logistic regression model is created DataFrame columns will be different.
        ...

        Parameters
        -------
        modelType: string -> ['Financial', 'Custom']
            Model type that is being generated
        data:
            DataFrame with removed nan values from independent column

        Returns
        -------
        endog: DataFrame
            DataFrame with one column either IsBankrupt or Y column
        """
        if modelType == "Financial":
            endog = data['IsBankrupt']
        elif modelType == "Custom":
            endog = data['Y']
        return endog

    def getCorrelation(self):
        """
        Description
        -------
        Iterates through Ratio groups and data groups and assigns correlation matrix for associated data and ratio group. Determines restricted variable combinations for each ratio group by the parameters inserted
        ...
        """
        for i in self.variableSpecifications.columnCorrelations:
            ratioGroupColumns = []
            for j in self.variableSpecifications.columnCorrelations[i]:
                columns = self.variableSpecifications.columnCorrelations[i][j]
                self.variableSpecifications.addColumnCorrelationMatrix(
                    i+j, self.getCorrelationForRatioGroup(columns, 0))
                ratioGroupColumns = ratioGroupColumns + columns
            self.getCorrelationForRatioGroup(ratioGroupColumns, 1)

    def getCorrelationForRatioGroup(self, column, corrRestriction):
        """
        Description
        -------
        Gets correlation matrix for ratio and data group combination and forms and returns a list of dictionaries that hold a column name and a list of correlations with other columns

        Parameters
        -------
        column: str
            column variable

        corrRestriction: int64
            indicates if method used to find correlation restrictions or correlation matrix 

        Returns
        -------
        correlation: Dictionary list -> [{column: column, correlations: [columnCorrelation, column_1Correlation, ..., column_nCorrelation]},...,{column_n, correlations: [columnCorrelation, column_1Correlation, ..., column_nCorrelation]}]
            a list of dictionaries for each column's correlation with other columns
        ...
        """
        corr_matrix = self.getCorrelationMatrix(column)
        return self.getColumnCorrelation(corr_matrix, corrRestriction)

    def getCorrelationMatrix(self, column):
        """
        Description
        -------
        Gets correlation matrix DataFrame

        Parameters
        -------
        column: str
            column variable

        Returns
        -------
        correlation: DataFrame
            a DataFrame each column's correlation with other columns
        ...
        """
        correlation = pd.DataFrame()
        correlation[column] = self.variables[column]
        correlation = correlation.dropna()
        return correlation.corr()

    def getColumnCorrelation(self, corr_matrix, corrRestriction):
        """
        Description
        -------
        Forms and returns a list of dictionaries that hold a column name and a list of correlations with other columns or forms correlations restrictions dictionary
        ...

        Parameters
        -------
        corr_matrix: DataFrame
            A DataFrame containing correlation between columns of same data group and ratio groups

        corrRestriction: int64
            indicates if method used to find correlation restrictions or correlation matrix 

        Returns
        -------
        correlation: Dictionary list -> [{column: column, correlations: [columnCorrelation, column_1Correlation, ..., column_nCorrelation]},...,{column_n, correlations: [columnCorrelation, column_1Correlation, ..., column_nCorrelation]}]
            a list of dictionaries for each column's correlation with other columns
        """

        for k in range(len(corr_matrix.values)):
            colCorrelation = []
            if corrRestriction == 0:
                colCorrelation.append(
                    {"column": corr_matrix.columns[k], "correlations": corr_matrix.values[k].tolist()})
            else:
                for i in range(len(corr_matrix.values)):
                    if abs(corr_matrix.values[k][i]) >= 0.7:
                        colCorrelation.append(corr_matrix.columns[i])
                self.variableSpecifications.addCorrelationRestriction(
                    corr_matrix.columns[k], colCorrelation)
        if corrRestriction == 0:
            return colCorrelation

    def train_testSplitByModelType(self, modelType):
        if modelType == "Financial":
            self.train_testSplit("IsBankrupt")
        else:
            self.train_testSplit("Y")

    def train_testSplit(self, dependantColumn):
        self.train, self.test = train_test_split(
            self.variables, test_size=0.2, random_state=42, stratify=self.variables[dependantColumn])

    def addModelColumn(self, column):
        self.modelColumns.append(column)
