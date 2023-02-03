import math
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import xlsxwriter
from scipy.stats import kstest
from scipy.stats import mannwhitneyu
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from variables.variables import getColumns, getColumnsByType, findRatioGroup, getFinancialColumns, getActivityColumns, getBranchColumns, getEconomicColumns, getLiquidityColumns, getNonFinancialColumns, getOtherColumns, getSolvencyColumns, getStructureColumns
from copy import deepcopy
import sys
import numpy
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
sys.float_info.epsilon


class Variables():

    def __init__(self):
        self.variables = pd.DataFrame()

    def readCSV(self, file):
        self.variables = pd.read_csv(file)

    def readXLSX(self, file):
        self.variables = pd.read_excel(file)

    def readJSON(self, file):
        self.variables = pd.read_json(file)

    def setDataframe(self, file, filesuffix):
        return self.readByFormat(file, filesuffix)

    def readByFormat(self, file, filesuffix):
        if filesuffix == "csv":
            self.readCSV(file)
            return True
        elif filesuffix == "xlsx":
            self.readXLSX(file)
            return True
        elif filesuffix == "json":
            self.readJSON(file)
            return True
        else:
            return False

    def changeValues(self):
        self.variables['Audit'] = self.variables['Audit'].replace(['T', 'N'], [
                                                                  1, 0])
        self.variables['SingleShareholder'] = self.variables['SingleShareholder'].replace([
                                                                                          'T', 'N'], [1, 0])

    def getMissingPercent(self, column):
        return self.variables[column].isna().sum() * 100 / len(self.variables)

    def kolmogorovSmirnovTest(self, column):
        print(column)
        return kstest(self.variables[column].dropna(), 'norm')

    def mannWhitneyUTest(self, column):
        IsBankrupt_Not = self.variables[self.variables['IsBankrupt'] == 0]
        IsBankrupt_Yes = self.variables[self.variables['IsBankrupt'] == 1]
        return mannwhitneyu(
            x=IsBankrupt_Yes[column].dropna(), y=IsBankrupt_Not[column].dropna(), alternative='two-sided')

    def singleLogit(self, column):
        if ("IsBankrupt" == column):
            return 0, 0, 0, 0, 0, 0
        dftemp = self.variables.dropna(subset=[column])
        exog = sm.add_constant(dftemp[column])
        endog = dftemp['IsBankrupt']
        model = sm.Logit(endog, exog, missing='drop').fit(
            method="bfgs", maxiter=100)
        constantPValue = model.pvalues[0]
        valuePValue = model.pvalues[1]
        constantStatistic = model.tvalues[0]
        valueStatistic = model.tvalues[1]
        constant = model.params[0]
        value = model.params[1]

        return constantPValue, valuePValue, constantStatistic, valueStatistic, constant, value

    # Filter columns that are not needed in the reggresion - fix problem with sm.Logit for getting string values
    def analyzeVariables(self, type):
        self.changeValues()
        self.variableSpec = []
        self.significantVariables = []
        variables = getColumnsByType(type, "A")
        for i in np.intersect1d(self.variables.columns, getColumns()):
            missingPercent = self.getMissingPercent(i)
            ksResult = self.kolmogorovSmirnovTest(i)
            mannWhitney = self.mannWhitneyUTest(i)
            modelConstPValue, modelValuePValue, modelConstStatistic, modelValueStatistic, constant, value = self.singleLogit(
                i)
            if (mannWhitney[1] < 0.05 and i in variables):
                self.significantVariables.append(i)
            variableSpecs = VariableSpecifications(
                i, missingPercent, ksResult[0], ksResult[1], mannWhitney[0], mannWhitney[1], value, constant,
                modelValueStatistic, modelConstStatistic, modelValuePValue, modelConstPValue).getJson()

            self.variableSpec.append(variableSpecs)

    def getExcel(self):
        excelGen = ExcelGenerator()
        return excelGen.generateExcel(self.variableSpec)

    def getVariableStats(self):
        return self.variableSpec

    def getSignificant(self):
        return self.significantVariables

    def getVariables(self):
        return self.variables

    def setCorrelation(self):
        self.correlationRestrictions = {}
        financial = self.getCorrelationByRatioType(
            getFinancialColumns())
        liquidity = self.getCorrelationByRatioType(
            getLiquidityColumns())
        solvency = self.getCorrelationByRatioType(
            getSolvencyColumns())
        activity = self.getCorrelationByRatioType(
            getActivityColumns())
        structure = self.getCorrelationByRatioType(
            getStructureColumns())
        other = self.getCorrelationByRatioType(getOtherColumns())
        nonfinancial = self.getCorrelationByRatioType(
            getNonFinancialColumns())
        economic = self.getCorrelationByRatioType(
            getEconomicColumns())
        industry = self.getCorrelationByRatioType(getBranchColumns())
        self.correlation = {"financial": financial, "liquidity": liquidity, "solvency": solvency,
                            "activity": activity, "structure": structure, "other": other, "nonfinancial": nonfinancial,
                            "economic": economic, "industry": industry}

    def getCorrelation(self):
        return self.correlation

    def getCorrelationByRatioType(self, columns):
        correlation = pd.DataFrame()
        for i in np.intersect1d(columns, self.variables.columns):
            correlation[i] = self.variables[i]
        correlation = correlation.dropna()
        corr_matrix = correlation.corr()
        corr_result = self.getCorrForObject(corr_matrix)
        print(corr_result)
        return corr_result

    def getCorrelationForResult(self, columns, data):
        correlation = pd.DataFrame()
        for i in columns:
            correlation[i] = data[i]
        correlation = correlation.dropna()
        corr_matrix = correlation.corr()
        corr_result = self.getCorrForObject(corr_matrix)
        print(corr_result)
        return corr_result

    def getCorrForObject(self, corr_matrix):
        columnCorrelation = []
        for i in range(len(corr_matrix.values)):
            cor = {"column": corr_matrix.columns[i],
                   "correlations": corr_matrix.values[i].tolist()}
            columnCorrelation.append(cor)
        return columnCorrelation

    def getCorrelationForModel(self, corr_matrix):
        columnCorrelation = []
        for i in range(len(corr_matrix.values)):
            cor = {"column": corr_matrix.columns[i],
                   "correlations": corr_matrix.values[i].tolist()}
            columnCorrelation.append(cor)

    def getCorrelationRestrictions(self):
        return self.correlationRestrictions

    def getRestrictions(self, column):
        return self.correlationRestrictions[column]

    def setCorrelationRestrictions(self, data, type):
        self.correlationRestrictions = {}
        if (type == '0'):
            self.setRestrictionsForAllVariables(
                data, self.getSignificant(), type)
        if (type == '1'):
            self.setRestrictionsForAllVariables(data,
                                                getFinancialColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getLiquidityColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getSolvencyColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getActivityColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getStructureColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getOtherColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getNonFinancialColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getEconomicColumns(), type)
            self.setRestrictionsForAllVariables(data,
                                                getBranchColumns(), type)
        if (type == '2'):
            self.setRestrictionsForAllVariables(data,
                                                self.getSignificant(), type)
        return 1

    def corrRestrictionsSpecified(self, column, corrRe):
        if column == 'I.1.10':
            corrRe.append('I.1.11')
        if column == 'I.1.11':
            corrRe.append('I.1.10')
        if column == 'I.1.20':
            corrRe.append('I.1.21')
        if column == 'I.1.21':
            corrRe.append('I.1.20')
        if column == 'I.1.30':
            corrRe.append('I.1.31')
        if column == 'I.1.31':
            corrRe.append('I.1.30')
        if column == 'I.2.10':
            corrRe.append('I.2.20')
            corrRe.append('I.2.30')
        if column == 'I.2.20':
            corrRe.append('I.2.10')
            corrRe.append('I.2.30')
        if column == 'I.2.30':
            corrRe.append('I.2.20')
            corrRe.append('I.2.10')
        if column == 'II.2.10':
            corrRe.append('II.2.11')
        if column == 'II.2.11':
            corrRe.append('II.2.10')
        if column == 'III.1.10':
            corrRe.append('III.1.11')
        if column == 'III.1.11':
            corrRe.append('III.1.10')
        if column == 'III.1.20':
            corrRe.append('III.1.21')
        if column == 'III.1.21':
            corrRe.append('III.1.20')
        if column == 'III.1.30':
            corrRe.append('III.1.31')
        if column == 'III.1.31':
            corrRe.append('III.1.30')
        if column == 'III.1.40':
            corrRe.append('III.1.41')
        if column == 'III.1.41':
            corrRe.append('III.1.40')
        if column == 'III.2.10':
            corrRe.append('III.2.11')
        if column == 'III.2.11':
            corrRe.append('III.2.10')
        if column == 'III.3.10':
            corrRe.append('III.3.11')
        if column == 'III.3.11':
            corrRe.append('III.3.10')

    def setRestrictionsForAllVariables(self, data, columns, type):

        if (type == '0'):
            for i in columns:
                corrRe = [i]
                self.corrRestrictionsSpecified(i, corrRe)
                self.correlationRestrictions[i] = corrRe
        else:
            correlation = pd.DataFrame()
            correlation[columns] = data[columns]
            correlation = correlation.dropna()
            corr_matrix = correlation.corr()
            for i in range(len(corr_matrix.values)):
                corrRe = []
                for j in range(len(corr_matrix.values[i].tolist())):
                    if corr_matrix.values[i][j] >= 0.7 or corr_matrix.values[i][j] <= -0.7:
                        corrRe.append(corr_matrix.columns[j])
                self.corrRestrictionsSpecified(i, corrRe)
                self.correlationRestrictions[corr_matrix.columns[i]] = corrRe


