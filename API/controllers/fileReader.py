import pandas as pd


class FileReader:
    """
    Description
    -------
    A class used to read json, xlsx or csv type files

    ...

    Methods
    -------
    read(file)
        Method to determine how to read file
    readCSV(file)
        Read a csv file and returns a DataFrame
    readJSON(file)
        Read a json file and returns a DataFrame
    readXLSX(file)
        Read a xlsx file and returns a DataFrame
    """

    @classmethod
    def read(self, file):
        """
        Description
        -------
        A class used to read json, xlsx or csv type files

        Attributes
        -------
        file: File
            a file from which to read data and type of the file

        Returns
        -------
        Status Code
            informs that reading the file caused an error
        pd.DataFrame
            DataFrame read from csv, xlsx or json file
        """
        match file.type:
            case "csv":
                return self.readCSV(file.file)
            case "xlsx":
                return self.readXLSX(file.file)
            case "json":
                return self.readJSON(file.file)
            case _:
                return 400

    def readCSV(file):
        """
        Description
        -------
        A class used to read csv type files

        Attributes
        -------
        file: File
            a file from which to read data and type of the file

        Returns
        -------
        pd.DataFrame
            DataFrame read from csv
        """
        return pd.read_csv(file)

    def readJSON(file):
        """
        Description
        -------
        A class used to read json type files

        Attributes
        -------
        file: File
            a file from which to read data and type of the file

        Returns
        -------
        pd.DataFrame
            DataFrame read from jsom
        """
        return pd.read_json(file)

    def readXLSX(file):
        """
        Description
        -------
        A class used to read xlsx type files

        Attributes
        -------
        file: File
            a file from which to read data and type of the file

        Returns
        -------
        pd.DataFrame
            DataFrame read from xlsx
        """
        return pd.read_excel(file)
