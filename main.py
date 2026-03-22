import logging
import math
from datetime import datetime

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



# === Main ===
