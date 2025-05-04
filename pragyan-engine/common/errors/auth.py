class UserAlreadyExists(Exception):
    """User Already exists in database"""

    def __init__(self, message="User Already exists in database"):
        self.message = message
        super().__init__(self.message)
