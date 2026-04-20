import logging
import math
from datetime import datetime 
from abc import ABC, abstractmethod
from __future__ import annotations

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
    def afegirModelCotxe(self, nom: str, es_electric: bool, cilindrada: int, numPortes: int, tipusCanvi: str, tipusCombustible: str) -> bool:
        try:
            nou_cotxe = ModelCotxe(nom, es_electric, cilindrada, numPortes, tipusCanvi, tipusCombustible)
            self._models.append(nou_cotxe)
            return True
        except Exception as e:
            logging.error(f"Error en afegir model cotxe: {e}")
            return False
    def afegirModelMoto(self, nom: str, es_electric: bool, cilindrada: int, tipus_rodes: str, carnet_necessari: str) -> bool:
        try:
            nova_moto = ModelMoto(nom, es_electric, cilindrada, tipus_rodes, carnet_necessari)
            self._models.append(nova_moto)
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


# === Main ====
class ModelVehicle(ABC) :
    def __init__(self, nomModel: str, electric: bool, cilindrada:int):
            self._nomModel = nomModel
            self._electric = electric
            self._requisits_peces = []
            if cilindrada > 0 :
                self._cilindrada = cilindrada
            else :
                raise ValueError("La cilindrada ha de ser un nombre major a 0 \n")
     
    @abstractmethod        
    def numeroDeRodes(self) :
        pass
    @abstractmethod
    def etiquetaDeContaminacio(self):
        pass
    def afegirRequisitPeca(self, requisit: RequisitPeca):
        self._requisits_peces.append(requisit)
    def pecesNecesaries(self) -> list:
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
        """The numeroDePortes property."""
        return self._numeroDePortes
    @numeroDePortes.setter
    def numeroDePortes(self, value):
        if value >=2 :
            self._numeroDePortes = value
        else :
            raise ValueError("El número de portes ha de ser com a mínim 2.")
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

    def get_nom(self): return self._nom
    def get_cif(self): return self._cif
    def get_adreca(self): return self._adreca
    def get_pais(self): return self._pais

class Peca:
    def __init__(self, codi, nom, descripcio, subministrador):
        self._codi = codi
        self._nom = nom
        self._descripcio = descripcio
        self._subministrador = subministrador

    def get_codi(self): return self._codi
    def get_nom(self): return self._nom
    def get_subministrador(self): return self._subministrador

class RequisitPeca:
    def __init__(self, peca, quantitat, opcional=False, posicio=0):
        self._peca = peca
        self._quantitat = quantitat
        self._opcional = opcional
        self._posicio = posicio

    def get_peca(self): return self._peca
    def get_quantitat(self): return self._quantitat

class InventariPeces:
    def __init__(self, data_ultima_revisio):
        self._data_ultima_revisio = data_ultima_revisio
        self._estoc = {} # codi_peca -> dict(peca: Peca, quantitat: int)

    def afegir_estoc(self, peca, quantitat):
        codi = peca.get_codi()
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
            if dades['peca'].get_subministrador().get_cif() == cif_proveidor:
                peces_prov.append(dades['peca'])
        return peces_prov

    def consumir_peces(self, model):
        for req in model.pecesNecesaries():
            codi = req.get_peca().get_codi()
            quantitat_necessaria = req.get_quantitat()
            
            if codi not in self._estoc or self._estoc[codi]['quantitat'] < quantitat_necessaria:
                raise Exception(f"Estoc insuficient per la peça: {codi}")
                
        for req in model.pecesNecesaries():
            codi = req.get_peca().get_codi()
            self._estoc[codi]['quantitat'] -= req.get_quantitat()
