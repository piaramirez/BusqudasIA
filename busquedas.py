"""
UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO - FES ARAGÓN
MATERIA: Inteligencia Artificial
GRUPO: 2907
DOCENTE: MARTIN ROMERO UGALDE

INTEGRANTES (orden alfabético por apellido):
- Flores Felix, Omar Victor
- Ramírez Alcántara, Pedro Antonio

PROGRAMA: 5 BÚSQUEDAS EN UN SOLO ARCHIVO
- BPA: Búsqueda a lo ancho
- BPP: Búsqueda en profundidad
- BES: Escalada simple
- BEMP: Escalada máxima pendiente
- BPM: Primero el mejor (A*)
"""

import customtkinter as ctk
import time
import threading
import collections
import heapq


class GrafoCompleto:
    """Clase que contiene el grafo y los 5 algoritmos de búsqueda"""
    
    def __init__(self):
        # LISTA DE ADYACENCIA (grafo de 28 nodos)
        self.adyacencia = {
            1: [6, 13, 4],
            2: [22, 12, 9],
            3: [14, 23, 19, 18],
            4: [9, 1, 13],
            5: [15, 11],
            6: [16, 1],
            7: [27, 8, 11],
            8: [27, 15, 7],
            9: [28, 2, 17, 4, 24],
            10: [],
            11: [7, 5],
            12: [],
            13: [4, 1, 24],
            14: [23, 3],
            15: [8, 24, 5],
            16: [],
            17: [],
            18: [21, 22, 28, 27],
            19: [],
            20: [],
            21: [18, 22, 28, 27],
            22: [23, 2, 28, 21],
            23: [14, 3, 22],
            24: [9, 13, 15],
            25: [],
            26: [],
            27: [21, 28, 8, 7],
            28: [27, 21, 22, 2, 9, 24, 18],
        }
        
        # HEURISTICAS (distancia estimada al nodo 18)
        self.heuristica = {
            1: 1000, 2: 514, 3: 200, 4: 900, 5: 1050, 6: 1100, 7: 826,
            8: 606, 9: 450, 10: 9999, 11: 950, 12: 9999, 13: 850, 14: 250,
            15: 928, 16: 9999, 17: 9999, 18: 0, 19: 9999, 20: 9999,
            21: 89, 22: 514, 23: 9999, 24: 255, 25: 9999, 26: 9999,
            27: 351, 28: 469
        }
        
        # DISTANCIAS REALES (extraídas de la tabla del PDF)
        self.distancias = {
            (1,2): 908, (1,3): 117, (1,4): 515, (1,6): 687, (1,7): 448,
            (1,8): 886, (1,9): 4, (1,13): 922, (1,15): 117, (1,18): 804,
            (2,9): 889, (2,12): 1373, (2,22): 1013, (2,28): 1811,
            (3,14): 250, (3,18): 200, (3,19): 480, (3,23): 117,
            (4,9): 181, (4,13): 1319,
            (5,11): 580, (5,15): 928,
            (6,16): 500,
            (7,8): 826, (7,11): 950, (7,27): 351,
            (8,15): 1000, (8,27): 500,
            (9,24): 255, (9,28): 469,
            (11,15): 800,
            (13,24): 600,
            (14,23): 300,
            (15,24): 400,
            (18,21): 89, (18,22): 514, (18,27): 351, (18,28): 469,
            (21,22): 200, (21,27): 150, (21,28): 180,
            (22,23): 300, (22,28): 250,
            (27,28): 100,
        }
    
    def obtener_distancia(self, a, b):
        """Obtiene la distancia real entre dos nodos"""
        if a == b:
            return 0
        if (a, b) in self.distancias:
            return self.distancias[(a, b)]
        if (b, a) in self.distancias:
            return self.distancias[(b, a)]
        if b in self.adyacencia.get(a, []):
            return self.heuristica.get(b, 9999)
        return 9999
    
    def obtener_vecinos(self, nodo, horario=True):
        """Obtiene vecinos en orden horario o antihorario"""
        vecinos = self.adyacencia.get(nodo, [])
        vecinos = [v for v in vecinos if v != 0]
        return vecinos if horario else vecinos[::-1]
    
    def bpa(self, inicio, meta, horario=True):
        """Búsqueda a lo ancho (BFS) - Usa cola FIFO"""
        cola = collections.deque([[inicio]])
        visitados = []
        while cola:
            ruta = cola.popleft()
            nodo = ruta[-1]
            if nodo not in visitados:
                visitados.append(nodo)
                if nodo == meta:
                    return ruta, visitados, ruta
                for v in self.obtener_vecinos(nodo, horario):
                    if v not in visitados:
                        cola.append(ruta + [v])
        return None, visitados, visitados if visitados else [inicio]
    
    def bpp(self, inicio, meta, horario=True):
        """Búsqueda en profundidad (DFS) - Usa pila LIFO"""
        pila = [[inicio]]
        visitados = []
        while pila:
            ruta = pila.pop()
            nodo = ruta[-1]
            if nodo not in visitados:
                visitados.append(nodo)
                if nodo == meta:
                    return ruta, visitados, ruta
                for v in reversed(self.obtener_vecinos(nodo, horario)):
                    if v not in visitados:
                        pila.append(ruta + [v])
        return None, visitados, visitados if visitados else [inicio]
    
    def escalada_simple(self, inicio, meta, horario=True):
        """Escalada simple - Toma el primer vecino que mejora la heurística"""
        actual = inicio
        ruta = [actual]
        visitados = [actual]
        while actual != meta:
            vecinos = self.obtener_vecinos(actual, horario)
            mejoro = False
            for v in vecinos:
                if self.heuristica.get(v, 9999) < self.heuristica.get(actual, 9999):
                    actual = v
                    ruta.append(actual)
                    visitados.append(actual)
                    mejoro = True
                    break
            if not mejoro:
                return None, visitados, ruta
        return ruta, visitados, ruta
    
    def escalada_maxima(self, inicio, meta, horario=True):
        """Escalada máxima pendiente - Toma el mejor vecino (el que más mejora)"""
        actual = inicio
        ruta = [actual]
        visitados = [actual]
        while actual != meta:
            vecinos = self.obtener_vecinos(actual, horario)
            if not vecinos:
                return None, visitados, ruta
            mejor = None
            mejor_h = self.heuristica.get(actual, 9999)
            for v in vecinos:
                h = self.heuristica.get(v, 9999)
                if h < mejor_h:
                    mejor_h = h
                    mejor = v
            if mejor and mejor_h < self.heuristica.get(actual, 9999):
                actual = mejor
                ruta.append(actual)
                visitados.append(actual)
            else:
                return None, visitados, ruta
        return ruta, visitados, ruta
    
    def primero_mejor(self, inicio, meta, horario=True):
        """Primero el mejor (A*) - Usa f(n) = g(n) + h(n)"""
        cont = 0
        heap = []
        g = 0
        f = g + self.heuristica.get(inicio, 9999)
        heapq.heappush(heap, (f, cont, inicio, [inicio], g))
        visitados = {}
        cont += 1
        while heap:
            f_act, _, nodo, ruta, g_act = heapq.heappop(heap)
            if nodo in visitados and visitados[nodo] <= g_act:
                continue
            visitados[nodo] = g_act
            if nodo == meta:
                return ruta, list(visitados.keys()), ruta
            for v in self.obtener_vecinos(nodo, horario):
                costo = self.obtener_distancia(nodo, v)
                if costo >= 9999:
                    continue
                g_nuevo = g_act + costo
                h_v = self.heuristica.get(v, 9999)
                f_nuevo = g_nuevo + h_v
                if v not in visitados or visitados[v] > g_nuevo:
                    heapq.heappush(heap, (f_nuevo, cont, v, ruta + [v], g_nuevo))
                    cont += 1
        return None, list(visitados.keys()), list(visitados.keys()) if visitados else [inicio]


