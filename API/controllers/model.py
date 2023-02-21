from copy import deepcopy
import pandas as pd
from sklearn.metrics import confusion_matrix
from controllers.logitModified import LogitModified
from variables.variables import getFinanacialRatios, economicColumns, industryBranchColumns, nonfinancialColumns
from controllers.variables import Variables
from controllers.fileReader import FileReader
from controllers.modelParameters import ModelParameters
from controllers.file import File
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod import families
from pprint import pprint
from statsmodels.stats.outliers_influence import MLEInfluence
import numpy as np
import math
import sys


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
        self.globalBestLLR = 0

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

    def setModelParameters(self, type, corrState, usedDataState, modelType):
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
            type, corrState, usedDataState, modelType)

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
        self.analuzeInfluence()
        self.printResult()

    # def analuzeInfluence(self):
    #     influence1 = self.getInfluence(
    #         self.Best_unfittedmodel, self.Best_model)
    #     print("------------------------------Custom---------------------------------")
    #     f = open("isskirtysNumbersAndNames.txt", "w")
    #     fs = open("isskirtysNumbers.txt", "w")
    #     for i in influence1.columns:
    #         print(influence1[i].describe())
    #         rowInfluence = influence1.index[influence1[i] > 1].tolist()
    #         print(len(rowInfluence))
    #         print(rowInfluence)
    #         rowInfluence.sort()
    #         for j in rowInfluence:
    #             fs.write(f"{j}")
    #             fs.write("\n")
    #             f.write(f"{j} {self.variables.train.iloc[[j]]}")
    #             f.write("\n")

    #     print("------------------------------Custom END---------------------------------")
    #     f.close()
    #     fs.close()

    def dataPrepareModel(self, modelType):
        self.variables.train_testSplitByModelType(modelType)
        if modelType == "Financial":
            self.variables.modelColumns.remove("IsBankrupt")
            self.variables.modelColumns = list(
                set(self.getColumnsByParams()) & set(self.variables.modelColumns))
        else:
            self.variables.modelColumns.remove("Y")

    def llr(self, llnull, llf):
        return -2*(llnull-llf)

    def prsquared(self, llnull, llf):
        return 1 - llnull-llf

    def generateModel(self):
        added_columns = []
        max_LR = 0
        counter = 0
        print(self.variables.modelColumns)
        for axas in range(100):

            Best_column = None
            for i in self.variables.modelColumns:
                if i not in added_columns:
                    if not any(x in added_columns for x in self.variables.variableSpecifications.correlationRestrictions[i]):
                        checkAddedColumns = added_columns + [i]
                        checkAddedColumns.sort()
                        tempColumnLog = deepcopy(self.columnLog)
                        for tempcol in tempColumnLog:
                            tempcol.sort()
                        if checkAddedColumns not in tempColumnLog:
                            endog = self.getDependentVariableColumn()
                            exog = sm.add_constant(
                                self.variables.train[added_columns + [i]])
                            self.unfittedmodel = sm.Logit(
                                endog, exog, missing='drop', disp=0)
                            self.model = self.unfittedmodel.fit(method="bfgs")
                            self.tests.loc[i] = [
                                self.model.llr, self.model.prsquared, self.model.bic, self.model.aic, self.model.pvalues[-1]]
                            if max_LR == None:
                                max_LR = self.model.llr
                                Best_column = i
                                self.Best_unfittedmodel = self.unfittedmodel
                                self.Best_model = self.model
                            elif self.model.pvalues[-1] < 0.05:
                                if max_LR < self.model.llr:
                                    max_LR = self.model.llr
                                    Best_column = i
                                    self.Best_unfittedmodel = self.unfittedmodel
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
            deleted = False
            while True:
                stdError = 0
                indexToRemove = None
                for j in range(1, len(self.Best_model.pvalues)):
                    if (self.Best_model.pvalues[j] >= 0.05):
                        if stdError < self.Best_model.bse[j]:
                            stdError = self.Best_model.bse[j]
                            indexToRemove = j
                if indexToRemove == None:
                    break
                else:
                    added_columns.remove(
                        self.Best_model.pvalues.index[indexToRemove])
                    endog = self.getDependentVariableColumn()
                    exog = sm.add_constant(
                        self.variables.train[added_columns])
                    self.unfittedmodel = sm.Logit(
                        endog, exog, missing='drop', disp=0)
                    self.model = self.unfittedmodel.fit(method="bfgs")
                    self.Best_model = self.model
                    self.Best_unfittedmodel = self.unfittedmodel
                    max_LR = self.model.llr
                    self.columnLog.append(deepcopy(added_columns))
                    trainRes = self.formConfusionMatrix(
                        self.variables.train, added_columns)
                    testRes = self.formConfusionMatrix(
                        self.variables.test, added_columns)
                    self.modelLog.loc[counter] = [
                        self.Best_model.llr, self.Best_model.prsquared, self.Best_model.bic, self.Best_model.aic, trainRes['avgAcc'], testRes['avgAcc']]
                    counter = counter + 1
                    self.modellist.append(self.Best_model)
                    indexToRemove == None

            if (self.globalBestLLR < max_LR):
                self.globalBestLLR = max_LR
                self.globalBestModel = self.Best_model
                self.globalBest_unfittedmodel = self.Best_unfittedmodel
                self.globalBestColumns = deepcopy(added_columns)
        self.Best_model = self.globalBestModel
        added_columns = self.globalBestColumns
        self.Best_unfittedmodel = self.globalBest_unfittedmodel
        print("GETTTTTTTTTTTTTTTTING INFLUENCE")
        print("GETTTTTTTTTTTTTTTTING INFLUENCE")
        print("GETTTTTTTTTTTTTTTTING INFLUENCE")
        print("GETTTTTTTTTTTTTTTTING INFLUENCE")
        print("GETTTTTTTTTTTTTTTTING INFLUENCE")
        removeVars = []
        influence = self.Best_model.get_influence().summary_frame()
        exceptCol = ['standard_resid', 'hat_diag',
                     'dffits_internal', 'dffits', 'student_resid']
        # print("------------------------------MLEINFLUENCE---------------------------------")
        # for i in filter(lambda i: i not in exceptCol, influence.columns):
        #     print(influence[i].describe())
        #     rowInfluence = influence.index[influence[i] > 1].tolist()
        #     print(rowInfluence)
        #     print(len(rowInfluence))
        #     removeVars = removeVars + rowInfluence
        # print("------------------------------MLEINFLUENCE END---------------------------------")

    def checkIfColumnCombinationsExists(self, list):
        for i in self.columnLog:
            if set(i) == set(list):
                return True
            else:
                return False

    def getDependentVariableColumn(self):
        if self.modelParameters.modelType == "Financial":
            return self.variables.train['IsBankrupt']
        else:
            return self.variables.train['Y']

    def formConfusionMatrix(self, data, added_columns):
        significantCoef = pd.DataFrame()
        if self.modelParameters.modelType == "Financial":
            significantCoef['IsBankrupt'] = data['IsBankrupt']
        else:
            significantCoef['Y'] = data['Y']
        significantCoef[added_columns] = data[added_columns]
        result = self.Best_model.predict(significantCoef)
        result.loc[result >= 0.5] = 1
        result.loc[result < 0.5] = 0
        classification_data = pd.DataFrame()
        if self.modelParameters.modelType == "Financial":
            classification_data['true'] = data['IsBankrupt']
        else:
            classification_data['true'] = data['Y']
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
        self.tests = self.tests.sort_values(by=['LLR'], ascending=False)
        print(self.tests)
        print("--------Best Model--------")
        print(self.Best_model.summary())

    def getColumnsByParams(self):
        return self.getDataByUsedDataStateParameter() + self.getDataByModelColumnType()

    def getDataByUsedDataStateParameter(self):
        if self.modelParameters.usedDataState == "0":
            return getFinanacialRatios()
        elif self.modelParameters.usedDataState == "1":
            return getFinanacialRatios() + ["DIV_" + x for x in getFinanacialRatios()]
        elif self.modelParameters.usedDataState == "2":
            return getFinanacialRatios() + ["SUB_" + x for x in getFinanacialRatios()]
        elif self.modelParameters.usedDataState == "3":
            return getFinanacialRatios() + ["DIV_" + x for x in getFinanacialRatios()] + ["SUB_" + x for x in getFinanacialRatios()]

    def getDataByModelColumnType(self):
        if self.modelParameters.type == "type2":
            return economicColumns
        elif self.modelParameters.type == "type3":
            return economicColumns + industryBranchColumns
        elif self.modelParameters.type == "type4":
            return economicColumns + industryBranchColumns + nonfinancialColumns
        else:
            return []

    def getInfluence(self, model, fittedModel):
        rownames = self.variables.train[model.exog_names[1:]].dropna().index
        # print(model.exog)
        # print(model.endog)
        # print(model.exog_names)
        # # for i in model.exog:

        dfbetasArray = []

        for i in range(model.exog.shape[0]):
            exoglist1 = model.exog[:i]
            exoglist2 = model.exog[i+1:]
            exoglist = np.concatenate((exoglist1, exoglist2))
            endoglist1 = model.endog[:i]
            endoglist2 = model.endog[i+1:]
            endoglist = np.concatenate((endoglist1, endoglist2))
            predictionsTrue = fittedModel.predict(exoglist)
            residualsTrue = endoglist - predictionsTrue
            residualsSquaredTrue = np.square(residualsTrue)
            degrees_of_freedomTrue = fittedModel.nobs - len(fittedModel.params)
            mseTrue = np.sum(residualsSquaredTrue)/degrees_of_freedomTrue
            exog = sm.add_constant(exoglist)
            mod1 = sm.Logit(endoglist, exog, missing='drop')
            res1 = mod1.fit(disp=0, method="bfgs")
            dfbetas = []
            sumOfDiffrence = 0
            for j in range(len(res1.params)):
                numerator = fittedModel.params[j] - res1.params[j]
                sumOfDiffrence = sumOfDiffrence + numerator
                predictions = res1.predict(exoglist)
                residuals = endoglist - predictions
                residualsSquared = np.square(residuals)
                degrees_of_freedom = res1.nobs - len(res1.params)
                mse = np.sum(residualsSquared)/degrees_of_freedom

                denumerator = math.sqrt(
                    mse*np.diag(fittedModel.normalized_cov_params)[j])
                # print(
                #     f"Row {i} Column {fittedModel.params.index[j]} Dfbeta: {numerator/denumerator}")
                dfbetas.append(numerator/denumerator)
            CooksDenumerator = len(res1.params) * mseTrue
            CooksDistance = sumOfDiffrence + CooksDenumerator
            dfbetas.append(CooksDistance)
            dfbetasArray.append(dfbetas)
        resultDaraFrame = pd.DataFrame(
            dfbetasArray, columns=fittedModel.params.index.to_list() + ["CooksD"], index=rownames)
        resultDaraFrame.to_excel('export_dataframe.xlsx')
        return resultDaraFrame
