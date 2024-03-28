# This function used to check whether any rule in regex
def check_rule(regex):
    if "(" in regex:
        return False
    if ")" in regex:
        return False
    if "*" in regex:
        return False
    if "|" in regex:
        return False

# This function help to make a subexpression to handle nested parenthesis
def make_Subexpression(index, termName):
    if index == 0:
        return "<S>"
    else:
        termName = termName.strip("<>")
        return "<" + termName + "." + str(index) + ">"

def split_String(regex):
    string_sublist = []
    string = ""
    brackCount = 0
    
    for i in range(0, len(regex)):
        char = regex[i]
        if char  == "(":
            if (string != "" and brackCount == 0):
                string_sublist.append(string)
                string = ""
            if (brackCount >= 1):
                string = string + "("
            brackCount += 1
        elif char == ")":
            brackCount -= 1
            if brackCount == 0:
                string_sublist.append(string)
                string = ""
            else:
                string = string + ")"
        elif char == "|":
            if brackCount == 0 and string != "":
                string = string + "|"
                string_sublist.append(string)
                string = ""
            elif string == "":
                h = len(string) - 1
                string_sublist[h] = "(" + string_sublist[h] + ")" + "|"
            else:
                string = string + char
        else: 
            string = string + char
            
        if (i == len(regex) - 1 and string != ""):
            string_sublist.append(string)
    return string_sublist
    
alphabet = []
grammar = {}
index = 0

def recursiveBuild (alphabet, grammar, regex, index, termName):
    string_sublist = split_String(regex)
    term = make_Subexpression(index, termName)
    text = ""
    
    start = make_Subexpression(index, termName)
    
    if (len(string_sublist) != 1):
        index += 1
    
    for i in range(0, len(string_sublist)):
        text = string_sublist[i]
        
        if (len(string_sublist) != 1):
            term = make_Subexpression(index, termName)
            if (grammar.get(start) == None):
                grammar.update({start: [term]})
            else:
                grammar.update({start: [grammar.get(start)[0] + term]})
        
        if (text[-1] == "*"):
            if check_rule(text[0:-1]):
                if (len(text[0:-1] != 1)):
                    text = text[0:-2] + make_Subexpression(index+1, termName)
                    grammar.update({term: [text]})
                    index += 1
                
                term = make_Subexpression(index, termName)
                text = string_sublist[i]
                text = text + term
                grammar.update({term: [text, ""]})
                
                index += 1
            else:
                text = make_Subexpression(index +1, termName)
                text = text + term
                grammar.update({term: [text, ""]})
                text = string_sublist[i]
                index += 1
                index = recursiveBuild(alphabet, grammar, text[0:-2], index, termName)
        else:
            text = string_sublist[i]
            grammar.update({make_Subexpression(index, termName): [text]})
            index += 1
    return index

print("start")
regex = input("Enter expression: ")
recursiveBuild(alphabet, grammar, regex, 0, "term")
print(grammar)