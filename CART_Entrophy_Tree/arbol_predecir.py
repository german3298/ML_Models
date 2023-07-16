import numpy as np
import arbol as ar

def arbol_predecir(arbol_entrenado,muestra_sin_etiquetar):
    if arbol_entrenado.esTerminal:
        return arbol_entrenado.c
    if muestra_sin_etiquetar[arbol_entrenado.j] <= arbol_entrenado.r:
        c_estrella = arbol_predecir(arbol_entrenado.hijo_iz, muestra_sin_etiquetar)
    else:
        c_estrella = arbol_predecir(arbol_entrenado.hijo_der, muestra_sin_etiquetar)
    return c_estrella
