def parse_regex_to_grammar(regex):
    # Initialize the alphabet and grammar dictionaries
    alphabet = set()
    grammar = {"<S>": []}
    
    def add_rule(symbol, production):
        if symbol not in grammar:
            grammar[symbol] = []
        grammar[symbol].append(production)
    
    def parse_subexpression(subexp, index):
        # Each subexpression corresponds to a new non-terminal in the grammar
        non_terminal = f"<SUB{index}>"
        grammar[non_terminal] = []
        subexp_parts = subexp.split('|')
        
        for part in subexp_parts:
            if part.isalpha() or part == '#':
                grammar[non_terminal].append(part)
                alphabet.add(part)
        
        return non_terminal
    
    index = 0
    i = 0
    while i < len(regex):
        if regex[i] == '(':
            # Find the matching closing parenthesis
            depth = 1
            j = i + 1
            while j < len(regex) and depth > 0:
                if regex[j] == '(':
                    depth += 1
                elif regex[j] == ')':
                    depth -= 1
                j += 1
            # Recursive call for subexpression
            non_terminal = parse_subexpression(regex[i+1:j-1], index)
            index += 1
            
            # Handle Kleene star after subexpression
            if j < len(regex) and regex[j] == '*':
                grammar["<S>"].append(non_terminal + "<S>")
                grammar["<S>"].append("")  # Epsilon production for kleene star
                j += 1  # Move past the kleene star
            else:
                grammar["<S>"].append(non_terminal)
            
            i = j
        else:
            i += 1  # Ignore other characters (for now)
    
    return sorted(alphabet), grammar

# Example usage with the specific regex
regex = input("Enter the expression: ")
alphabet, grammar = parse_regex_to_grammar(regex)
print("ALPHABET:", alphabet)
print("GRAMMAR", grammar)