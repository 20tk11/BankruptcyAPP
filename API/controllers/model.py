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
    """

    file = File

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
