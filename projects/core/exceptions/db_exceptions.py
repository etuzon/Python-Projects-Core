

class DbConnectionException(Exception):
    """
     Db connection Exception
    """

    def __init__(self, msg):
        """
        Constructor
        """
        self.message = msg
        super().__init__(self.message)


class DbException(Exception):
    def __init__(self, msg):
        """
        Constructor
        """
        self.message = msg
        super().__init__(self.message)
