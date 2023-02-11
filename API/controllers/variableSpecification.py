class VariableSpecification:

    def __init__(self, name, dataType, ratioGroup):
        self.name = name
        self.dataType = dataType
        self.ratioGroup = ratioGroup

    def toJson(self):
        return {"name": self.name, "dataType": str(self.dataType), "ratioGroup": self.ratioGroup}