class VariableSpecifications:

    def __init__(self, variableName, missingPercent, ksstatistic, kspvalue, testStatistic, testPValue,
                 singleValue, singleConstant, singleValueStatistic, singleConstantStatistic, singleValuePValue, singleConstantPValue):
        self.variableName = variableName
        self.missingPercent = float(missingPercent)
        self.ksstatistic = float(ksstatistic)
        self.kspvalue = float(kspvalue)
        if (self.kspvalue < 0.05):
            self.ksResults = "Mann-Whitney U Test"
        else:
            self.ksResults = "T=Test"
        self.testStatistic = float(testStatistic)
        self.testPValue = float(testPValue)
        if (self.testPValue < 0.05):
            self.testResults = "Significant"
        else:
            self.testResults = "Non Significant"
        self.singleValue = float(singleValue)
        self.singleConstant = float(singleConstant)
        self.singleValueStatistic = float(singleValueStatistic)
        self.singleConstantStatistic = float(singleConstantStatistic)
        self.singleValuePValue = float(singleValuePValue)
        self.singleConstantPValue = float(singleConstantPValue)

    def getJson(self):
        return {"column": self.variableName, "missingPercent": self.missingPercent,
                "ksstatistic": self.ksstatistic, "kspvalue": self.kspvalue, "Conc1": self.ksResults,
                "testStatistic": self.testStatistic, "testPValue": self.testPValue, "significance": self.testResults,
                "singleValue": self.singleValue, "singleConstant": self.singleConstant, "singleValueStatistic": self.singleValueStatistic,
                "singleConstantStatistic": self.singleConstantStatistic, "singleValuePValue": self.singleValuePValue, "singleConstantPValue": self.singleConstantPValue}


