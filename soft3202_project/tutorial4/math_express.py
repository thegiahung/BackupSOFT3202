import random

def expression(depth=0):
    if depth > 3:  # Limit the depth to avoid deep recursion
        return number() # if reach the maximum depth, then just go to term with depth + 1
    else:
        return term(depth+1) + random.choice([" + ", " - "]) + term(depth+1)

def term(depth=0):
    if depth > 3:  # Further limit depth in term
        return number() # expression with depth more than 3 lead to this.
    else:
        return factor(depth+1) + random.choice([" * ", " / "]) + factor(depth+1)

def factor(depth=0):
    if depth > 3:  # Stop recursion by not allowing more expressions within factors
        return number() # term with depth more than 3 lead to this
    else:
        return random.choice([str(number()), "(" + expression(depth+1) + ")"])

def number():
    return str(random.randint(0, 9))

def digit():
    return str(random.randint(0, 9))

for _ in range(10):
    print(expression())