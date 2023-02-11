
financialColumnsC = ['SUB_1B_1', 'SUB_1B_2', 'SUB_1B_3', 'SUB_1A_4', 'SUB_1A_5', 'SUB_1A_6', 'SUB_2_7', 'SUB_2_8', 'SUB_2_9', 'SUB_3_10', 'SUB_3_11', 'SUB_3_12', 'SUB_5B_13', 'SUB_5A_14', 'SUB_3_15', 'SUB_5A_16', 'SUB_4_17', 'SUB_4_18', 'SUB_4_19', 'SUB_4_20', 'SUB_4_21', 'SUB_4_22', 'SUB_4_23', 'SUB_4_24', 'SUB_1B_25', 'SUB_1B_26', 'SUB_1B_27', 'SUB_1B_28', 'SUB_1B_29', 'SUB_1A_30', 'SUB_2_31', 'SUB_2_32', 'SUB_2_33', 'SUB_2_34', 'SUB_2_35', 'SUB_2_36', 'SUB_2_37', 'SUB_5B_38', 'SUB_2_39', 'SUB_2_40', 'SUB_3_41', 'SUB_3_42', 'SUB_3_43', 'SUB_5A_44', 'SUB_3_45', 'SUB_4_46', 'SUB_6_47', 'SUB_4_48', 'SUB_6_50']

financialColumnsB = ['DIV_1B_1', 'DIV_1B_2', 'DIV_1B_3', 'DIV_1A_4', 'DIV_1A_5', 'DIV_1A_6', 'DIV_2_7', 'DIV_2_8', 'DIV_2_9', 'DIV_3_10', 'DIV_3_11', 'DIV_3_12', 'DIV_5B_13', 'DIV_5A_14', 'DIV_3_15', 'DIV_5A_16', 'DIV_4_17', 'DIV_4_18', 'DIV_4_19', 'DIV_4_20', 'DIV_4_21', 'DIV_4_22', 'DIV_4_23', 'DIV_4_24', 'DIV_1B_25', 'DIV_1B_26', 'DIV_1B_27', 'DIV_1B_28', 'DIV_1B_29', 'DIV_1A_30', 'DIV_2_31', 'DIV_2_32', 'DIV_2_33', 'DIV_2_34', 'DIV_2_35', 'DIV_2_36', 'DIV_2_37', 'DIV_5B_38', 'DIV_2_39', 'DIV_2_40', 'DIV_3_41', 'DIV_3_42', 'DIV_3_43', 'DIV_5A_44', 'DIV_3_45', 'DIV_4_46', 'DIV_6_47', 'DIV_4_48', 'DIV_6_49', 'DIV_6_50']

financialColumnsA = ['1B_1', '1B_2', '1B_3', '1A_4', '1A_5', '1A_6', '2_7', '2_8', '2_9', '3_10', '3_11', '3_12', '5B_13', '5A_14', '3_15', '5A_16', '4_17', '4_18', '4_19', '4_20', '4_21', '4_22', '4_23', '4_24', '1B_25', '1B_26', '1B_27', '1B_28', '1B_29', '1A_30', '2_31', '2_32', '2_33', '2_34', '2_35', '2_36', '2_37', '5B_38', '2_39', '2_40', '3_41', '3_42', '3_43', '5A_44', '3_45', '4_46', '6_47', '4_48', '6_49', '6_50']




def getNonFinancialColumns():
    return nonfinancialColumns

def getEconomicColumns():
    return economicColumns

def getBranchColumns():
    return industryBranchColumns

def getFinancialColumns():
    return financialRatios

def getLiquidityColumns():
    return liquidityRatios


def getSolvencyColumns():
    return solvencyRatios


def getActivityColumns():
    return activityRatios


def getStructureColumns():
    return structureRatios


def getOtherColumns():
    return otherRatios


def findRatioGroup(Best_model):
    significantVariables = []
    financial = []
    liquidity = []
    solvency = []
    activity = []
    structure = []
    other = []
    economic = []
    industry = []
    nonfinancial = []
    for i in range(len(Best_model.pvalues)):
        variable = {"variable": Best_model.pvalues.index[i],
                    "significance": Best_model.pvalues[i], "coefficient": Best_model.params[i]}
        if (Best_model.pvalues.index[i] in financialRatios):
            financial.append(variable)
        elif (Best_model.pvalues.index[i] in liquidityRatios):
            liquidity.append(variable)
        elif (Best_model.pvalues.index[i] in solvencyRatios):
            solvency.append(variable)
        elif (Best_model.pvalues.index[i] in activityRatios):
            activity.append(variable)
        elif (Best_model.pvalues.index[i] in structureRatios):
            structure.append(variable)
        elif (Best_model.pvalues.index[i] in otherRatios):
            other.append(variable)
        elif (Best_model.pvalues.index[i] in economicColumns):
            economic.append(variable)
        elif (Best_model.pvalues.index[i] in industryBranchColumns):
            industry.append(variable)
        elif (Best_model.pvalues.index[i] in nonfinancialColumns):
            nonfinancial.append(variable)
        else:
            const = {"variable": Best_model.pvalues.index[i],
                     "significance": Best_model.pvalues[i], "coefficient": Best_model.params[i]}

    return {"financial": financial, "liquidity": liquidity, "solvency": solvency, "activity": activity, "structure": structure, "other": other, "const": const, "economic": economic, "industry": industry, "nonfinancial": nonfinancial}


def getColumns():
    return financialColumnsA + financialColumnsB + financialColumnsC + nonfinancialColumns + economicColumns + industryBranchColumns


def getFinancialColumnsA():
    return financialColumnsA


def getFinancialColumnsAB():
    return financialColumnsA + financialColumnsB


def getFinancialColumnsAC():
    return financialColumnsA + financialColumnsC


def getFinancialColumnsABC():
    return financialColumnsA + financialColumnsB + financialColumnsC


def getByFinancialColumnsState(state):
    if state == "A":
        return getFinancialColumnsA()
    elif state == "AB":
        return getFinancialColumnsAB()
    elif state == "AC":
        return getFinancialColumnsAC()
    elif state == "ABC":
        return getFinancialColumnsABC()


def getColumnsByType(type, state):
    if type == "type1":
        return getByFinancialColumnsState(state)
    elif type == "type2":
        return getByFinancialColumnsState(state) + economicColumns
    elif type == "type3":
        return getByFinancialColumnsState(state) + economicColumns + industryBranchColumns
    elif type == "type4":
        return getByFinancialColumnsState(state) + economicColumns + industryBranchColumns + nonfinancialColumns