class Model:

    def __init__(self):
        self.variables = Variables()

    def readFile(self, file):
        self.variables.setDataframe(file, file.filename.rsplit('.', 1)[-1])

    def analyzeModelVariables(self, type):
        self.variables.analyzeVariables(type)

    def getVariableStats(self):
        return self.variables.getVariableStats()

    def setDataSplits(self):
        self.train, self.test = train_test_split(
            self.variables.getVariables(), test_size=0.2, random_state=42, stratify=self.variables.getVariables()['IsBankrupt'])

    # 0 -> Variables assigned to models are not valued by correlation
    # 1 -> Variables assigned to models are valued by group correlation
    # 2 -> Variables assigned to models are valued by all correlations
    def setCorrelationRestrictionType(self, corrType):
        self.corrRestrictionType = corrType

    # 0 -> Normal Variables
    # 1 -> Normal + Divided
    # 2 -> Normal + Subtracted
    # 3 -> Normal + Divided + Subtracted
    def setUsedFinancialColumns(self, usedFinCol):
        self.usedFinCol = usedFinCol

    def getModel(self):
        self.globalBestLLR = 0
        self.added_columns = []
        self.tests = pd.DataFrame(
            columns=['LLR', 'prsquared', 'aic', 'bic', 'p-value'])
        self.max_LR = None
        self.modellist = []
        self.modelLog = pd.DataFrame(
            columns=['LLR', 'prsquared', 'aic', 'bic', 'trainPred', 'testPred'])
        self.Best_model = None
        self.columnLog = []

        counter = 0

        while True:
            Best_column = None
            for column in self.variables.getSignificant():
                if column not in self.added_columns:
                    if not any(x in self.added_columns for x in self.variables.getRestrictions(column)):
                        checkAddedColumns = self.added_columns + [column]
                        checkAddedColumns.sort()
                        tempColumnLog = deepcopy(self.columnLog)
                        for tempcol in tempColumnLog:
                            tempcol.sort()
                        if checkAddedColumns not in tempColumnLog:
                            endog = self.train['IsBankrupt']
                            if len(self.added_columns) == 0:
                                exog = sm.add_constant(self.train[column])
                            else:
                                exog = sm.add_constant(
                                    self.train[self.added_columns + [column]])
                            self.model = sm.Logit(endog, exog, missing='drop').fit(
                                method="bfgs")
                            # print(self.model.summary())
                            self.tests.loc[column] = [
                                self.model.llr, self.model.prsquared, self.model.bic, self.model.aic, self.model.pvalues[-1]]
                            if self.max_LR == None:
                                self.max_LR = self.model.llr
                                Best_column = column
                                self.Best_model = self.model
                            elif self.model.pvalues[-1] < 0.05:
                                if self.max_LR < self.model.llr:
                                    self.max_LR = self.model.llr
                                    Best_column = column
                                    self.Best_model = self.model
            if (Best_column == None):
                break
            self.added_columns.append(Best_column)
            self.columnLog.append(deepcopy(self.added_columns))
            trainRes = self.formConfusionMatrix(self.train)
            testRes = self.formConfusionMatrix(self.test)
            self.modelLog.loc[counter] = [
                self.Best_model.llr, self.Best_model.prsquared, self.Best_model.bic, self.Best_model.aic, trainRes['avgAcc'], testRes['avgAcc']]
            counter = counter + 1
            self.modellist.append(self.Best_model)
            # print(self.Best_model.summary())
            deleted = False
            while True:
                for j in range(1, len(self.Best_model.pvalues)):
                    if (self.Best_model.pvalues[j] >= 0.05):
                        print(self.Best_model.pvalues[j])
                        print(self.Best_model.pvalues.index[j])
                        self.added_columns.remove(
                            self.Best_model.pvalues.index[j])
                        endog = self.train['IsBankrupt']
                        exog = sm.add_constant(
                            self.train[self.added_columns])
                        self.model = sm.Logit(endog, exog, missing='drop').fit(
                            method="bfgs")
                        self.Best_model = self.model
                        self.max_LR = self.model.llr
                        self.columnLog.append(deepcopy(self.added_columns))
                        self.modelLog.loc[counter] = [
                            self.Best_model.llr, self.Best_model.prsquared, self.Best_model.bic, self.Best_model.aic, trainRes['avgAcc'], testRes['avgAcc']]
                        counter = counter + 1
                        self.modellist.append(self.Best_model)
                        deleted = True
                        break
                    else:
                        deleted = False
                if not deleted:
                    break
            if (self.globalBestLLR < self.max_LR):
                self.globalBestLLR = self.max_LR
                self.globalBestModel = self.Best_model
                self.globalBestColumns = deepcopy(self.added_columns)
        self.Best_model = self.globalBestModel
        # print(self.globalBestColumns)
        self.added_columns = self.globalBestColumns
        self.getInfluence()
        endog = self.train['IsBankrupt']
        exog = sm.add_constant(
            self.train[self.globalBestColumns])
        self.model = sm.Logit(endog, exog, missing='drop').fit(
            method="bfgs")
        recursionCounter = 0

        print(self.model.summary())
        if (any(isLarger >= 0.05 for isLarger in self.model.pvalues)):
            recursionCounter = self.getModel() + 1
        # print(self.added_columns)
        # print(self.Best_model.summary())
        self.Best_model = self.model
        return recursionCounter

    def formSignificantVariables(self):
        return findRatioGroup(self.Best_model)

    def getInfluence(self):
        while True:
            removeVars = []
            model1 = sm.OLS(self.train['IsBankrupt'], sm.add_constant(
                self.train[self.globalBestColumns]), missing='drop').fit()
            influence = model1.get_influence().summary_frame()
            exceptCol = ['standard_resid', 'hat_diag',
                         'dffits_internal', 'cooks_d', 'dffits', 'student_resid']
            for i in filter(lambda i: i not in exceptCol, influence.columns):
                print(influence[i].describe())
                rowInfluence = influence.index[influence[i] > 1].tolist()
                print(rowInfluence)
                removeVars = removeVars + rowInfluence
            # print("----------------------------")
            # print(self.train)
            if len(removeVars) < 1:
                break
            tempDataFrame = self.train.drop(
                removeVars, inplace=False)
            # print(influence.head())
            # print(influence.columns)
            # print(removeVars)
            # print(self.train)
            # print(tempDataFrame)
            # print("----------------------------")
            self.train = tempDataFrame

    def formConfusionMatrix(self, data):
        significantCoef = pd.DataFrame()
        significantCoef['IsBankrupt'] = data['IsBankrupt']
        significantCoef[self.added_columns] = data[self.added_columns]
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

    def removeCorFromFinal(self, correlated):
        maxstd = 0
        maxstdCol = None
        correlatedColumns = correlated
        if (len(correlatedColumns) < 1):
            return 1
        print(self.Best_model.bse[correlatedColumns])
        for i in correlatedColumns:
            if (self.Best_model.bse[i] > maxstd):
                maxstd = self.Best_model.bse[i]
                maxstdCol = i
        print(self.added_columns)
        self.added_columns.remove(maxstdCol)
        print(self.added_columns)
        print(maxstd)
        print(maxstdCol)
        endog = self.train['IsBankrupt']
        exog = sm.add_constant(
            self.train[self.added_columns])
        self.model = sm.Logit(endog, exog, missing='drop').fit(
            method="bfgs")
        self.Best_model = self.model
        print(self.Best_model.bse)
        correlatedTemp = self.variables.getCorrelationForResult(
            self.added_columns, self.train)
        self.removeCorrFromModel(correlatedTemp)

    def getCoxSnell(self):
        coxSnell = 1 - math.exp((self.Best_model.llnull -
                                 self.Best_model.llf)*(2/self.Best_model.nobs))
        return coxSnell

    def getNegelkerke(self, CS):
        RsqNE = CS / \
            (1-math.exp((2*self.Best_model.llnull)/self.Best_model.nobs))
        return RsqNE

    def getMcFadden(self):
        return self.Best_model.prsquared

    def getChiSquare(self):
        return self.Best_model.llr_pvalue

    def getResult(self):
        variables = self.formSignificantVariables()

        confusionMatrixTrainData = self.formConfusionMatrix(self.train)
        confusionMatrixTestData = self.formConfusionMatrix(self.test)

        CS = self.getCoxSnell()
        Negel = self.getNegelkerke(CS)
        MF = self.getMcFadden()
        ChiSq = self.getChiSquare()

        correlation = self.variables.getCorrelationForResult(
            self.added_columns, self.train)

        return {"variables": variables, "trainPred": confusionMatrixTrainData,
                "testPred": confusionMatrixTestData, "coxSnell": CS, "negelkerke": Negel,
                "macFadden": MF, "chiSquare": ChiSq, "numObs": self.Best_model.nobs, "correlation": correlation}

    def removeCorrFromModel(self, correlation):
        correlated = set()
        for i in range(len(correlation)):
            for j in range(len(correlation[i]["correlations"])):
                if (correlation[i]["column"] != correlation[j]["column"]):
                    if (abs(correlation[i]["correlations"][j]) >= 0.7):
                        correlated.add(correlation[j]["column"])
        self.removeCorFromFinal(correlated)

    def compareLR(self, column):
        if self.max_LR == None:
            self.max_LR = self.model.llr
            Best_column = column
            self.Best_model = self.model
        elif self.model.pvalues[-1] < 0.05:
            if self.max_LR < self.model.llr:
                self.max_LR = self.model.llr
                Best_column = column
                self.Best_model = self.model
        return Best_column

    def displayHistory(self):
        print("---ModelList---")
        print(self.modelLog)
        print("---Column Log---")
        for i in self.columnLog:

            print(i)
        print("---Test Log---")
        self.tests = self.tests.sort_values(by=['LLR'], ascending=False)
        print(self.tests)

    def setCorrelation(self):
        self.variables.setCorrelation()

    def getCorrelationRestrictions(self):
        return self.variables.getCorrelationRestrictions()

    def getCorrelation(self):
        return self.variables.getCorrelation()

    def setCorrelationRestrictions(self):
        return self.variables.setCorrelationRestrictions(self.train, self.corrRestrictionType)


