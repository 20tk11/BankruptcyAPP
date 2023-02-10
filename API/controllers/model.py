from controllers.modelParameters import ModelParameters
from controllers.file import File


class Model:
    """
    Description
    -------
    A class used to store Logistic regression model and to train it.

    Here Variables and VariableSpecifications are stored
        Access methods and variables of other classes

    ...

    Attributes
    ----------
    file : File
        file of types: json, csv, xlsx

    Methods
    -------
    setFile(file)
        Set file containing data
    getFile()
        Get file containing data
    setModelParameters(type, corrState, modelType, usedDataState)
        Set parameters for model by which the model will be generated
    """

    file = File
    modelParameters = ModelParameters

    def __init__(self):
        self.var = "1"

    @classmethod
    def setFile(self, file):
        """
        Description
        -------
        Set file containing data

        Parameters
        ----------
        file : werkzeug.datastructures.FileStorage
            file of types: json, csv, xlsx
        """
        return self.file.setFile(file)

    @classmethod
    def getFile(self):
        """
        Description
        -------
        Get file containing data

        Returns
        -------
        File
            a file containing data used in model creation and file type
        """
        return self.file

    @classmethod
    def setModelParameters(self, type, corrState, modelType, usedDataState):
        """
        Description
        -------
        Set parameters for model by which the model will be generated

        Parameters
        ----------
        type : str
            parameter which describes which types of data to use when creating an model
        corrState : str
            parameter which describes what kind of correlation requirement to use when choosing variables to add into the model
        modelType : str
            parameter which describes to generate a model from financial data or custom
        usedDataState : str
            parameter which describes if to use bonus variables in the model: Divided and Subtracted
        """
        self.modelParameters.setModelParameters(
            type, corrState, modelType, usedDataState)
