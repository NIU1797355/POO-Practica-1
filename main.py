from __future__ import annotations
import logging
import math
from datetime import datetime 
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox, ttk

# === Fabrica ==========

class Fabrica:
    def __init__(self, marca: str):
        self._marca = marca
        self._lineesProduccio = []
        self._inventariPeces = None
        self._registreProduccio = None
        self._models = []
        self._subministradors = []

        self._comptador_series = 1
        self._index_linea_actual = 0

    def assignarInventari(self, inventari: InventariPeces):
        self._inventariPeces = inventari

    def assignarRegistre(self, registre: RegistreProduccio):
        self._registreProduccio = registre

    def afegirModelCotxe(self, model: ModelCotxe) -> bool:
        try:
            self._models.append(model)
            return True
        except Exception as e:
            logging.error(f"Error en afegir model cotxe: {e}")
            return False

    def afegirModelMoto(self, model: ModelMoto) -> bool:
        try:
            self._models.append(model)
            return True
        except Exception as e:
            logging.error(f"Error en afegir model moto: {e}")
            return False

    def produirVehicle(self, model: ModelVehicle, color: str, data: datetime) -> VehicleProduit:
        if not self._lineesProduccio:
            raise Exception("No hi ha línies de producció assignades a la fàbrica.")
        if self._inventariPeces is None:
            raise Exception("No hi ha inventari assignat.")
        try:
            self._inventariPeces.consumir_peces(model)
        except Exception as e:
            print(f"Error de producció: Falten peces - {e}")
            return None

        linea = self._lineesProduccio[self._index_linea_actual]
        self._index_linea_actual = (self._index_linea_actual + 1) % len(self._lineesProduccio)
        
        vehicle = linea.produirVehicle(model)

        vehicle._numeroSerie = f"SN-{self._comptador_series:05d}"
        self._comptador_series += 1
        vehicle._color = color
        vehicle._dataProduccio = data

        if self._registreProduccio is not None:
            self._registreProduccio.registrarVehicle(vehicle)

        return vehicle

    def afegirLineaProduccio(self, linea_produccio: LineaProduccioVehicle) -> bool:
        if (linea_produccio not in self._lineesProduccio):
            self._lineesProduccio.append(linea_produccio)
            return True
        else:
            raise Exception("Error: linea de produccio ja està a la llista.")

    def es_possible_produir(self, model: ModelVehicle) -> bool:
        if self._inventariPeces is None:
            return False
        for req in model.requisits_peces:
            codi = req.peca.codi
            quantitat_necessaria = req.quantitat
            if codi not in self._inventariPeces._estoc or self._inventariPeces._estoc[codi]['quantitat'] < quantitat_necessaria:
                return False
        return True


# === Main ====
class ModelVehicle(ABC) :
    def __init__(self, nomModel: str, electric: bool, cilindrada:int):
            self._nomModel = nomModel
            self._electric = electric
            self._requisits_peces = dict()
            if cilindrada > 0 :
                self._cilindrada = cilindrada
            else :
                logging.error("La cilindrada ha de ser un nombre major a 0.\n")
                raise ValueError("La cilindrada ha de ser un nombre major a 0.\n")
     
    @abstractmethod        
    def numeroDeRodes(self) :
        pass

    @abstractmethod
    def etiquetaDeContaminacio(self):
        pass

    def afegirRequisitPeca(self, requisit: RequisitPeca):
        if requisit in self._requisits_peces :
            self._requisits_peces[requisit] += 1
        else :
            self._requisits_peces[requisit] = 1
    
    @property
    def requisits_peces(self) -> dict:
        return self._requisits_peces

class LineaProduccioVehicle:
    def __init__(self, id_linea: str):
        self._id_linea = id_linea
    def produirVehicle(self, model: ModelVehicle) -> VehicleProduit:
        return VehicleProduit(numeroSerie="", color="", dataProduccio=None, model=model)

class RegistreProduccio:
    def __init__(self, dataIniciRegistre: datetime):
        self._dataIniciRegistre = dataIniciRegistre
        self._vehicles_registrats = []

    def registrarVehicle(self, vehicle: VehicleProduit):
        self._vehicles_registrats.append(vehicle)

    def nVehiclesProduits(self, model: ModelVehicle, dataInici: datetime, dataFi: datetime) -> int:
        comptador = 0
        for vehicle in self._vehicles_registrats:
            if vehicle._model == model and (dataInici <= vehicle._dataProduccio <= dataFi):
                comptador += 1
        return comptador

    @property
    def vehicles_registrats(self):
        return self._vehicles_registrats

    @property 
    def dataIniciRegistre(self):
        return self._dataIniciRegistre

