const columns: { [key: string]: string[] } = {
    '1B_1': ['ROA'],
    '1B_2': ['EBIT/TA'],
    '1B_3': ['ROE'],
    '1A_4': ['NP/S'],
    '1A_5': ['EBIT/S'],
    '1A_6': ['GP/S'],
    '2_7': ['CA/CL'],
    '2_8': ['CASH/CL'],
    '2_9': ['WC/TA'],
    '3_10': ['TL/TA'],
    '3_11': ['EQ/TA'],
    '3_12': ['EQ/TL'],
    '5B_13': ['RE/TA'],
    '5A_14': ['CASH/TA'],
    '3_15': ['FA/EQ'],
    '5A_16': ['INV/TA'],
    '4_17': ['S/TA'],
    '4_18': ['S/WC'],
    '4_19': ['S/FA'],
    '4_20': ['S/CA'],
    '4_21': ['S/EQ'],
    '4_22': ['S/CL'],
    '4_23': ['S/CASH'],
    '4_24': ['CS/S'],
    '1B_25': ['EBT/TA'],
    '1B_26': ['GP/TA'],
    '1B_27': ['EBT/EQ'],
    '1B_28': ['EBIT/CL'],
    '1B_29': ['EBT/(EQ-CL)'],
    '1A_30': ['EBT/S'],
    '2_31': ['(CL-CASH)/TA'],
    '2_32': ['(CASH-INV)/CL'],
    '2_33': ['(CA-INV)/CL'],
    '2_34': ['WC/EQ'],
    '2_35': ['INV/CL'],
    '2_36': ['CASH/TL'],
    '2_37': ['CASH/EQ'],
    '5B_38': ['CL/(TL-CASH)'],
    '2_39': ['AR/(TL-CASH)'],
    '2_40': ['AR/TL'],
    '3_41': ['EQ/(EQ+LTL)'],
    '3_42': ['CA/TL'],
    '3_43': ['CA/(TA-CASH)'],
    '5A_44': ['CA/TA'],
    '3_45': ['(EQ-IA)/(TA-IA-CASH-LAB)'],
    '4_46': ['S/TL'],
    '6_47': ['S/CS'],
    '4_48': ['WC/OE'],
    '6_49': ['LOGTA'],
    '6_50': ['LOGS'],
    'Audit': ['Audit'],
    'SingleShareholder': ['Single Shareholder'],
    'numberOfEntries': ['Number Of Records'],
    'FinancialReportLate': ['Financial Report Delivered Late'],
    'FinancialReportEstablishment': ['Financial Report Establishment Year'],
    'I.1.10': ['GDP'], // 1.1.10 Lietuvos BVP (lyginamosiomis kainomis (2010))
    'I.1.11': ['GDP Change'],
    'I.1.20': ['GDP Index'],
    'I.1.21': ['GDP Index Change'],
    'I.1.30': ['GDP Market Price'],
    'I.1.31': ['GDP Market Price Change'],
    'I.2.10': ['HICP'],
    'I.2.20': ['Infliation'],
    'I.2.30': ['Annual Infliation'],
    'I.3': ['Unemployment Rate'],
    'II.1': ['CIPI'],
    'II.2.10': ['HPI'],
    'II.2.11': ['HPI Change'],
    'III.1.10': ['ICW'],
    'III.1.11': ['ICW Change'],
    'III.1.20': ['CW'],
    'III.1.21': ['CW Change'],
    'III.1.30': ['TCA'],
    'III.1.31': ['TCA Change'],
    'III.1.40': ['STT'],
    'III.1.41': ['STT Change'],
    'III.2.10': ['IWS'],
    'III.2.11': ['IWS Change'],
    'III.3.10': ['INPE'],
    'III.3.11': ['INPE Change'],
    'IV.1.1': ['GP/S_CS'],
    'IV.1.2': ['NP/S_CS'],
    'IV.1.3': ['ROE_CS'],
    'IV.1.4': ['ROA_CS'],
    'IV.2.1': ['CA/CL_CS'],
    'IV.2.2': ['TL/TA_CS'],
    'IV.3.1': ['S/AR_CS'],
    'IV.3.2': ['S/TA_CS'],
    'IV.4': ['CCI_CS'],
}

// const economicColumns: { [key: string]: string[] } = {

// }
// const sectorColumns: { [key: string]: string[] } = {

// }

function getName(column: string) {

    if (column.includes('DIV_')) {
        return "Divided " + columns[column.replace('DIV_', '')][0]
    }
    else if (column.includes('SUB_')) {
        return "Subtracted " + columns[column.replace('SUB_', '')][0]
    }
    else {
        return columns[column][0]
    }



}

export { getName };