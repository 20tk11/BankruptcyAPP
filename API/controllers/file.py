from flask import abort, jsonify


class File:
    """
    Description
    -------
    A class used to store file and information about file

    ...

    Attributes
    ----------
    file : werkzeug.datastructures.FileStorage
        file of types: json, csv, xlsx
    type : str
        type of file

    Methods
    -------
    setFile(file)
        Set file and it's type
    getFile()
        Get file
    getFileType()
        Get file Type
    setFileType()
        Set File Type
    """

    def __init__(self):
        self.type = None
        self.file = None

    def setFile(self, file):
        """
        Description
        -------
        Set file and it's type

        Parameters
        ----------
        file : werkzeug.datastructures.FileStorage
            file of types: json, csv, xlsx
        """
        self.file = file
        self.setFileType(file)

        if self.type not in ["csv", "json", "xlsx"]:
            return 400

    def setFileType(self, file):
        """
        Description
        -------
        Set file type by getting extension string of filename

        Parameters
        ----------
        file : werkzeug.datastructures.FileStorage
            file of types: json, csv, xlsx
        """
        self.type = file.filename.lower().split(".")[-1]
