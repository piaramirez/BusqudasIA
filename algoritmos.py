import collections

class GrafoIA:
    def __init__(self):
        # Datos basados en tu ListaAdyacencia.csv
        self.adyacencia = {
            '1': ['6', '13', '4'], '2': ['22', '12', '9'], '3': ['14', '23', '19', '18'],
            '4': ['9', '1', '13'], '5': ['15', '11'], '6': ['16', '1'],
            '7': ['27', '8', '11'], '8': ['27', '15', '7'], '9': ['28', '2', '17', '4', '24'],
            '11': ['7', '5'], '13': ['4', '1', '24'], '15': ['8', '24', '5'],
            '18': ['21', '22', '28', '27'], '21': ['18', '22', '28', '27'],
            '27': ['8', '21', '7'], '28': ['9', '21', '18']
            # Se pueden agregar más nodos según el Excel
        }
        # Heurísticas (h) extraídas de los ejemplos (distancia al nodo 18)
        self.heuristica = {
            '8': 606, '27': 351, '15': 928, '7': 826, '21': 89, 
            '28': 469, '24': 255, '5': 1050, '11': 950, '18': 0, '22': 514
        }

    def obtener_vecinos(self, nodo, horario=True):
        vecinos = self.adyacencia.get(str(nodo), [])
        return vecinos if horario else vecinos[::-1]

    def bpa(self, inicio, meta, horario=True):
        cola = collections.deque([[inicio]])
        visitados = []
        while cola:
            ruta = cola.popleft()
            nodo = ruta[-1]
            if nodo not in visitados:
                visitados.append(nodo)
                if nodo == meta: return ruta, visitados
                for v in self.obtener_vecinos(nodo, horario):
                    if v not in visitados:
                        cola.append(list(ruta) + [v])
        return None, visitados

    def bpp(self, inicio, meta, horario=True):
        pila = [[inicio]]
        visitados = []
        while pila:
            ruta = pila.pop()
            nodo = ruta[-1]
            if nodo not in visitados:
                visitados.append(nodo)
                if nodo == meta: return ruta, visitados
                for v in reversed(self.obtener_vecinos(nodo, horario)):
                    if v not in visitados:
                        pila.append(list(ruta) + [v])
        return None, visitados

    def escalada_simple(self, inicio, meta, horario=True):
        nodo_actual = inicio
        ruta = [nodo_actual]
        visitados = [nodo_actual]
        
        while nodo_actual != meta:
            vecinos = self.obtener_vecinos(nodo_actual, horario)
            encontro_mejor = False
            for v in vecinos:
                if self.heuristica.get(v, 9999) < self.heuristica.get(nodo_actual, 9999):
                    nodo_actual = v
                    ruta.append(nodo_actual)
                    visitados.append(nodo_actual)
                    encontro_mejor = True
                    break
            if not encontro_mejor: break # Se atoró en un máximo local
        return ruta, visitados