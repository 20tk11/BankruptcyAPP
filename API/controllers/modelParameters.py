class ModelParameters:
    """
    Description
    -------
    A class used to parameters to use in model generation.

    ...

    Attributes
    ----------
    type : str
            parameter which describes which types of data to use when creating an model
    corrState : str
        parameter which describes what kind of correlation requirement to use when choosing variables to add into the model
    modelType : str
        parameter which describes to generate a model from financial data or custom
    usedDataState : str
        parameter which describes if to use bonus variables in the model: Divided and Subtracted

    Methods
    -------
    setModelParameters(type, corrState, usedDataState, modelType)
        Set file containing data
    setType(type)
        Get file containing data
    setCorrState(corrState)
        Set parameters for model by which the model will be generated
    setUsedDataState(usedDataState)
        Get file containing data
    setModelType(modelType)
        Get file containing data
    getType()
        Get file containing data
    getCorrState()
        Set parameters for model by which the model will be generated
    getUsedDataState()
        Get file containing data
    getModelType()
        Get file containing data
    """

    type = None
    corrState = None
    usedDataState = None
    modelType = None

    @classmethod
    def setModelParameters(self, type, corrState, usedDataState, modelType):
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
        self.setType(type)
        self.setCorrState(corrState)
        self.setUsedDataState(usedDataState)
        self.setModelType(modelType)

    @classmethod
    def setType(self, type):
        """
        Description
        -------
        Set model date types parameter

        Parameters
        ----------
        type : str
            parameter which describes which types of data to use when creating an model
        """
        self.type = type

    @classmethod
    def setCorrState(self, corrState):
        """
        Description
        -------
        Set model correlation restriction parameter

        Parameters
        ----------
        corrState : str
            parameter which describes what kind of correlation requirement to use when choosing variables to add into the model
        """
        self.corrState = corrState

    @classmethod
    def setUsedDataState(self, usedDataState):
        """
        Description
        -------
        Set model bonus variables parameter

        Parameters
        ----------
        usedDataState : str
            parameter which describes if to use bonus variables in the model: Divided and Subtracted
        """
        self.usedDataState = usedDataState

    @classmethod
    def setModelType(self, modelType):
        """
        Description
        -------
        Set model type parameter

        Parameters
        ----------
        modelType : str
            parameter which describes to generate a model from financial data or custom
        """
        self.modelType = modelType

    @classmethod
    def getType(self):
        """
        Description
        -------
        Get model date types parameter

        Returns
        ----------
        parameter which describes which types of data to use when creating an model
        """
        return self.type

    @classmethod
    def getCorrState(self):
        """
        Description
        -------
        Get model correlation restriction parameter

        Returns
        ----------
        parameter which describes what kind of correlation requirement to use when choosing variables to add into the model
        """
        return self.corrState

    @classmethod
    def getUsedDataState(self):
        """
        Description
        -------
        Get model bonus variables parameter

        Returns
        ----------
        parameter which describes if to use bonus variables in the model: Divided and Subtracted
        """
        return self.usedDataState

    @classmethod
    def getModelType(self):
        """
        Description
        -------
        Get model type parameter

        Returns
        ----------
        parameter which describes to generate a model from financial data or custom
        """
        return self.modelType
