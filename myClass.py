import re
class ExternalFunctions():
    def passwordVerify(password,confirm_password):
        if password==confirm_password:
            return True
        else:
            return False
    def validEmail(email):
        if re.match\
        ("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"\
        , email) != None:
            return True
        return False        
        
        