class ExcelGenerator:
    def generateExcel(self, data):
        table_start_pos = 2
        print("1 line")
        fileNameWithoutPath = "user_id_" + datetime.now().strftime("%Y%m%d") + "_" + \
            datetime.now().strftime("%H%M%S%f") + "_VariableStats"
        fileName = "API//Results//" + fileNameWithoutPath + ".xlsx"
        sheet_name = "VariableSpec"
        workbook = xlsxwriter.Workbook(fileName)
        worksheet = workbook.add_worksheet(name=sheet_name)
        header = "user_id " + datetime.now().strftime("%Y-%m-%d") + " " + \
            datetime.now().strftime("%H:%M:%S") + \
            " Variable Specifications for " + fileNameWithoutPath + ".xlsx"

        worksheet.write(2, 0, "Variable Name")
        worksheet.set_column("A:A", 16)
        worksheet.write(2, 1, "Missing values, %")
        worksheet.set_column("B:B", 18)
        worksheet.merge_range(first_row=0, first_col=0,
                              last_row=0, last_col=5, data=header)
        worksheet.add_table(table_start_pos, 0, len(data) + table_start_pos, 1, options={
                            'columns': [{'header': 'Variable Name'}, {'header': 'Missing values, %'}]})
        format1 = workbook.add_format({'bg_color':   'red',
                                       'font_color': 'white'})
        format2 = workbook.add_format({'bg_color':   'orange',
                                       'font_color': 'black'})
        print("2 line")
        conditions = "B" + str(table_start_pos + 2) + \
            ":B" + str(table_start_pos + 1 + len(data))
        worksheet.conditional_format(conditions, options={
                                     'type': 'cell', 'criteria': 'greater than or equal to', 'value':  20, 'format':   format1})
        worksheet.conditional_format(conditions, options={
                                     'type': 'cell', 'criteria': 'between', 'minimum':  15, 'maximum':  20, 'format':   format2})
        print("3 line")
        for i in range(len(data)):
            worksheet.write_row(row=table_start_pos + 1 + i, col=0,
                                data=[data[i]["column"], data[i]["missingPercent"]])
        print("4 line")
        workbook.close()
        return fileNameWithoutPath
