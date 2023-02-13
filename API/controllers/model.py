from copy import deepcopy
import pandas as pd
from sklearn.metrics import confusion_matrix
from controllers.variables import Variables
from controllers.fileReader import FileReader
from controllers.modelParameters import ModelParameters
from controllers.file import File
import statsmodels.api as sm


class Model:
    """
    Description
    -------
    A class used to store Logistic regression model and to train it.

    Here Variables and VariableSpecifications are stored
        Access methods and variables of other classes

    ...

    Attributes
    ----------
    file : File
        file of types: json, csv, xlsx
    modelParameters: ModelParameters
        Model parameters for model Object
    variables: Variables
        Storing of Data and specifications of the data

    Methods
    -------
    setFile(file)
        Set file containing data
    setModelParameters(type, corrState, modelType, usedDataState)
        Set parameters for model by which the model will be generated
    read()
        read file into a DataFrame
    analyzeVariables()
        Uses to analyze variables in the dataset, get correlation matrix for all data groups and ratio groups 
    """

    def __init__(self):
        self.file = File()
        self.modelParameters = ModelParameters()
        self.variables = Variables()
        self.tests = pd.DataFrame(
            columns=['LLR', 'prsquared', 'aic', 'bic', 'p-value'])
        self.Best_model = None
        self.columnLog = []
        self.modelLog = pd.DataFrame(
            columns=['LLR', 'prsquared', 'aic', 'bic', 'trainPred', 'testPred'])
        self.modellist = []

    def setFile(self, file):
        """
        Description
        -------
        Set file containing data

        Parameters
        ----------
        file : werkzeug.datastructures.FileStorage
            file of types: json, csv, xlsx
        """
        return self.file.setFile(file)

    def setModelParameters(self, type, corrState, modelType, usedDataState):
        """
        Description
        -------
        Set parameters for model by which the model will be generated

        Parameters
        ----------
        type : str
            parameter which describes which types of data to use when creating an model
        corrState : str
            parameter which describes what kind of correlation requirement to use when choosing variables to add into the model
        modelType : str
            parameter which describes to generate a model from financial data or custom
        usedDataState : str
            parameter which describes if to use bonus variables in the model: Divided and Subtracted
        """
        self.modelParameters.setModelParameters(
            type, corrState, modelType, usedDataState)

    def read(self):
        """
        Description
        -------
        Sets DataFrame to Variables Object

        Returns
        -------
        Status Code
            informs that reading the file caused an error
        """
        try:
            self.variables.setData(FileReader.read(self.file))
        except Exception as e:
            print(e)
            return 400

    def analyzeVariables(self):
        """
        Description
        -------
        Uses to analyze variables in the dataset, get correlation matrix for all data groups and ratio groups 
        """
        self.variables.analyzeVariables(self.modelParameters.modelType)
        self.variables.getCorrelation()
        self.dataPrepareModel(self.modelParameters.modelType)
        self.generateModel()
        self.printResult()

    def dataPrepareModel(self, modelType):
        self.variables.train_testSplitByModelType(modelType)

    def generateModel(self):
        added_columns = []
        max_LR = 0
        counter = 0
        # while True:
        for z in range(2):
            Best_column = None
            for i in self.variables.modelColumns:
                if i not in added_columns:
                    if len(set(added_columns).intersection(self.variables.modelColumns)) > 0:
                        endog = self.getDependentVariableColumn()
                        exog = sm.add_constant(
                            self.variables.train[added_columns + [i]])
                        self.model = sm.Logit(endog, exog, missing='drop').fit(
                            method="bfgs")
                        self.tests.loc[i] = [
                            self.model.llr, self.model.prsquared, self.model.bic, self.model.aic, self.model.pvalues[-1]]
                        if max_LR == None:
                            max_LR = self.model.llr
                            Best_column = i
                            self.Best_model = self.model
                        elif self.model.pvalues[-1] < 0.05:
                            if max_LR < self.model.llr:
                                max_LR = self.model.llr
                                Best_column = i
                                self.Best_model = self.model
            if (Best_column == None):
                break
            added_columns.append(Best_column)
            self.columnLog.append(deepcopy(added_columns))
            trainRes = self.formConfusionMatrix(
                self.variables.train, added_columns)
            testRes = self.formConfusionMatrix(
                self.variables.test, added_columns)
            self.modelLog.loc[counter] = [
                self.Best_model.llr, self.Best_model.prsquared, self.Best_model.bic, self.Best_model.aic, trainRes['avgAcc'], testRes['avgAcc']]
            counter = counter + 1
            self.modellist.append(self.Best_model)

    def getDependentVariableColumn(self):
        if self.modelParameters.modelType == "Financial":
            return self.variables.train['IsBankrupt']
        else:
            return self.variables.train['Y']

    def formConfusionMatrix(self, data, added_columns):
        significantCoef = pd.DataFrame()
        significantCoef['IsBankrupt'] = data['IsBankrupt']
        significantCoef[added_columns] = data[added_columns]
        result = self.Best_model.predict(significantCoef)
        result.loc[result >= 0.5] = 1
        result.loc[result < 0.5] = 0
        classification_data = pd.DataFrame()
        classification_data['true'] = data['IsBankrupt']
        classification_data['pred'] = result
        classification_data = classification_data.dropna()
        classification_data = classification_data.astype(int)
        confusion_matrix(
            classification_data['true'], classification_data['pred'])
        Tnonbancruptcy = confusion_matrix(classification_data['true'], classification_data['pred'])[
            0][0] / len(classification_data.loc[classification_data['true'] == 0]) * 100
        Tbancruptcy = confusion_matrix(classification_data['true'], classification_data['pred'])[
            1][1] / len(classification_data.loc[classification_data['true'] == 1]) * 100
        Tboth = (confusion_matrix(classification_data['true'], classification_data['pred'])[
            1][1] + confusion_matrix(classification_data['true'], classification_data['pred'])[0][0]) / len(classification_data) * 100
        return {"nonBankruptTrue": Tnonbancruptcy, "bankruptTrue": Tbancruptcy, "avgAcc": Tboth}

    def printResult(self):
        print("--------Model Log--------")
        print(self.modelLog)
        print("--------Column Log--------")
        for i in self.columnLog:
            print(i)
        print("--------Column Stat--------")
        print(self.tests)
