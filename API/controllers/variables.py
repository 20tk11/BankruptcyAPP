class Variables:
    """
    Description
    -------
    A class used to store DataFrame with file data and perform actions with data

    ...

    Attributes
    ----------
    variables : pd.DataFrame
        DataFrame which stores data from a file

    Methods
    -------
    setData(file)
        Set DataFrame with data from a file
    getData()
        Get DataFrame
    """
    @classmethod
    def setData(self, dataFrame):
        """
        Description
        -------
        Sets DataFrame

        ...


        Parameters
        -------
        dataFrame: pd.DataFrame
            DataFrame that contains data from file
        """
        self.variables = dataFrame

    @classmethod
    def getData(self):
        """
        Description
        -------
        Gets DataFrame

        ...


        Returns
        -------
        variables: pd.DataFrame
            DataFrame that contains data from file
        """
        return self.variables
