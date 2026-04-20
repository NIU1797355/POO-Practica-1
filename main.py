import logging
import math
from datetime import datetime 
from abc, import ABC, abstractmethod

# === Fabrica ==========

class Fabrica:
    def __init__(self, marca: str):
        self._marca = marca
        self._lineaProduccio = []
        self._inventariPeces = None
        self._registreProduccio = None
    def afegirModelCotxe(self, nom: str, es_electric: bool, cilindrada: int, numPortes: int, tipusCanvi: str, tipusCombustible: str) -> bool:
        pass
    def afegirModelMoto(self, nom: str, es_electric: bool, cilindrada: int, tipus_rodes: str, carnet_necessari: str) -> bool:
        pass
    def produirVehicle(self, model: ModelVehicle, color: str, data: Date) -> VehicleProduit:
        pass
    def afegirLineaProduccio(self, linea_produccio: LineaProduccioVehicle) -> bool:
        if (linea_produccio not in self._linea_produccio):
            self._linea_produccio.append(linea_produccio)
            return True
        else:
            raise Exception("Error: linea de produccio ja està a la llista.")


# === Main ====
class ModelVehicle(ABC) :
    def __init__(self, nomModel: str, electric: bool, cilindrada:int):
            self._nomModel = nomModel
            self._electric = electric
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
    @abstractmethod
    def pecesNecesaries(self, pecesll: list()):
        pass

class LineaProduccioVehicle:
    def __init__(self, id_linea: str):
        self._id_linea = id_linea
    def produirVehicle(model: ModelVehicle) -> VehicleProduit:
        pass

class RegistreProduccio:
    def __init__(self, dataIniciRegistre: Date):
        self._dataIniciRegistre = dataIniciRegistre 
    def nVehiclesProduits(model: Model, dataInici: Date, dataFi: Date) -> int:
        pass


class ModelCotxe(ModelVehicle) :
    def __init__(self,nomModel:str, electric:bool, cilindrada:int,portes:int,canvi:str,combustible:str):
        super().__init__(nomModel,electric,cilindrada)
        self.numeroDePortes = portes
        self.tipusCanviMarxes = canvi
        self.tipusCombustible = combustible
    def numeroDeRodes(self):
        return 4
    def etiquetaDeContaminacio(self,etiqueta:str):
        if self.electric :
            return "0 Emisions"
        elif self.tipusCombustible.lower() == "gasolina":
            return "C"
        elif self.tipusCombustible.lower() == "diesel" :
            return "B"
        else :
            return "Sense etiqueta"
    def pecesNecesaries(self) :
        return 
    @property
    def numeroDePortes(self):
        """The numeroDePortes property."""
        return self._numeroDePortes
    @numeroDePortes.setter
    def numeroDePortes(self, value):
        if value >=2 :
            self._numeroDePortes = value
        else :
            print("El numero de portes ha de ser com a mínim 2.")
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
        if self.electric :
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
        """Mètode auxiliar per actualitzar inventari a l'hora de produir."""
        for req in model.pecesNecesaries():
            self._estoc[req.get_peca().get_codi()]['quantitat'] -= req.get_quantitat()
