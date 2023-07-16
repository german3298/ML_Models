import arbol; import math
import numpy as np; import sys
from arbol_decision import ADC
from arbol_predecir import arbol_predecir
from confus import confus


if len(sys.argv) != 3:
    print('Argumentos para ejecutar: %s <data> <epsilon>' % sys.argv[0])  
    sys.exit(1)
datos = np.loadtxt(sys.argv[1])
epsilon = float(sys.argv[2])
# Parámetros de los datos
N,L = datos.shape; D = L-1
# Barajar datos
np.random.seed(23)
permutacion = np.random.permutation(N)
datos = datos[permutacion]
# Establecer conjunto de entrenamiento y de test
NTr=int(round(.7*N));
entrenamiento = datos[:NTr,:];
M=N-NTr;
test = datos[NTr:,:];
# Imprimir cabeceras
print('#  Eps Ete Ete(%)    Ite (%)');
print('# ---- --- ------ ----------');
# Crear árbol con muestras de entrenamiento
arbol_solucion = ADC(entrenamiento,epsilon)
predicciones = np.zeros((M,1))
for m in range(M):
    predicciones[m] = arbol_predecir(arbol_solucion,test[m,:D])
numero_errores, matrix_confusion = confus(test[:,D].reshape(M,1),predicciones)
prob_error = (numero_errores/M)
r =1.96*math.sqrt(prob_error*(1-prob_error)/M)
min_prob= (prob_error-r)*100
max_prob= (prob_error+r)*100
print('%6.2f %3d %6.1f [%.1f, %.1f]' % (epsilon,numero_errores, prob_error*100, min_prob, max_prob));








    


  
