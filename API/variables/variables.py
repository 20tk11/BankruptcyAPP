informationalColumns = ["JARCODE", "RegistrationYear", "DeregistrationYear", "BusinessSector",
                        "BankruptcyCaseStartYear", "FinancialYear", "FinancialYearsTillBankruptcy"]

profitabilityRatios = ['1B_1', '1B_2', '1B_3', '1A_4', '1A_5', '1A_6', '1B_25', '1B_26',
                       '1B_27', '1B_28', '1B_29', '1A_30']

liquidityRatios = ['2_7', '2_8', '2_9', '2_31', '2_32', '2_33', '2_34', '2_35', '2_36',
                   '2_37', '2_39', '2_40']

solvencyRatios = ['3_10', '3_11', '3_12',
                  '3_15', '3_41', '3_42', '3_43', '3_45']

activityRatios = ['4_17', '4_18', '4_19', '4_20',
                  '4_21', '4_22', '4_23', '4_24', '4_46', '4_48']

structureRatios = ['5B_13', '5A_14', '5A_16', '5B_38', '5A_44']

otherRatios = ['6_47', '6_49', '6_50']

nonfinancialColumns = ['Audit', 'SingleShareholder', 'numberOfEntries', 'FinancialReportLate',
                       'FinancialReportEstablishment']

economicColumns = ['I.1.10', 'I.1.11', 'I.1.20', 'I.1.21', 'I.1.30', 'I.1.31', 'I.2.10',
                   'I.2.20', 'I.2.30', 'I.3', 'II.1', 'II.2.10', 'II.2.11']

industryBranchColumns = ['III.1.10', 'III.1.11', 'III.1.20', 'III.1.21', 'III.1.30', 'III.1.31',
                         'III.1.40', 'III.1.41', 'III.2.10', 'III.2.11', 'III.3.10', 'III.3.11', 'IV.1.1', 'IV.1.2', 'IV.1.3', 'IV.1.4', 'IV.2.1', 'IV.2.2', 'IV.3.1', 'IV.3.2', 'IV.4']
#


def getFinanacialRatios():
    return profitabilityRatios + liquidityRatios + solvencyRatios + activityRatios + structureRatios + otherRatios
