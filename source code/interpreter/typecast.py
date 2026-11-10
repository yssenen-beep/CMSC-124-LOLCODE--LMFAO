"""
Typecasting rules for LOLCODE values. See specs for more details.
"""
from interpreter.values import MK_NOOB, MK_NUMBR, MK_NUMBAR, MK_YARN, MK_TROOF

def to_troof(value):
    if value.type == "TROOF":
        return value    
    # NOOBs can be implicitly typecast into TROOF.
    elif value.type == "NOOB":
        return MK_TROOF(False)                 
   
    # The empty string (“”) and numerical zero values are cast to FAIL.
    # All other values, except those mentioned above, are cast to WIN.
    elif value.type == "NUMBR" or value.type == "NUMBAR":
        return MK_TROOF(value.value != 0)      
    elif value.type == "YARN":
        return MK_TROOF(value.value != "")   
    else:
        raise Exception(f"Cannot cast {value.type} to TROOF.")



def to_numeric(value, explicit=False):

    if value.type == "NUMBR" or value.type == "NUMBAR":
        return value

    #  Casting WIN to a numerical type results in 1 or 1.0
    #  Casting FAIL results in a numerical zero.
    elif value.type == "TROOF":
        if value.value == True: 
            return MK_NUMBR(1)                 
        return MK_NUMBR(0)                  
    
    # YARN can be successfully cast into a NUMBAR or NUMBR if the
    # YARN does not contain any non-numerical, non-hyphen, non-period characters.
    elif value.type == "YARN":
     
        text = value.value
        digits = text
        if digits.startswith("-"):
            digits = digits[1:]                

        is_number = True
        if digits == "" or digits.count(".") > 1:
            is_number = False                  
        elif digits.startswith(".") or digits.endswith("."):
            is_number = False                
        else:
            for character in digits:
                if character not in "0123456789.":
                    is_number = False         

        if not is_number:
            raise Exception(f"Cannot cast YARN \"{text}\" to a number.")

        #if a decimal is found then the number is a NUMBAR, otherwise it is a NUMBR
        if "." in text: 
            return MK_NUMBAR(float(text))
        else:      
            return MK_NUMBR(int(text))             
    
    # Implicit typecasting of NOOB to any other type except TROOF will result in an error.
    # Explicit typecasting of NOOBs is allowed and results to empty/zero values depending on the type.
    elif value.type == "NOOB":
        if explicit == True:
            return MK_NUMBR(0)
        else:
            raise Exception("Cannot use NOOB as a number. Give the variable a value first.")
    else:
        raise Exception(f"Cannot cast {value.type} to a number.")



def to_yarn(value, explicit=False):
    
    if value.type == "YARN":
        return value
    # Casting NUMBRs to YARN will just convert the value into a
    # string of characters.
    elif value.type == "NUMBR":
        return MK_YARN(str(value.value))    
    
    # Casting NUMBARs to YARN will truncate the decimal portion up
    # to two decimal places.
    elif value.type == "NUMBAR":
        text = f"{value.value:.2f}" # straight to .2f no more slicing
        return MK_YARN(text)

    elif value.type == "TROOF":
        if value.value == True:
            return MK_YARN("WIN")
        else:
            return MK_YARN("FAIL")
    
    # Implicit typecasting of NOOB to any other type except TROOF will result in an error.
    # Explicit typecasting of NOOBs is allowed and results to empty/zero values depending on the type.
    elif value.type == "NOOB":
        if explicit == True:
            return MK_YARN("")
        else:
            raise Exception("Cannot use NOOB as a YARN. Give the variable a value first.")
    else:
        raise Exception(f"Cannot cast {value.type} to YARN.")


def cast(value, type_name):  
    if type_name == "TROOF":
        return to_troof(value)
    elif type_name == "NUMBR":
        number = to_numeric(value, explicit=True)
        return MK_NUMBR(int(number.value))
    elif type_name == "NUMBAR":
        number = to_numeric(value, explicit=True)
        return MK_NUMBAR(float(number.value))    
    elif type_name == "YARN":
        return to_yarn(value, explicit=True)
    elif type_name == "NOOB":
        return MK_NOOB()
    else:
        raise Exception(f"Unknown type {type_name}.")