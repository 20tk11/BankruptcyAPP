from flask import jsonify


class ErrorHandler:
    """
    Description
    -------
    A class to return appropriate response message for an error

    ...

    Methods
    -------
    fileTypeError()
        Gets response for bad file type error
    """
    def fileTypeError():
        """
        Description
        -------
        Gets response for wrong file type import

        Returns
        ----------
        json : Response
            returns status code 400 with message and description for error
        """
        return jsonify(status=400, error="File type is incompatible", description="Ensure File type is correct"), 400

    def fileReadError(file):
        """
        Description
        -------
        Gets response for error caused while reading a file

        Returns
        ----------
        json : Response
            returns status code 400 with message and description for error
        """
        return jsonify(status=400, error=f"Error ocurred while reading file of {file.type}", description=f"Ensure that data is inserted correctly inside type {file.type} file or provide the file for us to find the solution to fix the file"), 400