class VehicleProduit:
    def __init__(self, numeroSerie: str, color: str, dataProduccio: datetime, model: ModelVehicle):
        self._numeroSerie = numeroSerie
        self._color = color
        self._dataProduccio = dataProduccio
        self._model = model

class ModelCotxe(ModelVehicle) :
    def __init__(self,nomModel:str, electric:bool, cilindrada:int,portes:int,canvi:str,combustible:str):
        super().__init__(nomModel,electric,cilindrada)
        self.numeroDePortes = portes
        self.tipusCanviMarxes = canvi
        self.tipusCombustible = combustible

    def numeroDeRodes(self):
        return 4

    def etiquetaDeContaminacio(self):
        if self._electric :
            return "0 Emisions"
        elif self.tipusCombustible.lower() == "gasolina":
            return "C"
        elif self.tipusCombustible.lower() == "diesel" :
            return "B"
        else :
            return "Sense etiqueta"
    
    @property
    def numeroDePortes(self):
        return self._numeroDePortes

    @numeroDePortes.setter
    def numeroDePortes(self, value):
        if value >=2 :
            self._numeroDePortes = value
        else :
            logging.error("El nombre de portes ha de ser com a mínim 2.\n")
            raise ValueError("El número de portes ha de ser com a mínim 2.\n")

    @property 
    def tipusCanviMarxes(self) :
        return self._tipusCanviMarxes

    @tipusCanviMarxes.setter
    def tipusCanviMarxes(self, tipus):
        self._tipusCanviMarxes = tipus
    
    @property 
    def tipusCombustible(self):
        return self._tipusCombustible

    @tipusCombustible.setter
    def tipusCombustible(self, tipus):
        self._tipusCombustible = tipus

class ModelMoto(ModelVehicle):
    def __init__(self,nomModel:str, electric:bool, cilindrada: int, tipusRodes:str, carnetNecessari:str):
        super().__init__(nomModel,electric,cilindrada)
        self.tipusRodes = tipusRodes
        self.carnetNecessari = carnetNecessari

    def numeroDeRodes(self):
        return 2

    def etiquetaDeContaminacio(self):
        if self._electric :
            return "0 Emisions"
        else :
            return "C"
    
    @property 
    def tipusRodes(self):
        return self._tipusRodes

    @tipusRodes.setter
    def tipusRodes(self,value:str):
        self._tipusRodes = value
    
    @property 
    def carnetNecessari(self):
        return self._carnetNecessari

    @carnetNecessari.setter
    def carnetNecessari(self,value:str):
        self._carnetNecessari = value

class Subministrador:
    def __init__(self, nom, cif, adreca, pais):
        self._nom = nom
        self._cif = cif
        self._adreca = adreca
        self._pais = pais

    @property
    def nom(self):
        return self._nom
    @property
    def cif(self):
        return self._cif
    @property
    def adreca(self):
        return self._adreca
    @property
    def pais(self):
        return self._pais

class Peca:
    def __init__(self, codi, nom, descripcio, subministrador: Subministrador):
        self._codi = codi
        self._nom = nom
        self._descripcio = descripcio
        self._subministrador = subministrador

    @property
    def codi(self):
        return self._codi
    @property
    def nom(self):
        return self._nom
    @property
    def subministrador(self):
        return self._subministrador

class RequisitPeca:
    def __init__(self, peca, quantitat, opcional=False, posicio=0):
        self._peca = peca
        self._quantitat = quantitat
        self._opcional = opcional
        self._posicio = posicio

    @property
    def peca(self):
        return self._peca
    @property
    def quantitat(self):
        return self._quantitat

