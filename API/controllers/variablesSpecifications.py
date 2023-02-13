class VariablesSpecifications:
    """
    Description
    -------
    A class used to store data's DataFrame's list's for suitability for each column

    ...

    Attributes
    ----------
    validColumns: List<str>
        Suitable columns

    nonValidColumns: List<str>
        Non Suitable columns

    boolColumns: List<str>
        Columns which need to be prepared before being added to suitable column list

    variableSpecifications: List<Dictionary<VariableSpecification>>
        List of VariableSpecification Dictionary objects

    columnCorrelations: Dictionary -> {RatioGroup: {DataGroup: List<str>}}
        Dictionary that stores what kind of correlations are meaningful. Meaningful correlations are split into ratio group and the by data groups and by these conditions variables are splitted to meaningful correlations

    correlationMatrix:  Dictionary -> {RatioDataGroup: {column: columnName, correlations: List<columnCorrelations>}}
        Dictionary that holds splits of ratio and data group column correlation with each other, each column has a list of correlations with others variables

    Methods
    -------
    addValidColumn(column)
        add column to suitable column list

    addNonValidColumn(column)
        add column to unsuitable column list

    addBoolColumn(column)
        add column to unprepared before suitable column list

    addVariableSpecification(specification)
        adds Dictionary<VariableSpecification> to VariableSpecification list

    addCorrelationColumn(column, group)
        Adds variable to associated ratio group and the data group

    findDataGroup(column)
        Finds to which data group variable is associated with

    addColumnCorrelationMatrix(index, matrixJson)
        Adds a correlations dictionary to associated ratio group, data group
    """

    def __init__(self):
        self.validColumns = []
        self.nonValidColumns = []
        self.boolColumns = []
        self.variableSpecifications = []
        self.columnCorrelations = {}
        self.correlationMatrix = {}
        self.correlationRestrictions = {}

    def addValidColumn(self, column):
        """
        Description
        -------
        add column to suitable column list

        ...

        Attributes
        ----------
        column: string
            DataFrame's column to add to list
        """
        self.validColumns.append(column)

    def addNonValidColumn(self, column):
        """
        Description
        -------
        add column to unsuitable column list

        ...

        Attributes
        ----------
        column: string
            DataFrame's column to add to list
        """
        self.nonValidColumns.append(column)

    def addBoolColumn(self, column):
        """
        Description
        -------
        add column to unprepared before suitable column list

        ...

        Attributes
        ----------
        column: string
            DataFrame's column to add to list
        """
        self.boolColumns.append(column)

    def addVariableSpecification(self, specification):
        """
        Description
        -------
        adds Dictionary<VariableSpecification> to VariableSpecification list

        ...

        Attributes
        ----------
        specification: Dictionary<VariableSpecification>
            Dictionary of Variable Specification data
        """
        self.variableSpecifications.append(specification)

    def addCorrelationColumn(self, column, group):
        """
        Description
        -------
        Adds variable to associated ratio group and the data group

        ...

        Attributes
        ----------
        column: str
            variable name

        group: str
            ratio group
        """
        if "ResultVariable" == group:
            return
        elif group in self.columnCorrelations:
            var = self.findDataGroup(column)
            if var in self.columnCorrelations[group]:
                self.columnCorrelations[group][var].append(column)
            else:
                self.columnCorrelations[group][var] = [column]
        else:
            self.columnCorrelations[group] = {
                self.findDataGroup(column): [column]}

    def findDataGroup(self, column):
        """
        Description
        -------
        Finds to which data group variable is associated with

        ...

        Attributes
        ----------
        column: str
            variable name

        Returns
        ----------
        dataGroup: str
            Data group variable is associated with
        """
        if column.count("_") == 2:
            return column.split("_", 1)[0]
        else:
            return "Nor"

    def addColumnCorrelationMatrix(self, index, matrixJson):
        """
        Description
        -------
        Adds a correlations dictionary to associated ratio group, data group

        ...

        Attributes
        ----------
        index: str
            combined string from ratio group and data group

        matrixJson: Dictionary -> {column: variableColumn, correlations: List<correlationValues>}
            Dictionary of single column's correlation values with other variables
        """
        self.correlationMatrix[index] = matrixJson

    def addCorrelationRestriction(self, column, correlations):
        """
        Description
        -------
        Adds a correlation restriction list to dictionary by column

        ...

        Attributes
        ----------
        column: str
            column of dataset

        correlations: List<str>
            list of variables that cannot be in a model together with key 
        """
        self.correlationRestrictions[column] = correlations

    