from __future__ import annotations
import logging
import math
from datetime import datetime 
from abc import ABC, abstractmethod

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


# EXERCICI 1: DEFINICIÓ DE CLASSES

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

# ==========================================
# EXERCICI 2 I 3: MAIN I CASOS D'ÚS
# ==========================================

def main():
    print("Iniciant el sistema de gestió de la Fàbrica...")
    
    # Inicialitzem entorn
    fabrica = Fabrica("Honda")
    fabrica.afegirLineaProduccio(LineaProduccioVehicle("L1"))
    inventari = InventariPeces(datetime.now())
    registre = RegistreProduccio(datetime.now())
    
    fabrica.assignarInventari(inventari)
    fabrica.assignarRegistre(registre)

    # ---------------------------------------------------------
    # Exercici 2: Creació de proveïdors i peces
    # ---------------------------------------------------------

    prov_michelin = Subministrador("Michelin", "11111111C", "c/ Tour Eiffel sn", "Paris")
    prov_sporting = Subministrador("Sporting Wheels", "22222222C", "c/ Big Ben sn", "Londres")
    prov_handle = Subministrador("Handle BarBikes", "33333333C", "c/ Tower Bridge sn", "Londres")
    prov_gearbox = Subministrador("GearBox", "444444444C", "c/ Trafalgar Square sn", "Londres")
    prov_titanium = Subministrador("Titanium", "555555555C", "c/ Muralla Xinesa sn", "Xangai")
    prov_honda_m = Subministrador("HondaMotors", "666666666C", "c/ Mont Fuji", "Japó")
    prov_aed = Subministrador("AED", "777777777C", "Desconegut", "Desconegut")

    p1 = Peca("0001", "Roda davantera de cotxe", "Roda davantera cotxe", prov_michelin)
    p2 = Peca("0002", "Roda posterior de cotxe", "Roda posterior cotxe", prov_michelin)
    p3 = Peca("0003", "Roda davantera de moto", "Roda davantera moto", prov_michelin)
    p4 = Peca("0004", "Roda posterior de moto", "Roda posterior moto", prov_michelin)
    p5 = Peca("0005", "Volant de cotxe", "Volant de direcció", prov_sporting)
    p6 = Peca("0006", "Manillar de moto", "Manillar de direcció", prov_handle)
    p7 = Peca("0007", "Caixa de canvis de cotxe", "Canvi automàtic/manual", prov_gearbox)
    p8 = Peca("0008", "Caixa de canvis de cotxe elèctric", "Canvi per elèctrics", prov_gearbox)
    p9 = Peca("0009", "Bateria de Liti per cotxe", "Bateria gran", prov_titanium)
    p10 = Peca("0010", "Bateria de Liti per moto", "Bateria petita", prov_titanium)
    p11 = Peca("0011", "Carburador de cotxe", "Carburador cotxe combustio", prov_aed)
    p12 = Peca("0012", "Carburador de moto", "Carburador moto combustio", prov_aed)
    p13 = Peca("0013", "Motor de cotxe de combustió", "Motor gasolina/diesel", prov_honda_m)
    p14 = Peca("0014", "Motor de moto de combustió", "Motor gasolina", prov_honda_m)
    p15 = Peca("0015", "Motor de cotxe elèctric", "Motor elèctric cotxe", prov_honda_m)
    p16 = Peca("0016", "Motor de moto elèctric", "Motor elèctric moto", prov_honda_m)

    inventari.afegir_estoc(p1, 18)
    inventari.afegir_estoc(p2, 18)
    inventari.afegir_estoc(p3, 10)
    inventari.afegir_estoc(p4, 10)
    inventari.afegir_estoc(p5, 5)
    inventari.afegir_estoc(p6, 8)
    inventari.afegir_estoc(p7, 7)
    inventari.afegir_estoc(p8, 15)
    inventari.afegir_estoc(p9, 12)
    inventari.afegir_estoc(p10, 21)
    inventari.afegir_estoc(p11, 17)
    inventari.afegir_estoc(p12, 7)
    inventari.afegir_estoc(p13, 5)
    inventari.afegir_estoc(p14, 15)
    inventari.afegir_estoc(p15, 25)
    inventari.afegir_estoc(p16, 35)

    # ---------------------------------------------------------
    # Exercici 3: Casos d'ús
    # ---------------------------------------------------------

    # =================================================================
    # CAS D'ÚS 1 - Afegir un nou model de vehicle
    # =================================================================

    print("\n--- CAS D'ÚS 1: Afegint models ---")
    
    civic_elec = ModelCotxe("Honda Civic elèctric", True, 1500, 5, "Automàtic", "Elèctric")
    civic_elec.afegirRequisitPeca(RequisitPeca(p1, 2))
    civic_elec.afegirRequisitPeca(RequisitPeca(p2, 2))
    civic_elec.afegirRequisitPeca(RequisitPeca(p5, 1))
    civic_elec.afegirRequisitPeca(RequisitPeca(p8, 1))
    civic_elec.afegirRequisitPeca(RequisitPeca(p9, 1))
    civic_elec.afegirRequisitPeca(RequisitPeca(p15, 1))
    
    civic_comb = ModelCotxe("Honda Civic combustió", False, 2000, 5, "Manual", "Gasolina")
    civic_comb.afegirRequisitPeca(RequisitPeca(p1, 2))
    civic_comb.afegirRequisitPeca(RequisitPeca(p2, 2))
    civic_comb.afegirRequisitPeca(RequisitPeca(p5, 1))
    civic_comb.afegirRequisitPeca(RequisitPeca(p7, 1))
    civic_comb.afegirRequisitPeca(RequisitPeca(p11, 1))
    civic_comb.afegirRequisitPeca(RequisitPeca(p13, 1))

    hrv_comb = ModelCotxe("Honda HR-V combustió", False, 2200, 5, "Automàtic", "Gasolina")
    hrv_comb.afegirRequisitPeca(RequisitPeca(p1, 2))
    hrv_comb.afegirRequisitPeca(RequisitPeca(p2, 2))
    hrv_comb.afegirRequisitPeca(RequisitPeca(p13, 1))

    moto_cbr_e = ModelMoto("Honda CBR elèctrica", True, 600, "Carretera", "A2")
    moto_cbr_e.afegirRequisitPeca(RequisitPeca(p3, 1))
    moto_cbr_e.afegirRequisitPeca(RequisitPeca(p4, 1))
    moto_cbr_e.afegirRequisitPeca(RequisitPeca(p6, 1))
    moto_cbr_e.afegirRequisitPeca(RequisitPeca(p10, 1))
    moto_cbr_e.afegirRequisitPeca(RequisitPeca(p16, 1))

    moto_crm_c = ModelMoto("Honda CRM 75 combustió", False, 75, "Muntanya", "AM")
    moto_crm_c.afegirRequisitPeca(RequisitPeca(p3, 1))
    moto_crm_c.afegirRequisitPeca(RequisitPeca(p4, 1))
    moto_crm_c.afegirRequisitPeca(RequisitPeca(p6, 1))
    moto_crm_c.afegirRequisitPeca(RequisitPeca(p12, 1))
    moto_crm_c.afegirRequisitPeca(RequisitPeca(p14, 1))

    fabrica.afegirModelCotxe(civic_elec)
    fabrica.afegirModelCotxe(civic_comb)
    fabrica.afegirModelCotxe(hrv_comb)
    fabrica.afegirModelMoto(moto_cbr_e)
    fabrica.afegirModelMoto(moto_crm_c)
    print("Models afegits correctament.")

    # =================================================================
    # CAS D'ÚS 2 - Produir un nou vehicle
    # =================================================================

    print("\n--- CAS D'ÚS 2: Producció de vehicles ---")
    data_prod_1 = datetime(2026, 3, 10)
    print("Produint 10 Honda Civic elèctrics (Blanc)...")
    for _ in range(10):
        fabrica.produirVehicle(civic_elec, "Blanc", data_prod_1)
        
    data_prod_2 = datetime(2026, 3, 12)
    print("Produint 10 Honda Civic de combustió (Blau)...")
    for _ in range(10):
        
        fabrica.produirVehicle(civic_comb, "Blau", data_prod_2)


    # =================================================================
    # CAS D'ÚS 3 - Consulta de si una peça està disponible
    # =================================================================

    print("\n--- CAS D'ÚS 3: Consulta d'inventari ---")
    codi_consulta = "0001"
    stock_0001 = inventari.numExistenciesPeca(codi_consulta)
    print(f"Estoc disponible de la peça {codi_consulta}: {stock_0001} unitats.")

    cif_gearbox = "444444444C"
    peces_gb = inventari.pecesProveidor(cif_gearbox)
    print(f"Peces subministrades pel proveïdor GearBox ({cif_gearbox}):")
    for p in peces_gb:
        print(f" - [{p.codi}] {p.nom}")


    # =================================================================
    # CAS D'ÚS 4 - Saber quants models d'un determinat vehicle s'han produït
    # =================================================================

    print("\n--- CAS D'ÚS 4: Registre en un interval ---")
    inici_marc = datetime(2026, 3, 1)
    fi_marc = datetime(2026, 3, 31)
    
    quantitat_produida = registre.nVehiclesProduits(civic_comb, inici_marc, fi_marc)
    print(f"S'han produït {quantitat_produida} vehicles 'Honda Civic de combustió' al març de 2026.")


    # =================================================================
    # CAS D'ÚS 5 - Saber si és possible produir un vehicle
    # =================================================================

    print("\n--- CAS D'ÚS 5: Viabilitat de producció ---")
    es_possible = fabrica.es_possible_produir(civic_comb)
    print(f"És possible produir un Honda Civic de combustió en aquests moments?: {'Sí' if es_possible else 'No (Falten peces)'}.")

if __name__ == "__main__":
    main()
