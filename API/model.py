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

    def getCorrelation(self):
        self.correlationRestrictions = []
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
        return {"financial": financial, "liquidity": liquidity, "solvency": solvency,
                "activity": activity, "structure": structure, "other": other, "nonfinancial": nonfinancial,
                "economic": economic, "industry": industry}

    def getCorrelationByRatioType(self, columns):
        correlation = pd.DataFrame()
        for i in np.intersect1d(columns, self.variables.columns):
            correlation[i] = self.variables[i]
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
            corrRe = []
            for j in range(len(corr_matrix.values[i].tolist())):
                if corr_matrix.values[i][j] >= 0.7 or corr_matrix.values[i][j] <= -0.7:
                    corrRe.append(corr_matrix.columns[j])
            corrRestrictionColumn = {corr_matrix.columns[i]:corrRe }
            self.correlationRestrictions.append(corrRestrictionColumn)
        return columnCorrelation

    def getCorrelationRestrictions(self):
        return self.correlationRestrictions

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

    def getModel(self):
        self.added_columns = []
        self.tests = pd.DataFrame(
            columns=['LLR', 'prsquared', 'aic', 'bic', 'p-value'])
        self.max_LR = None
        self.modellist = []
        self.modelLog = pd.DataFrame(
            columns=['LLR', 'prsquared', 'aic', 'bic'])
        self.Best_model = None
        self.columnLog = []
        self.setDataSplits()
        counter = 0
        print(self.variables.getSignificant())
        for i in range(8):
            Best_column = None
            for column in self.variables.getSignificant():
                if column not in self.added_columns:
                    endog = self.train['IsBankrupt']
                    if len(self.added_columns) == 0:
                        exog = sm.add_constant(self.train[column])
                    else:
                        exog = sm.add_constant(
                            self.train[self.added_columns + [column]])
                    self.model = sm.Logit(endog, exog, missing='drop').fit(
                        method="bfgs")
                    print(self.model.summary())
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
            self.modelLog.loc[counter] = [
                self.Best_model.llr, self.Best_model.prsquared, self.Best_model.bic, self.Best_model.aic]
            counter = counter + 1
            self.modellist.append(self.Best_model)
            print(self.Best_model.summary())
            for j in range(1, len(self.Best_model.pvalues)):
                if (self.Best_model.pvalues[j] >= 0.05):
                    print(self.Best_model.pvalues[j])
                    print(self.Best_model.pvalues.index[j])
                    self.added_columns.remove(self.Best_model.pvalues.index[j])
                    endog = self.train['IsBankrupt']
                    exog = sm.add_constant(
                        self.train[self.added_columns])
                    self.model = sm.Logit(endog, exog, missing='drop').fit(
                        method="bfgs")
                    self.Best_model = self.model
                    self.columnLog.append(deepcopy(self.added_columns))
                    self.modelLog.loc[counter] = [
                        self.Best_model.llr, self.Best_model.prsquared, self.Best_model.bic, self.Best_model.aic]
                    counter = counter + 1
                    self.modellist.append(self.Best_model)
                    break
        print(self.Best_model.summary())

    def formSignificantVariables(self):
        return findRatioGroup(self.Best_model)

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

        return {"variables": variables, "trainPred": confusionMatrixTrainData,
                "testPred": confusionMatrixTestData, "coxSnell": CS, "negelkerke": Negel,
                "macFadden": MF, "chiSquare": ChiSq, "numObs": self.Best_model.nobs}

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

    def getCorrelation(self):
        return self.variables.getCorrelation()

    def getCorrelationRestrictions(self):
        return self.variables.getCorrelationRestrictions()


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
