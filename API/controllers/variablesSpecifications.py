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
    """

    def __init__(self):
        self.validColumns = []
        self.nonValidColumns = []
        self.boolColumns = []
        self.variableSpecifications = []

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