class InventariPeces:
    def __init__(self, data_ultima_revisio):
        self._data_ultima_revisio = data_ultima_revisio
        self._estoc = {} # codi_peca -> dict(peca: Peca, quantitat: int)

    def afegir_estoc(self, peca, quantitat):
        codi = peca.codi
        if codi in self._estoc:
            self._estoc[codi]['quantitat'] += quantitat
        else:
            self._estoc[codi] = {'peca': peca, 'quantitat': quantitat}

    def numExistenciesPeca(self, codiPeca):
        if codiPeca in self._estoc:
            return self._estoc[codiPeca]['quantitat']
        return 0

    def pecesProveidor(self, cif_proveidor):
        peces_prov = []
        for dades in self._estoc.values():
            if dades['peca'].subministrador.cif == cif_proveidor:
                peces_prov.append(dades['peca'])
        return peces_prov

    def consumir_peces(self, model):
        for req in model.requisits_peces:
            codi = req.peca.codi
            quantitat_necessaria = req.quantitat
            
            if codi not in self._estoc or self._estoc[codi]['quantitat'] < quantitat_necessaria:
                raise Exception(f"Estoc insuficient per la peça: {codi}")
                
        for req in model.requisits_peces:
            codi = req.peca.codi
            self._estoc[codi]['quantitat'] -= req.quantitat

class ControllerCreaModel:
    def __init__(self, fabrica):
        self.fabrica = fabrica

    def afegir_model(self, tipus_vehicle, nom, electric, cilindrada, portes, canvi, combustible, tipus_rodes, carnet):
        try:
            # Validem cilindrada
            cil = int(cilindrada) if cilindrada else 0
            
            if tipus_vehicle == "Cotxe":
                portes = int(portes) if portes else 0
                nou_model = ModelCotxe(nom, electric, cil, portes, canvi, combustible)
                self.fabrica.afegirModelCotxe(nou_model)
            elif tipus_vehicle == "Moto":
                nou_model = ModelMoto(nom, electric, cil, tipus_rodes, carnet)
                self.fabrica.afegirModelMoto(nou_model)
            else:
                raise ValueError("Selecciona Cotxe o Moto.")
            return True
        except Exception as e:
            raise e

class ViewCreaModel:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Crear Nou Model de Vehicle")
        self.root.geometry("400x450")

        # Variables
        self.tipus_var = tk.StringVar(value="Cotxe")
        self.nom_var = tk.StringVar()
        self.electric_var = tk.BooleanVar()
        self.cilindrada_var = tk.StringVar()
        
        # Variables Cotxe
        self.portes_var = tk.StringVar()
        self.canvi_var = tk.StringVar()
        self.combustible_var = tk.StringVar()
        
        # Variables Moto
        self.rodes_var = tk.StringVar()
        self.carnet_var = tk.StringVar()

        self.crear_interficie()

    def crear_interficie(self):
        # Tipus de vehicle (Radiobuttons)
        tk.Label(self.root, text="Tipus de Vehicle:").pack(pady=5)
        frame_radios = tk.Frame(self.root)
        frame_radios.pack()
        tk.Radiobutton(frame_radios, text="Cotxe", variable=self.tipus_var, value="Cotxe").pack(side=tk.LEFT)
        tk.Radiobutton(frame_radios, text="Moto", variable=self.tipus_var, value="Moto").pack(side=tk.LEFT)

        # Camps comuns
        tk.Label(self.root, text="Nom del Model:").pack()
        tk.Entry(self.root, textvariable=self.nom_var).pack()

        tk.Checkbutton(self.root, text="És Elèctric?", variable=self.electric_var).pack()

        tk.Label(self.root, text="Cilindrada (cc):").pack()
        tk.Entry(self.root, textvariable=self.cilindrada_var).pack()

        # Camps Cotxe
        tk.Label(self.root, text="--- Camps Cotxe ---").pack(pady=5)
        frame_cotxe = tk.Frame(self.root)
        frame_cotxe.pack()
        tk.Label(frame_cotxe, text="Portes:").grid(row=0, column=0)
        tk.Entry(frame_cotxe, textvariable=self.portes_var, width=10).grid(row=0, column=1)
        tk.Label(frame_cotxe, text="Canvi:").grid(row=1, column=0)
        tk.Entry(frame_cotxe, textvariable=self.canvi_var, width=10).grid(row=1, column=1)
        tk.Label(frame_cotxe, text="Combustible:").grid(row=2, column=0)
        tk.Entry(frame_cotxe, textvariable=self.combustible_var, width=10).grid(row=2, column=1)

        # Camps Moto
        tk.Label(self.root, text="--- Camps Moto ---").pack(pady=5)
        frame_moto = tk.Frame(self.root)
        frame_moto.pack()
        tk.Label(frame_moto, text="Tipus Rodes:").grid(row=0, column=0)
        tk.Entry(frame_moto, textvariable=self.rodes_var, width=10).grid(row=0, column=1)
        tk.Label(frame_moto, text="Carnet:").grid(row=1, column=0)
        tk.Entry(frame_moto, textvariable=self.carnet_var, width=10).grid(row=1, column=1)

        # Botó Afegir
        tk.Button(self.root, text="Afegir Model", command=self.afegir).pack(pady=15)

    def afegir(self):
        try:
            self.controller.afegir_model(
                self.tipus_var.get(),
                self.nom_var.get(),
                self.electric_var.get(),
                self.cilindrada_var.get(),
                self.portes_var.get(),
                self.canvi_var.get(),
                self.combustible_var.get(),
                self.rodes_var.get(),
                self.carnet_var.get()
            )
            messagebox.showinfo("Èxit", "Model afegit correctament a la fàbrica.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No s'ha pogut afegir: {str(e)}")

    def run(self):
        self.root.mainloop()

