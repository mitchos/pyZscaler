class InvalidOSType(Exception):
    """
    Exception raised for errors in the input os_type.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message="Invalid os_type specified. Check the pyZscaler documentation for valid os_type options."):
        self.message = message
        super().__init__(message)
