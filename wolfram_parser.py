import copy
import base64
import urllib.parse as urlparse

class DifferentListLength(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class WolframInputGenerator(object):
    def __init__(self) -> None:     
        # The WolframInputGenerator class exists because Wolfram API doesn't
        # accept convetional expressions as inputs, instead it accepts a weird
        # conbination of parameters that allow it to exist

        # This is not a full adaptation, it only accepts regular expressions 
        # such as + = evaluation, etc and derivatives.

        self.wolfram_input = "[{expression}]"
        self.partial_derivative = '{{"t":46,"c":[[{{"t":0,"v":"{expression}"}}],[{{"t":0,"v":"{variable}"}}]]}}'
        self.normal_expression = '{{"t": 0, "v":"{expression}"}}'


        # This url is to make a request to the API
        self.wolfree_url = "" +\
        "https://api.wolframalpha.com/v2/query?"+\
        "&callback=jQuery36108552903897608751_1666553041562"+\
        "&output=json"+\
        "&reinterpret=true"+\
        "&scantimeout=30"+\
        "&podtimeout=30"+\
        "&formattimeout=30"+\
        "&parsetimeout=30"+\
        "&totaltimeout=30"+\
        "&podstate=Approximate form"+\
        "&i2d=true"+\
        "&input={request_input}"+\
        "&appid=H9V325-HTALUWHKGK"+\
        "&_=1666553041563"

    @staticmethod
    def __encode(code):
        code = base64.b64encode(bytes(code, 'utf-8'))
        code = urlparse.quote_plus(code)

        return code


    def url_generator(self, codes):
        """
        Creates the url for a specific base64 WolframAlpha accepted code
        """
        if isinstance(codes, list):
            for n, code in enumerate(codes):
                codes[n] = self.wolfree_url.format(request_input=code)

        else:
            codes = [codes]

        return codes
    
    def gaussian_error(self, function: str, variables_big):
        """
        Creates the code for an acceptable Wolfram Alpaha base64 urlencoded
        code / wolfree_input, which will be used to make a request
        """
        request_input_list = []
        if isinstance(variables_big, dict):
            variables_big = self.__var_list_value(variables_big)

        for i, variables in enumerate(variables_big):
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

                if var != list(variables.keys())[-1]:
                    request_input += ","
                    request_input += self.normal_expression.format(expression="+")
                    request_input += ","

            # Close square root
            request_input += ","
            request_input += self.normal_expression.format(expression=")")

            # Evaluate
            for var in variables:
                request_input += ","
                request_input += self.normal_expression.format(expression=f',{var}={variables[var]["value"]}')

            
            # Transform to base64 url encoded format
            request_input = self.wolfram_input.format(expression=request_input)
            request_input = self.__encode(request_input)

            request_input_list.append(request_input)
            
        url_lists = self.url_generator(request_input_list)
        search_term = "Substitution"

        return (url_lists, search_term)


    def function_eval(self, function: str, variables_big):
        """
        Creates the code for an acceptable Wolfram Alpaha base64 urlencoded
        code / wolfree_input, which will be used to make a request
        """
        request_input_list = []
        if isinstance(variables_big, dict):
            variables_big = self.__var_list_value(variables_big)

        for i, variables in enumerate(variables_big):
            request_input = ""
            request_input += self.normal_expression.format(expression=function)
            for var in variables:
                request_input += ","
                request_input += self.normal_expression.format(expression=f',{var}={variables[var]["value"]}')

            # Transform to base64 url encoded format
            request_input = self.wolfram_input.format(expression=request_input)
            request_input = self.__encode(request_input)

            request_input_list.append(request_input)
        
        url_lists = self.url_generator(request_input_list)
        search_term = "Substitution"

        return (url_lists, search_term)

    def __var_list_value(self, variables: dict):
        """
        Transforms a dictionary of values into multiple dictionaries that
        contain only 1 value per x_n, so that it's easier to make the requests
        """
        variables_list = []
        new_variables = copy.deepcopy(variables)

        length = 0
        for var in variables:
            if length == 0:
                length = len(variables[var]["value"])

            val_length = len(variables[var]["value"])
            # err_length = len(variables[var]["error"])

            if (val_length != length):
                raise DifferentListLength("The list of value is different for your variables")

        list_length = len(variables[list(variables.keys())[0]]["value"])
        for i in range(list_length):
            for var in variables:
                new_variables[var]["value"] = variables[var]["value"][i]

                if isinstance(variables[var]["error"], list):
                    new_variables[var]["error"] = variables[var]["error"][i]
            
            variables_list.append(copy.deepcopy(new_variables))

        return variables_list