class VariableSpecification:
    """
    Description
    -------
    A class Object for storing DataFrame column's specification

    ...

    Attributes
    ----------
    name: str
        name of DataFrame's column
    dataType: str
        type of data stored in DataFrame column
    ratioGroup: str
        Ratio group that DataFrame's column belongs to
    Methods
    -------
    toJson()
        gets dictionary type object formed from VariableSpecification
    """

    def __init__(self, name, dataType, ratioGroup):
        self.name = name
        self.dataType = dataType
        self.ratioGroup = ratioGroup

    def toJson(self):
        """
        Description
        -------
        gets dictionary type object formed from VariableSpecification
        ...

        Returns
        ----------
        dict: Dictionary
            Dictionary type object of VariableSpecification
        """
        return {"name": self.name, "dataType": str(self.dataType), "ratioGroup": self.ratioGroup}
