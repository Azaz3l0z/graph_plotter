import re
from math import log10, floor

class ScientificErrorNotation(object):
    def __init__(self, value: float, error: float):
        self._value = value
        self._error = error      
        
        self.rounding_index = self.round_to_1(self._error)

    def original_value(self):
        return self._value
        
    def original_error(self):
        return self._error

    def value(self):
        return round(self._value, self.rounding_index)

    def error(self):
        return round(self._error, self.rounding_index)

    @staticmethod
    def round_to_1(x):
        round_to_digit = -(floor(log10(abs(x))))
        point = str(x).find(".")

        if abs(x) > 1:
            if str(x)[round_to_digit - 1] == "1":
                round_to_digit += 1

        elif abs(x) < 1:
            if str(x)[round_to_digit + 1] == "1":
                round_to_digit += 1
            
        return round_to_digit
    
    def __str__(self):
       

        return f'{self.value()} +- {self.error()}'