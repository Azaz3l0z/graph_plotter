import json
import base64
import requests
import numpy as np
import matplotlib.pyplot as plt
import urllib.parse as urlparse

def request_derivative(equation: str, variables: dict):
    wolfree_url = "" +\
        "https://api.wolframalpha.com/v2/query?"+\
        "&callback=jQuery36108552903897608751_1666553041562"+\
        "&output=json"+\
        "&reinterpret=true"+\
        "&scantimeout=30"+\
        "&podtimeout=30"+\
        "&formattimeout=30"+\
        "&parsetimeout=30"+\
        "&totaltimeout=30"+\
        "&podstate=Step-by-step%20solution"+\
        "&podstate=Step-by-step"+\
        "&podstate=Show%20all%20steps"+\
        "&i2d=true"+\
        "&input={request_input}"+\
        "&appid=H9V325-HTALUWHKGK"+\
        "&_=1666553041563"
    
    request_structure = '[{"t":0,"v":"sqrt("},'
    
    for var in variables:
        error = variables[var]["error"]
        
        request_structure += f'{{"t":3,"c":[[{{"t":0,"v":"("}},{{"t":48,"c":[[{{"t":0,"v":"{equation}"}}],[{{"t":0,"v":"x"}}]]}},{{"t":0,"v":"*{error})"}}],[{{"t":0,"v":"2"}}]]}},'
        if var != list(variables.keys())[-1]:
            request_structure += '{"t":0,"v":"+"},'
    
    request_structure += '{"t":0,"v":")"}'
    
    for var in variables:
        value = variables[var]["value"]
        request_structure += f',{{"t":0,"v":",{var}={value}"}}'
    
    request_structure += ']'
    
    request_input = base64.b64encode(bytes(request_structure, 'utf-8'))
    request_input = urlparse.quote_plus(request_input)
    
    print(request_input)

    r = requests.get(wolfree_url.format(request_input=request_input))
    data = r.text[:-2]
    data = data.replace(urlparse.parse_qs(urlparse.urlparse(r.url).query)["callback"][0], "")
    data = data[1:]
    
    data = json.loads(data)
    solution = ""
    for pod in data["queryresult"]["pods"]:
        if pod["title"] == "Substitution":
            solution = pod["subpods"][0]["plaintext"]
            break
    
    return solution
    
    
def main():
    equation = "x + y + ln(x/y)^2"
    variables = {
        "x": {
            "value": 1,
            "error": 0.1
        },
        "y": {
            "value": 1,
            "error": 0.1
        },
    }
    solution = request_derivative(equation, variables)
    print(solution)

if __name__ == "__main__":
    main()

# for x_n in variables:
    


# print(x, y)   

# plt.plot(x, y, color="red", marker=".", linestyle="-")
# plt.xlabel("$\infty$")
# plt.ylabel("Lol2")
# plt.show()