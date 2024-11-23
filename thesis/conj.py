from math import factorial
from sage.all import * 

def f(d,n):
    total = 0
    for comp in IntegerVectors(n, d+1):
        term = 1
        for i in range(d+1): 
            term *= factorial(n-comp[i])/(factorial(comp[i])**d)
        total += term
    return int(total)

table = ''
for d in range(1,6):
    row = f''
    for n in range(1,6):
        total = f(d,n)
        row += str(total) + ' | '
    table += row + '\n'
print(table)