class ControllerAfegeixPeces:
    def __init__(self, fabrica, inventari):
        self.fabrica = fabrica
        self.inventari = inventari

    def get_llista_models(self):
        return [m._nomModel for m in self.fabrica._models]

    def get_llista_peces(self):
        return [f"{dades['peca'].codi} - {dades['peca'].nom}" for dades in self.inventari._estoc.values()]

    def afegir_peca_a_model(self, nom_model, seleccio_peca, quantitat, opcional, posicio):
        try:
            model_obj = next((m for m in self.fabrica._models if m._nomModel == nom_model), None)
            if not model_obj:
                raise ValueError("Model no trobat.")

            codi_peca = seleccio_peca.split(" - ")[0]
            peca_obj = self.inventari._estoc[codi_peca]['peca']

            quantitat_int = int(quantitat)
            posicio_int = int(posicio) if posicio else 0

            requisit = RequisitPeca(peca_obj, quantitat_int, opcional, posicio_int)
            model_obj.afegirRequisitPeca(requisit)
            return True
        except ValueError as ve:
            raise ValueError(f"Dades invàlides: {ve}")
        except Exception as e:
            raise Exception(f"Error inesperat: {e}")

class ViewAfegeixPeces:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Afegir Peces al Model")
        self.root.geometry("400x350")

        self.model_var = tk.StringVar()
        self.peca_var = tk.StringVar()
        self.quantitat_var = tk.StringVar()
        self.opcional_var = tk.BooleanVar()
        self.posicio_var = tk.StringVar()

        self.crear_interficie()

    def crear_interficie(self):
        tk.Label(self.root, text="Selecciona Model:").pack(pady=5)
        self.combo_models = ttk.Combobox(self.root, textvariable=self.model_var, values=self.controller.get_llista_models(), state="readonly", width=35)
        self.combo_models.pack()

        tk.Label(self.root, text="Selecciona Peça:").pack(pady=5)
        self.combo_peces = ttk.Combobox(self.root, textvariable=self.peca_var, values=self.controller.get_llista_peces(), state="readonly", width=35)
        self.combo_peces.pack()

        frame_dades = tk.Frame(self.root)
        frame_dades.pack(pady=10)

        tk.Label(frame_dades, text="Quantitat:").grid(row=0, column=0, padx=5)
        tk.Entry(frame_dades, textvariable=self.quantitat_var, width=10).grid(row=0, column=1, padx=5)

        tk.Label(frame_dades, text="Posició:").grid(row=1, column=0, padx=5)
        tk.Entry(frame_dades, textvariable=self.posicio_var, width=10).grid(row=1, column=1, padx=5)

        tk.Checkbutton(self.root, text="És Opcional?", variable=self.opcional_var).pack()

        tk.Button(self.root, text="Afegir Peça", command=self.afegir).pack(pady=15)

    def afegir(self):
        try:
            self.controller.afegir_peca_a_model(
                self.model_var.get(),
                self.peca_var.get(),
                self.quantitat_var.get(),
                self.opcional_var.get(),
                self.posicio_var.get()
            )
            messagebox.showinfo("Èxit", "Peça afegida correctament al model.")
            self.quantitat_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()


# ==========================================
# MAIN
# ==========================================

