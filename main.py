import logging
import math
from datetime import datetime

# === Fabrica ==========

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
from abc import ABC, abstractmethod
from datetime import date

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
