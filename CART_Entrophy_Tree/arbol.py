class Arbol:

    def __init__(self,c,j,r,hijo_iz,hijo_der):
        self.c = c
        self.j = j
        self.r = r
        self.hijo_iz = hijo_iz
        self.hijo_der = hijo_der
        if hijo_iz == None or hijo_der == None :
            self.esTerminal = True
        else:
            self.esTerminal = False


  