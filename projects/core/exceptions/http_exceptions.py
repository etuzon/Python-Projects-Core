class HttpResponseNotJson(Exception):

    def __init__(self, msg):
        """
        Constructor
        """
        self.message = msg
        super().__init__(self.message)
