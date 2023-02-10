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
