"""
Maps the types of LOLCODE values to their corresponding Python types. 
"""

class RuntimeVal:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def MK_NOOB():
    return RuntimeVal("NOOB", None)


def MK_NUMBR(integer_number):
    return RuntimeVal("NUMBR", int(integer_number))


def MK_NUMBAR(float_number):
    return RuntimeVal("NUMBAR", float(float_number))


def MK_YARN(text):
    return RuntimeVal("YARN", str(text))


def MK_TROOF(boolean_value):
    return RuntimeVal("TROOF", bool(boolean_value))