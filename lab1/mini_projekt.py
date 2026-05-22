from math import sin, pi, sqrt, exp

# Zadanie:
"""
Przy pomocy w.w. symboli i funkcji zdefiniować:
- cos
- tangens i cotanges
- funkcje hiperboliczne (sin, cos, tan, cotan)
- secans i cosecans
- wszystkie pochodne (pierwszego stopnia) w.w. funkcji
*Opcjonalnie*: użyć biblioteki sympy

Zaproponuj architekturę (ew. obiektową) i logikę wybierania funkcji przez użytkownika w terminalu

Całe rozwiązanie powinno się mieścić w jednym pliku.
Wyświetlać 3 miejsca po przecinku przy pomocy print(f"Wynik: {x}").

"""

def cos(x):
    return sin(x + pi/2)

def tg(x):
    if cos(x) != 0:
        return sin(x)/cos(x)
    
    print("undefined")

def ctg(x):
    if sin(x) != 0:
        return cos(x)/sin(x)
    
    print("undefined")

def sinh(x):
    return (exp(x) - exp(-x))/2

def cosh(x):
    return (exp(x) + exp(-x))/2

def tgh(x):
        return sinh(x)/cosh(x)

def ctgh(x):
    if sinh(x) != 0:
        return cosh(x)/sinh(x)
     
    print("undefined")

def sec(x):
    if cos(x) != 0:
        return 1/cos(x)
    
    print("undefined")

def csc(x):
    if sin(x) != 0:
        return 1/sin(x)
    
    print("undefined")

def dsin(x):
    return cos(x)

def dcos(x):
    return -sin(x)

def dtg(x):
    return sec(x)**2
    

def dctg(x):
    return -(csc(x))**2

def dsec(x):
    return sec(x)*tg(x)

def dcsc(x):
    return -csc(x)*ctg(x)

def dsinh(x):
    return cosh(x)

def dcosh(x):
    return sinh(x)

def dtgh(x):
    return 1/cosh(x)**2

def dctgh(x):
    return -1/sinh(x)**2

fun = [sin, cos, tg, ctg, sinh, cosh, tgh, ctgh, sec, csc, dsin, dcos, dtg, dctg, dsinh, dcosh, dtgh, dctgh, dsec, dcsc]

while True:
    print("Wybierz funkcje:")
    for i, f in enumerate(fun):
        print(f"{i+1:2}. Funkcja: {f.__name__}")

    num = int(input("Podaj numer funkcji: "))
    x = float(input("Podaj argument funkcji: "))
    res = fun[num-1](x)
    print(f"Wynik: {res:.3f}")
    _ = input("Wcisnij dowolny klawisz aby kontynuowac")