class AppBusquedasFES(ctk.CTk):
    """Interfaz gráfica principal"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Búsquedas IA - FES Aragón")
        self.geometry("1200x750")
        ctk.set_appearance_mode("dark")
        
        self.grafo = GrafoCompleto()
        self.animacion_en_curso = False
        
        # Layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
        
        # ==================== SIDEBAR ====================
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="CONFIGURACIÓN", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        self.algo_var = ctk.StringVar(value="BPA")
        algoritmos = [
            ("BPA - Anchura", "BPA"),
            ("BPP - Profundidad", "BPP"),
            ("BES - Escalada Simple", "BES"),
            ("BEMP - Escalada Máxima", "BEMP"),
            ("BPM - Primero el Mejor", "BPM")
        ]
        
        for texto, valor in algoritmos:
            ctk.CTkRadioButton(self.sidebar, text=texto, 
                              variable=self.algo_var, value=valor).pack(anchor="w", padx=35, pady=3)
        
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#333").pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="Nodo Inicial (NI):").pack(anchor="w", padx=20, pady=(10,0))
        self.ni_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 1", width=180)
        self.ni_entry.pack(pady=5, padx=20)
        
        ctk.CTkLabel(self.sidebar, text="Nodo Final (NF):").pack(anchor="w", padx=20, pady=(10,0))
        self.nf_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 18", width=180)
        self.nf_entry.pack(pady=5, padx=20)
        
        ctk.CTkLabel(self.sidebar, text="Sentido de búsqueda:").pack(anchor="w", padx=20, pady=(10,0))
        self.sentido_var = ctk.StringVar(value="Horario")
        self.combo_sentido = ctk.CTkComboBox(self.sidebar, 
                                            values=["Horario", "Antihorario"],
                                            variable=self.sentido_var, width=180)
        self.combo_sentido.pack(pady=5, padx=20)
        
        self.btn_iniciar = ctk.CTkButton(self.sidebar, text="▶ INICIAR BÚSQUEDA", 
                                        command=self.iniciar_busqueda,
                                        fg_color="#1f538d", height=40)
        self.btn_iniciar.pack(pady=20, padx=20)
        
        self.btn_limpiar = ctk.CTkButton(self.sidebar, text="🗑 LIMPIAR", 
                                        command=self.limpiar, fg_color="#555", height=35)
        self.btn_limpiar.pack(pady=5, padx=20)
        
        # ==================== CANVAS ====================
        self.canvas_frame = ctk.CTkFrame(self, corner_radius=10)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=5, pady=5)
        
        # ==================== BITÁCORA ====================
        self.log_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.log_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.log_frame, text="BITÁCORA", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.log_text = ctk.CTkTextbox(self.log_frame, font=ctk.CTkFont(size=11), wrap="word")
        self.log_text.pack(expand=True, fill="both", padx=10, pady=10)
        
        # ==================== POSICIONES DE NODOS ====================
        self.posiciones = {
            1: (100, 80), 2: (350, 80), 3: (600, 80), 4: (150, 180),
            5: (100, 280), 6: (200, 80), 7: (300, 280), 8: (400, 280),
            9: (450, 180), 10: (700, 180), 11: (200, 380), 12: (450, 80),
            13: (250, 180), 14: (550, 180), 15: (500, 280), 16: (300, 80),
            17: (600, 280), 18: (650, 450), 19: (750, 350), 20: (800, 250),
            21: (550, 380), 22: (450, 380), 23: (350, 450), 24: (350, 250),
            25: (700, 150), 26: (250, 500), 27: (450, 550), 28: (550, 550)
        }
        
        self.nodos_id = {}
        self.dibujar_grafo()
    
    def log(self, mensaje):
        """Agrega un mensaje a la bitácora con timestamp"""
        import datetime
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{hora}] {mensaje}\n")
        self.log_text.see("end")
        self.update_idletasks()
    
    def dibujar_grafo(self):
        """Dibuja el grafo completo en el canvas"""
        self.canvas.delete("all")
        
        # Dibujar aristas
        for nodo, vecinos in self.grafo.adyacencia.items():
            if nodo in self.posiciones:
                x1, y1 = self.posiciones[nodo]
                for vecino in vecinos:
                    if vecino in self.posiciones:
                        x2, y2 = self.posiciones[vecino]
                        self.canvas.create_line(x1, y1, x2, y2, fill="#444", width=1.5)
        
        # Dibujar nodos
        for nodo, (x, y) in self.posiciones.items():
            circulo = self.canvas.create_oval(x-18, y-18, x+18, y+18, 
                                              fill="#2b2b2b", outline="#666", width=2)
            self.canvas.create_text(x, y, text=str(nodo), fill="white", font=("Arial", 11, "bold"))
            self.nodos_id[nodo] = circulo
    
    def pintar_nodo(self, nodo, color):
        """Cambia el color de un nodo en el canvas"""
        if nodo in self.nodos_id:
            self.canvas.itemconfig(self.nodos_id[nodo], fill=color)
        self.update_idletasks()
    
    def limpiar(self):
        """Limpia la bitácora y reinicia el grafo"""
        self.log_text.delete("1.0", "end")
        self.dibujar_grafo()
        self.log("Interfaz limpiada. Listo para nueva búsqueda.")
    
    def iniciar_busqueda(self):
        """Inicia la búsqueda con los parámetros seleccionados"""
        if self.animacion_en_curso:
            self.log("⚠️ Ya hay una búsqueda en curso. Espera a que termine.")
            return
        
        ni = self.ni_entry.get().strip()
        nf = self.nf_entry.get().strip()
        
        if not ni or not nf:
            self.log("❌ ERROR: Debes ingresar nodo inicial y nodo final.")
            return
        
        try:
            inicio = int(ni)
            meta = int(nf)
        except ValueError:
            self.log("❌ ERROR: Los nodos deben ser números enteros.")
            return
        
        if inicio not in self.posiciones or meta not in self.posiciones:
            self.log(f"❌ ERROR: El nodo {inicio} o {meta} no existe en el grafo.")
            return
        
        sentido_horario = self.sentido_var.get() == "Horario"
        algoritmo = self.algo_var.get()
        
        algoritmos_map = {
            "BPA": self.grafo.bpa,
            "BPP": self.grafo.bpp,
            "BES": self.grafo.escalada_simple,
            "BEMP": self.grafo.escalada_maxima,
            "BPM": self.grafo.primero_mejor
        }
        
        self.log("=" * 50)
        self.log(f"🚀 INICIANDO BÚSQUEDA:")
        self.log(f"   Algoritmo: {algoritmo}")
        self.log(f"   Nodo Inicial: {inicio}")
        self.log(f"   Nodo Final: {meta}")
        self.log(f"   Sentido: {'Horario' if sentido_horario else 'Antihorario'}")
        self.log("=" * 50)
        
        self.dibujar_grafo()
        self.animacion_en_curso = True
        
        def ejecutar():
            try:
                ruta, visitados, ruta_parcial = algoritmos_map[algoritmo](inicio, meta, sentido_horario)
                
                # Animar nodos visitados
                for nodo in visitados:
                    self.pintar_nodo(nodo, "#d4af37")
                    time.sleep(0.1)
                
                if ruta:
                    self.log(f"✅ ¡META ENCONTRADA!")
                    self.log(f"📌 Ruta completa: {' → '.join(map(str, ruta))}")
                    self.log(f"📊 Longitud de la ruta: {len(ruta)} nodos")
                    for nodo in ruta:
                        self.pintar_nodo(nodo, "#27ae60")
                    self.pintar_nodo(inicio, "#2980b9")
                    self.pintar_nodo(meta, "#c0392b")
                else:
                    self.log(f"⚠️ NO se encontró ruta completa a {meta}")
                    self.log(f"📌 Ruta parcial: {' → '.join(map(str, ruta_parcial))}")
                    for nodo in ruta_parcial:
                        self.pintar_nodo(nodo, "#e67e22")
                    self.pintar_nodo(inicio, "#2980b9")
                
                self.log("=" * 50)
            except Exception as e:
                self.log(f"❌ ERROR: {e}")
            finally:
                self.animacion_en_curso = False
                self.log("🏁 Búsqueda finalizada.")
        
        threading.Thread(target=ejecutar, daemon=True).start()


# ==================== PUNTO DE ENTRADA ====================
if __name__ == "__main__":
    app = AppBusquedasFES()
    app.mainloop()