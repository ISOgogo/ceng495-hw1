class InvalidEmail(Exception):
    """Email Error"""
    pass

class InvalidPassword(Exception):
    """Password Error"""
    pass

class EmptyEmailError(Exception):
    """Empty Email Error"""
    pass

class EmptyPasswordError(Exception):
    """Empty Password Error"""
    pass

class EmailAlreadyUsed(Exception):
    """Email Already Used Error"""
    pass

class UserNotFound(Exception):
    """User Not Found Error"""
    pass