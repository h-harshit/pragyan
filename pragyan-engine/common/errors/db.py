class ResourceNotFound(Exception):
    """Resource not found exception for database results"""

    def __init__(self, message="Resource Not found"):
        self.message = message
        super().__init__(self.message)
