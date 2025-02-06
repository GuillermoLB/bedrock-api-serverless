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
    E001 = "Model configuration not found"
    E002 = "Text_generation not found"
    E003 = "Incorrect username or password"
    E004 = "Prompt cannot be empty"
    E005 = "Not correct value: {max_length}. Max_length must be an int number greater than 0"
    E006 = "Not correct value: {temperature}. Temperature must be a float number between 0.0 and 1.0"
    E007 = "Not correct value: {top_p}. Top_p must be a float number between 0.0 and 1.0"
    E008 = "User with username {username} already exists"
    E009 = "User account is inactive"
    E010 = "Invalid or expired token"
    E011 = "User not found"