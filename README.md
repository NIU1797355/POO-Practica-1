# Sistema de Gestió de Fàbrica de Vehicles (UML Implementation)

Aquest projecte és una implementació en Python d'un sistema de gestió de producció industrial per a una fàbrica de vehicles (cotxes i motos). El sistema controla tot el cicle de vida de la producció: des de la gestió de subministradors i peces en inventari fins a l'ensamblatge final en línies de producció i el seu registre històric.

## Descripció del Sistema

El programari segueix fidelment el disseny d'un diagrama de classes UML, aplicant principis de Programació Orientada a Objectes (POO) com l'abstracció, l'herència i l'encapsulament.

### Components Principals:

1.  **Fàbrica (Fabrica)**: L'orquestrador central. Gestiona els models disponibles, les línies de producció, l'inventari i el registre.
2.  **Models de Vehicle (ModelVehicle)**: Classe abstracta que defineix les propietats comunes (nom, cilindrada, si és elèctric). Es divideix en:
    * **ModelCotxe**: Inclou atributs com el nombre de portes i tipus de canvi.
    * **ModelMoto**: Inclou tipus de rodes i carnet necessari.
3.  **Gestió de Peces**:
    * **Subministrador**: Dades de les empreses que proveeixen components.
    * **Peca**: Informació tècnica de cada component.
    * **InventariPeces**: Control d'estoc i consum de materials.
4.  **Producció**:
    * **LineaProduccioVehicle**: Unitat física que fabrica el vehicle (ensamblatge).
    * **VehicleProduit**: L'objecte final amb número de sèrie, color i data de fabricació.
    * **RegistreProduccio**: Històric de tots els vehicles fabricats per a consultes estadístiques.

## Lògica de Producció

El sistema implementa una lògica de negoci robusta per evitar errors de producció:

* **Validació d'Estoc**: Abans de fabricar, la fàbrica consulta la llista de requisits de peces del model. Si no hi ha prou peces a l'estoc, la producció s'atura i llança una excepció.
* **Round-Robin**: El treball es distribueix equitativament entre les línies de producció disponibles de forma seqüencial.
* **Càlcul d'Etiquetes**: El sistema calcula automàticament l'etiqueta de contaminació (0 Emisions, C, B) segons el tipus de combustible i motorització.

## Instal·lació i Ús

### Requisits
* Python 3.7 o superior.

### Com executar la simulació
Pots utilitzar el bloc d'execució principal inclòs en el codi per veure una demostració del sistema en funcionament:

1.  Crea la infraestructura (Fàbrica, Inventari, Registre).
2.  Afegeix peces a l'inventari i assigna-les com a requisits d'un model.
3.  Crida al mètode per produir el vehicle.

    ```python
    # Exemple d'ús
    fabrica = Fabrica("Seat")
    fabrica.afegirModelCotxe("Leon", False, 2000, 5, "Manual", "Gasolina")
    # ... configurar peces ...
    vehicle = fabrica.produirVehicle(model_leon, "Blau", datetime.now())
    print(f"Vehicle fabricat: {vehicle._numeroSerie}")
    ```

## Diagrama de Classes (Resum)

El disseny se centra en la relació de composició entre la Fàbrica i els seus components, i la relació de dependència entre el Model de Vehicle i les peces necessàries.

## Autors

Aquest projecte ha estat desenvolupat per:
* Jiaxu
* Hector
* Pol
