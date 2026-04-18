import logging
import math
from datetime import datetime 
from abc, import ABC, abstractmethod

# === Fabrica ===

class Fabrica:
    def __init__(self, nom):
        self._nom = nom
        self._lines_produccio = None
        self._inventari = None
        self._registre = None
    def afegirModelCotxe(self, nom: str, es_electric: bool, cilindrada: int, num_portes: int, tipus_canvi: str, tipus_combustible: str) -> bool:
        pass
    def afegirModelMoto(self, nom: str, es_electric: bool, cilindrada: int, tipus_rodes: str, carnet_necessari: str) -> bool:
        pass
    def produirVehicle(self, model: ModelVehicle, color: str, data: Date) -> VehicleProduit:
        pass



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
    def numeroDeRodes(self, nombre:int) :
            pass
    @abstractmethod
    def etiquetaDeContaminacio(self,etiqueta:str):
        pass
    @abstractmethod
    def pecesNecesaries(self, pecesll: list()):
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






