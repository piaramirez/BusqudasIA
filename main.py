import customtkinter as ctk
import time
from collections import deque

class AppBusquedasFES(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Búsquedas IA - Padrino Edition")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")

        # --- DATOS DEL GRAFO (Extraídos de tus archivos) ---
        self.adyacencia = {
            '1': ['6', '13', '4'], '2': ['22', '12', '9'], '3': ['14', '23', '19', '18'],
            '4': ['9', '1', '13'], '5': ['15', '11'], '6': ['16', '1'],
            '7': ['27', '8', '11'], '8': ['27', '15', '7'], '9': ['28', '2', '17', '4', '24'],
            '11': ['7', '5'], '13': ['4', '1', '24'], '14': ['23', '3'], '15': ['8', '24', '5'],
            '18': ['14', '3', '21'], '21': ['18', '22', '28', '27'], '22': ['23', '2', '28', '21'],
            '24': ['9', '13', '15'], '27': ['21', '28', '8', '7'], '28': ['27', '21', '22', '2', '9', '8']
        }
        
        # Heurísticas (Valores h - Distancia al 18)
        self.heuristica = {
            '1': 1000, '2': 514, '3': 200, '4': 900, '5': 1050, '6': 1100, '7': 826, '8': 606, 
            '9': 450, '11': 950, '13': 850, '14': 250, '15': 928, '18': 0, '21': 89, '22': 514, 
            '24': 255, '27': 351, '28': 469
        }

        # Coordenadas para el Canvas (Layout para que se vea bonito)
        self.pos = {
            '1': (50, 50), '6': (150, 50), '16': (250, 50), '13': (50, 150), '4': (150, 150),
            '9': (250, 150), '2': (350, 150), '12': (450, 150), '5': (50, 250), '11': (150, 250),
            '7': (250, 250), '8': (350, 250), '15': (450, 250), '24': (550, 250), '27': (350, 350),
            '28': (450, 350), '21': (250, 450), '18': (350, 450), '14': (450, 450), '3': (550, 450),
            '22': (150, 450), '23': (50, 450), '17': (650, 150), '19': (650, 350)
        }

        # --- ESTRUCTURA DE LA INTERFAZ ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Controles)
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="CONFIGURACIÓN", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.algo_var = ctk.StringVar(value="BPA")
        algos = [("Anchura (BPA)", "BPA"), ("Profundidad (BPP)", "BPP"), 
                 ("Escalada Simple (BES)", "BES"), ("Máxima Pendiente (BEMP)", "BEMP"), 
                 ("Primero el Mejor (BPM)", "BPM")]
        for t, v in algos:
            ctk.CTkRadioButton(self.sidebar, text=t, variable=self.algo_var, value=v).pack(anchor="w", padx=20, pady=5)

        self.ni_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Nodo Inicial (NI)")
        self.ni_entry.pack(pady=10, padx=20)
        self.nf_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Nodo Final (NF)")
        self.nf_entry.pack(pady=10, padx=20)
        
        self.sentido_var = ctk.StringVar(value="Horario")
        self.combo_sentido = ctk.CTkComboBox(self.sidebar, values=["Horario", "Antihorario"], variable=self.sentido_var)
        self.combo_sentido.pack(pady=10)

        ctk.CTkButton(self.sidebar, text="ANIMAR", command=self.iniciar_busqueda, fg_color="#1f538d").pack(pady=20)

        # 2. Canvas (Grafo)
        self.canvas = ctk.CTkCanvas(self, bg="#1a1a1a", highlightthickness=0)
        self.canvas.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 3. Bitácora (Resultados)
        self.log_frame = ctk.CTkFrame(self, width=250)
        self.log_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(self.log_frame, text="BITÁCORA", font=("Arial", 16, "bold")).pack(pady=5)
        self.log_text = ctk.CTkTextbox(self.log_frame, width=230, font=("Consolas", 11))
        self.log_text.pack(expand=True, fill="both", padx=5, pady=5)

        self.dibujar_grafo_base()

    def log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def dibujar_grafo_base(self):
        self.canvas.delete("all")
        self.nodos_id = {}
        # Dibujar aristas
        for u, vecinos in self.adyacencia.items():
            if u in self.pos:
                x1, y1 = self.pos[u]
                for v in vecinos:
                    if v in self.pos:
                        x2, y2 = self.pos[v]
                        self.canvas.create_line(x1, y1, x2, y2, fill="#333", width=1)
        # Dibujar nodos
        for nodo, (x, y) in self.pos.items():
            circ = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="#2b2b2b", outline="#555")
            self.canvas.create_text(x, y, text=nodo, fill="white", font=("Arial", 9, "bold"))
            self.nodos_id[nodo] = circ

    def obtener_sucesores(self, nodo, horario=True):
        sucs = self.adyacencia.get(nodo, [])
        return sucs if horario else sucs[::-1]

    def iniciar_busqueda(self):
        self.dibujar_grafo_base()
        self.log_text.delete("1.0", "end")
        ni, nf = self.ni_entry.get(), self.nf_entry.get()
        horario = self.sentido_var.get() == "Horario"
        algo = self.algo_var.get()
        
        if ni not in self.pos or nf not in self.pos:
            self.log("ERROR: Nodos no válidos.")
            return

        self.log(f"Iniciando {algo}...")
        self.ejecutar_animacion(ni, nf, algo, horario)

    def ejecutar_animacion(self, inicio, meta, tipo, horario):
        # Configuración inicial por tipo
        visitados = []
        if tipo == "BPA": # Queue
            frontera = deque([(inicio, [inicio])])
        elif tipo == "BPP": # Stack
            frontera = [(inicio, [inicio])]
        else: # Heurísticas (BES, BEMP, BPM)
            frontera = [(inicio, [inicio])]

        def paso():
            nonlocal frontera
            if not frontera:
                self.log("FIN: No se encontró ruta.")
                return

            # Extraer nodo según algoritmo
            if tipo == "BPA":
                actual, ruta = frontera.popleft()
            elif tipo == "BPP":
                actual, ruta = frontera.pop()
            elif tipo == "BPM":
                frontera.sort(key=lambda x: self.heuristica.get(x[0], 9999))
                actual, ruta = frontera.pop(0)
            else: # BES y BEMP
                actual, ruta = frontera.pop(0)

            if actual in visitados:
                self.after(300, paso)
                return
            
            visitados.append(actual)
            h_val = self.heuristica.get(actual, "N/A")
            self.log(f"Evaluando: {actual} (h={h_val})")
            self.canvas.itemconfig(self.nodos_id[actual], fill="#d4af37") # Amarillo: Procesando

            if actual == meta:
                self.canvas.itemconfig(self.nodos_id[actual], fill="#27ae60")
                self.log(f"¡META ENCONTRADA!\nRuta: {'->'.join(ruta)}")
                return

            sucesores = self.obtener_sucesores(actual, horario)
            
            if tipo == "BES": # Escalada Simple: El primer mejor vecino
                mejor = None
                for s in sucesores:
                    if self.heuristica.get(s, 9999) < self.heuristica.get(actual, 9999):
                        mejor = s
                        break
                if mejor: frontera = [(mejor, ruta + [mejor])]
            
            elif tipo == "BEMP": # Escalada Máxima: El mejor de todos los vecinos
                mejor = min(sucesores, key=lambda s: self.heuristica.get(s, 9999), default=None)
                if mejor and self.heuristica.get(mejor, 9999) < self.heuristica.get(actual, 9999):
                    frontera = [(mejor, ruta + [mejor])]
            
            else: # BPA, BPP, BPM
                for s in sucesores:
                    if s not in visitados:
                        frontera.append((s, ruta + [s]))

            self.after(600, paso)

        paso()

if __name__ == "__main__":
    app = AppBusquedasFES()
    app.mainloop()