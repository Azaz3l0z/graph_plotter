from math import *
from error_manager import ScientificErrorNotation

def eval_all(dict_):
    for key in dict_:
        # Transform items to list and sort
        items = [x[1] for x in sorted(dict_[key].items())]

        # Remove equal signs and evaluate
        for n, item in enumerate(items):
            # Fix bad characters
            item = item.replace("^", "**")
            item = item.replace("×", "*")
            
            # Get solution (right hand of equal sign)
            if "=" in item:
                items[n] = item.split("=")[1]
            
            if "≈" in item:
                items[n] = item.split("≈")[1]
            
            items[n] = eval(items[n].strip())

        dict_[key] = items

    # Parse significant digits
    length = len(dict_[list(dict_.keys())[0]])
    final_numbers = []
    for i in range(length):
        number = ScientificErrorNotation(dict_["functions"][i], dict_["errors"][i])
        final_numbers.append(number)

    return final_numbers