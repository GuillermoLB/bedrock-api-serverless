class ErrorsWithCodes(type):
    def __getattribute__(self, code):
        msg = super().__getattribute__(code)
        if code.startswith("__"):  # python system attributes like __class__
            return msg
        else:
            return f"[{code}] {msg}"


class Warnings(metaclass=ErrorsWithCodes):
    pass


class Errors(metaclass=ErrorsWithCodes):
    E003 = "Incorrect username or password"
    E004 = "Prompt cannot be empty"
    E008 = "User with username {username} already exists"
    E009 = "User account is inactive"
    E010 = "Invalid or expired token"
    E011 = "User not found"