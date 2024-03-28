import pickle
   
def parse_regex_to_grammar(regex):
    alphabet = set(filter(str.isalpha, regex))
    grammar = {"<S>": []}
    
    # Create non-terminals for kleene star parts 
    def kleene_non_terminal(char):
        non_terminal = f"<{char.upper()}>"
        grammar[non_terminal] = [char + non_terminal, ""]
        return non_terminal
    
    # This will hold all subexpressions for alternation
    subexpressions = []

    i = 0
    while i < len(regex):
        if regex[i].isalpha():
            alphabet.add(regex[i])
            if i + 1 < len(regex) and regex[i + 1] == '*':
                subexpressions.append(kleene_non_terminal(regex[i]))
                i += 1  # Skip the '*' character
            else:
                subexpressions.append(regex[i])
        # This is to handle the Union part
        elif regex[i] == '|':
            if subexpressions:
                grammar["<S>"].append("".join(subexpressions))
                subexpressions = []
                
        elif regex[i] == '(':
            # Find the matching closing parenthesis
            j = i
            depth = 0
            while j < len(regex):
                if regex[j] == '(':
                    depth += 1
                elif regex[j] == ')':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            
            # Handle the subexpression recursively
            subexpr = regex[i+1:j]
            # Initialize a non-terminal for the subexpression
            sub_nt = f"<SUB{i}>"
            grammar[sub_nt] = []
            parts = subexpr.split('|')

            # Add parts to the subexpression non-terminal, don't include epsilon yet
            for part in parts:
                grammar[sub_nt].append(part)

            # If the entire subexpression is followed by a kleene star,
            # add the recursive part to <S>, but not to sub_nt
            if j + 1 < len(regex) and regex[j + 1] == '*':
                grammar["<S>"].append(sub_nt + "<S>")  # Recursive part
                grammar["<S>"].append("")  # Epsilon part for <S>
                i = j + 1  # Skip the '*' character
            else:
                subexpressions.append(sub_nt)  # No Kleene star, just add the non-terminal

            i = j + 1  # Move past the closing parenthesis
        i += 1
    
    # Add the last set of subexpressions if there are any
    if subexpressions:
        grammar["<S>"].append("".join(subexpressions))
    
    return sorted(list(alphabet)), grammar

# Read regular expression from standard input
regex_input = input("Enter the regular expression: ")

# Parse and generate the grammar
alphabet, grammar = parse_regex_to_grammar(regex_input)

# Output the alphabet and grammar to a pickle file
# output = (alphabet, grammar)
# with open('grammar.pkl', 'wb') as outfile:
#     pickle.dump(output, outfile)

# For testing purposes: print the alphabet and grammar
print("Alphabet:", alphabet)
print("Grammar:", grammar)