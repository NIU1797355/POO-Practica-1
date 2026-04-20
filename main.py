import logging
import math
from datetime import datetime

# === Fabrica ===

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


# === Main ===
