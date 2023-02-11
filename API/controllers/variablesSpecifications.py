class VariablesSpecifications:

    def __init__(self):
        self.validColumns = []
        self.nonValidColumns = []
        self.boolColumns = []
        self.variableSpecifications = []

    def addValidColumn(self, column):
        self.validColumns.append(column)

    def addNonValidColumn(self, column):
        self.nonValidColumns.append(column)

    def addBoolColumn(self, column):
        self.boolColumns.append(column)

    def addVariableSpecification(self, specification):
        self.variableSpecifications.append(specification)
