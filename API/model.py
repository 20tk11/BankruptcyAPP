import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import xlsxwriter
from scipy.stats import kstest
from scipy.stats import mannwhitneyu
import statsmodels.api as sm


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

    def getMissingPercent(self, column):
        return self.variables[column].isna().sum() * 100 / len(self.variables)

    def kolmogorovSmirnovTest(self, column):
        print(column)
        return kstest(self.variables[column].dropna(), 'norm')

    def mannWhitneyUTest(self, column):
        IsBankrupt_Not = self.variables[self.variables['Y'] == 0]
        IsBankrupt_Yes = self.variables[self.variables['Y'] == 1]
        return mannwhitneyu(
            x=IsBankrupt_Yes[column].dropna(), y=IsBankrupt_Not[column].dropna(), alternative='two-sided')

    
    def singleLogit(self, column):
        if ("Y" == column):
            return 0, 0, 0, 0, 0, 0
        dftemp = self.variables.dropna(subset=[column])
        exog = sm.add_constant(dftemp[column])
        endog = dftemp['Y']
        model = sm.Logit(endog, exog, missing='drop').fit(
            method="bfgs", maxiter=100)
        print(model.summary())
        constantPValue = model.pvalues[0]
        valuePValue = model.pvalues[1]
        constantStatistic = model.tvalues[0]
        valueStatistic = model.tvalues[1]
        constant = model.params[0]
        value = model.params[1]

        return constantPValue, valuePValue, constantStatistic, valueStatistic, constant, value

    #Filter columns that are not needed in the reggresion - fix problem with sm.Logit for getting string values
    def analyzeVariables(self):
        self.variableSpec = []
        for i in self.variables.columns:
            missingPercent = self.getMissingPercent(i)
            ksResult = self.kolmogorovSmirnovTest(i)
            mannWhitney = self.mannWhitneyUTest(i)
            modelConstPValue, modelValuePValue, modelConstStatistic, modelValueStatistic, constant, value = self.singleLogit(
                i)
            variableSpec = VariableSpecifications(
                i, missingPercent, ksResult[0], ksResult[1], mannWhitney[0], mannWhitney[1], value, constant,
                modelValueStatistic, modelConstStatistic, modelValuePValue, modelConstPValue).getJson()
            print(modelValuePValue)
            print(type(modelValuePValue))
            self.variableSpec.append(variableSpec)

    def getExcel(self):
        excelGen = ExcelGenerator()
        return excelGen.generateExcel(self.variableSpec)


class VariableSpecifications:

    def __init__(self, variableName, missingPercent, ksstatistic, kspvalue, testStatistic, testPValue,
                 singleValue, singleConstant, singleValueStatistic, singleConstantStatistic, singleValuePValue, singleConstantPValue):
        self.variableName = variableName
        self.missingPercent = missingPercent
        self.ksstatistic = ksstatistic
        self.kspvalue = kspvalue
        if (self.kspvalue < 0.05):
            self.ksResults = "Mann-Whitney U Test"
        else:
            self.ksResults = "T=Test"
        self.testStatistic = testStatistic
        self.testPValue = testPValue
        if (self.testPValue < 0.05):
            self.testResults = "Significant"
        else:
            self.testResults = "Non Significant"
        self.singleValue = singleValue
        self.singleConstant = singleConstant
        self.singleValueStatistic = singleValueStatistic
        self.singleConstantStatistic = singleConstantStatistic
        self.singleValuePValue = singleValuePValue
        self.singleConstantPValue = singleConstantPValue

    def getJson(self):
        return {"column": self.variableName, "missingPercent": self.missingPercent,
                "ksstatistic": self.ksstatistic, "kspvalue": self.kspvalue, "Conc1": self.ksResults,
                "testStatistic": self.testStatistic, "testPValue": self.testPValue, "significance": self.testResults,
                "singleValue": self.singleValue, "singleConstant": self.singleConstant, "singleValueStatistic": self.singleValueStatistic,
                "singleConstantStatistic": self.singleConstantStatistic, "singleValuePValue": self.singleValuePValue, "singleConstantPValue": self.singleConstantPValue}


class Model:
    def __init__(self):
        self.variables = Variables()

    def setFileName(self, fileName):
        self.fileName = fileName

    def setVariables(self):
        self.variables.setDataframe(self.fileName)

    def analyzeModelVariables(self):
        self.variables.columnMisingPercent()

    def getVariableStats(self):
        return self.variables

    def getModel(self):
        self.setFileName("Data//dataset1.csv")
        self.setVariables()
        self.analyzeModelVariables()
        return self.variables.getVariableStats()


class ExcelGenerator:
    def generateExcel(self, data):
        table_start_pos = 2
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
        conditions = "B" + str(table_start_pos + 2) + \
            ":B" + str(table_start_pos + 1 + len(data))
        worksheet.conditional_format(conditions, options={
                                     'type': 'cell', 'criteria': 'greater than or equal to', 'value':  20, 'format':   format1})
        worksheet.conditional_format(conditions, options={
                                     'type': 'cell', 'criteria': 'between', 'minimum':  15, 'maximum':  20, 'format':   format2})
        for i in range(len(data)):
            worksheet.write_row(row=table_start_pos + 1 + i, col=0,
                                data=[data[i]["column"], data[i]["missingPercent"]])
        workbook.close()
        return fileNameWithoutPath