import base64
import urllib.parse as urlparse

class WolframInputGenerator(object):
    def __init__(self) -> None:      
        self.wolfram_input = "[{expression}]"
        self.partial_derivative = '{{"t":46,"c":[[{{"t":0,"v":"{expression}"}}],[{{"t":0,"v":"{variable}"}}]]}}'
        self.normal_expression = '{{"t": 0, "v":"{expression}"}}'
    
    
    def gaussian_error(self, function: str, variables: list):
        request_input = ""
        request_input += self.normal_expression.format(expression="sqrt(")
        request_input += ","

        # Add squared partial derivatives
        for var in variables:
            request_input += self.normal_expression.format(expression="(")
            request_input += ","
            request_input += self.partial_derivative.format(expression=function, variable=var)
            request_input += ","
            request_input += self.normal_expression.format(expression="0.1")
            request_input += ","
            request_input += self.normal_expression.format(expression=")^2")

            if var != variables[-1]:
                request_input += ","
                request_input += self.normal_expression.format(expression="+")
                request_input += ","

        # Close square root
        request_input += ","
        request_input += self.normal_expression.format(expression=")")

        # Evaluate
        for var in variables:
            request_input += ","
            request_input += self.normal_expression.format(expression=f",{var}=1")

        # Transform to base64 url encoded format
        request_input = self.wolfram_input.format(expression=request_input)
        print(request_input)
        request_input = base64.b64encode(bytes(request_input, 'utf-8'))
        request_input = urlparse.quote_plus(request_input)

        return request_input

variables = ["x", "y"]
f = "x*y"

r = WolframInputGenerator().gaussian_error(f, variables)


print(r)