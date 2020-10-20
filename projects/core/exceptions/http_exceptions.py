class HttpResponseNotJson(Exception):

    def __init__(self, msg):
        """
        Constructor
        """
        super().__init__(msg)
        self.message = msg