def main():
    print("Iniciant el sistema de gestió de la Fàbrica...")
    
    fabrica = Fabrica("Honda")
    fabrica.afegirLineaProduccio(LineaProduccioVehicle("L1"))
    inventari = InventariPeces(datetime.now())
    registre = RegistreProduccio(datetime.now())
    
    fabrica.assignarInventari(inventari)
    fabrica.assignarRegistre(registre)

    prov_michelin = Subministrador("Michelin", "11111111C", "c/ Tour Eiffel sn", "França")
    prov_sporting = Subministrador("Sporting Wheels", "22222222C", "c/ Big Ben sn", "Anglaterra")
    prov_handle = Subministrador("HandleBarBikes", "33333333C", "c/ Tower Bridge sn", "Anglaterra")
    prov_gearbox = Subministrador("GearBox", "444444444C", "c/ Trafalgar Square sn", "Anglaterra")
    prov_titanium = Subministrador("Titanium", "555555555C", "c/ Muralla Xinesa sn", "Xina")
    prov_aed = Subministrador("AED", "666666666C", "c/ de la boira 5, Vic", "Catalunya")
    prov_honda_m = Subministrador("HondaMotors", "777777777C", "c/ Mont Fuji, Tokio", "Japó")

    p1 = Peca("0001", "Roda davantera de cotxe", "Michelin", prov_michelin)
    p2 = Peca("0002", "Roda posterior de cotxe", "Michelin", prov_michelin)
    p3 = Peca("0003", "Roda davantera de moto", "Michelin", prov_michelin)
    p4 = Peca("0004", "Roda posterior de moto", "Michelin", prov_michelin)
    p5 = Peca("0005", "Volant de cotxe", "Sporting Wheels", prov_sporting)
    p6 = Peca("0006", "Manillar de moto", "HandleBarBikes", prov_handle)
    p7 = Peca("0007", "Caixa de canvis de cotxe", "GearBox", prov_gearbox)
    p8 = Peca("0008", "Caixa de canvis de cotxe elèctric", "GearBox", prov_gearbox)
    p9 = Peca("0009", "Bateria de Liti per cotxe", "Titanium", prov_titanium)
    p10 = Peca("0010", "Bateria de Liti per moto", "Titanium", prov_titanium)
    p11 = Peca("0011", "Carburador de cotxe", "AED", prov_aed)
    p12 = Peca("0012", "Carburador de moto", "AED", prov_aed)
    p13 = Peca("0013", "Motor de cotxe de combustió", "HondaMotors", prov_honda_m)
    p14 = Peca("0014", "Motor de moto de combustió", "HondaMotors", prov_honda_m)
    p15 = Peca("0015", "Motor de cotxe elèctric", "HondaMotors", prov_honda_m)
    p16 = Peca("0016", "Motor de moto elèctric", "HondaMotors", prov_honda_m)

    inventari.afegir_estoc(p1, 40)
    inventari.afegir_estoc(p2, 45)
    inventari.afegir_estoc(p3, 10)
    inventari.afegir_estoc(p4, 10)
    inventari.afegir_estoc(p5, 25)
    inventari.afegir_estoc(p6, 8)
    inventari.afegir_estoc(p7, 27)
    inventari.afegir_estoc(p8, 15)
    inventari.afegir_estoc(p9, 12)
    inventari.afegir_estoc(p10, 21)
    inventari.afegir_estoc(p11, 17)
    inventari.afegir_estoc(p12, 7)
    inventari.afegir_estoc(p13, 5)
    inventari.afegir_estoc(p14, 15)
    inventari.afegir_estoc(p15, 25)
    inventari.afegir_estoc(p16, 35)

    # Aqui comença practica 3
    
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1 - Formulari per nous Models")
        print("2 - Formulari per afegir peces als models")
        print("3 - Sortir")
        opcio = input("Escull una opció (1, 2 o 3): ")

        if opcio == "1":
            controller_model = ControllerCreaModel(fabrica)
            view_model = ViewCreaModel(controller_model)
            view_model.run()
        elif opcio == "2":
            controller_peces = ControllerAfegeixPeces(fabrica, inventari)
            view_peces = ViewAfegeixPeces(controller_peces)
            view_peces.run()
        elif opcio == "3":
            print("\nSortint...")
            break
        else:
            print("Opció no vàlida.")

    print("\nLlista de models existents a la fàbrica al tancar:")
    for m in fabrica._models:
        print(f" - {m._nomModel} ({'Elèctric' if m._electric else 'Combustió'})")

if __name__ == "__main__":
    main()
