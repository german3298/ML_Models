import arbol as ar; import numpy as np
import math;

def __crea_nodo(c,j,r,iz,der):
    nuevo = ar.Arbol(c,j,r,iz,der)
    return nuevo

#O(D N log N) (por el método mejor division)
#Recibe lista de muestras etiquetadas, epsilon, y si las etiquetas tienen strings o floats
def ADC(lista_muestras,epsilon):
    j_estrella,r_estrella,decrem_estrella = __mejor_division(lista_muestras)
    if decrem_estrella < epsilon:       # Si el decremento es menor que epsilon, se crea nodo terminal
         c_estrella = __clase_dominante(lista_muestras)
         return __crea_nodo(c_estrella,None,None,None,None)
    else:                               # Si el decremento es mayor que epsilon, se dividen los nodos en dos listas y se crea el nodo
        numero_muestras,dimension_muestras = lista_muestras.shape
        lista_muestras_iz = np.zeros((0,dimension_muestras))
        lista_muestras_der = np.zeros((0,dimension_muestras))
        #Division de nodos en dos listas
        for n in range(numero_muestras):
            muestra_et = lista_muestras[n,:dimension_muestras]
            valor_j = muestra_et[j_estrella]
            muestra_dimensionada = np.reshape(muestra_et,(1,dimension_muestras))
            if valor_j <= r_estrella:
                lista_muestras_iz = np.concatenate((lista_muestras_iz,muestra_dimensionada))
            else:
                lista_muestras_der = np.concatenate((lista_muestras_der,muestra_dimensionada))
        #Se crean recursivamente los hijos del nodo creado:
        arbol_iz = ADC(lista_muestras_iz,epsilon)
        arbol_der = ADC(lista_muestras_der,epsilon)
        return __crea_nodo(None,j_estrella,r_estrella,arbol_iz,arbol_der)

#O(N)
def __clase_dominante(lista_muestras):
    numero_muestras,dimension_muestras = lista_muestras.shape
    lista_clases = np.unique(lista_muestras[:,dimension_muestras-1])
    contador_mayor = np.zeros((lista_clases.shape[0]))
    for n in range(numero_muestras):
        cn = np.where(lista_clases==lista_muestras[n, dimension_muestras-1])[0][0]
        contador_mayor[cn] += 1
    #Buscamos la posición del elemento que más se repite y devolvemos la clase de esa posición
    posicion_maximo = np.where(contador_mayor == np.amax(contador_mayor))
    return lista_clases[posicion_maximo]

#O(D N log N)
def __mejor_division(lista_muestras):
    numero_muestras,dimension_muestras = lista_muestras.shape
    decrem_estrella = 0
    j_estrella = None
    r_estrella = None
    lista_clases = np.unique(lista_muestras[:,dimension_muestras-1])
    numero_clases = lista_clases.shape[0]
    #Calculamos la entropia de este nodo en un principio:
    contador_elementos_total = np.zeros((numero_clases))
    #Para la entropia, calculamos un array con el número de elementos de cada clase
    for n in range(numero_muestras):
        pos_label = np.where(lista_clases==lista_muestras[n, dimension_muestras-1])[0][0]
        contador_elementos_total[pos_label] += 1
    sum = 0
    #Formula de la entropía
    for m in range(numero_clases):
        prob = contador_elementos_total[m]/numero_muestras
        if (prob != 0):
            sum += prob*math.log2(prob)
    entropia_nodo_padre = -sum
    #Recorremos cada j por cada muestra O(D N log N)
    for j in range(dimension_muestras-1):
        #Ordenar las muestras en función de cada j, por eficiencia O(N log N)
        lista_muestras = lista_muestras[lista_muestras[:,j].argsort()]
        # Copiamos la lista ya ordenada antes de numero de elementos por cada clase y creamos otra con ceros para las muestras que vayan al hijo izquierdo
        contador_elementos_hijo_izq = np.zeros((numero_clases))
        contador_elementos_hijo_der = np.copy(contador_elementos_total)
        # Recorremos las muestras - 1(en el último todos los nodos habrían ido a un mismo nodo hijo, en cuyo caso el decremento de impureza sería 0)
        for n in range(numero_muestras-1):
            r = lista_muestras[n,j]
            # Para calcular la entropia, ajustamos la lista de elementos de cada hijo (sabiendo que las muestras están ordenadas por j)
            pos_label = np.where(lista_clases==lista_muestras[n, dimension_muestras-1])[0][0]
            contador_elementos_hijo_izq[pos_label] += 1
            contador_elementos_hijo_der[pos_label] -= 1
            # Si el r del siguiente elemento es igual que el de este, pasamos a la siguiente iteración
            # Si es la penultima muestra, el siguiente será la última muestra, por lo que el decremento de impureza sería 0 (irían todos los nodos a un mismo hijo)
            # En el caso de la penultima muestra, habría que hacer un "break", pero como es la ultima de este bucle, funciona igual el "continue"
            r_siguiente = lista_muestras[n+1,j]
            if r_siguiente == r:
                continue
            # REFINAMIENTO: Calculamos la media entre este r y el siguiente, para añadir todo el margen posible
            r = (r+r_siguiente)/2.0
            # Obtenemos el número total de muestras que ha ido a cada hijo (sabiendo que las muestras están ordenadas por j)
            total_muestras_izq = n+1
            total_muestras_der = numero_muestras-(n+1)
            # Calculamos la entropía de cada hijo (aprovechando el mismo bucle para ambos hijos):
            sum_izq = 0
            sum_der = 0
            for m in range(numero_clases):
                prob_izq = contador_elementos_hijo_izq[m]/total_muestras_izq
                if (prob_izq != 0):
                    sum_izq += prob_izq*math.log2(prob_izq)
                prob_der = contador_elementos_hijo_der[m]/total_muestras_der
                if (prob_der != 0):
                    sum_der += prob_der*math.log2(prob_der)
            entropia_nodo_hijo_izq = -sum_izq
            entropia_nodo_hijo_der = -sum_der
            #Calculamos la probabilidad a posteriori de que un elemento vaya a cada hijo
            prob_hijo_izq = total_muestras_izq/numero_muestras
            prob_hijo_der = total_muestras_der/numero_muestras
            #Calculamos el decremento de impureza
            decrem = entropia_nodo_padre - (prob_hijo_izq*entropia_nodo_hijo_izq) - (prob_hijo_der*entropia_nodo_hijo_der)
            #Si el decremento es el mayor hasta ahora, se guardan los valores
            if (decrem > decrem_estrella):
                decrem_estrella = decrem
                j_estrella = j
                r_estrella = r
    return j_estrella,r_estrella,decrem_estrella
    


  
