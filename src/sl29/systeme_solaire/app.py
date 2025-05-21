"""Un module pour l'application"""

import json
from flask import Flask, render_template, request
from os import chdir,getcwd
print(getcwd())
if getcwd()[-25:] != "/src/sl29/systeme_solaire":
    texte = getcwd() + "/src/sl29/systeme_solaire"
    chdir(texte)
app = Flask(__name__)

# Chargement des données
with open('data/planets.json', 'r', encoding='utf-8') as f:
    planets = json.load(f)

with open('data/satellites.json', 'r', encoding='utf-8') as f:
    satellites = json.load(f)

for satellite in satellites:
    satellite["diameter"] = satellite["radius"]*2
    satellite["mass"] = satellite["gm"] / (6.6743*10**-11) / 10**13

@app.route('/')
def index():
    """Page d'accueil montrant comment les paramètres fonctionnent"""
    return render_template('index.html', planets=planets)

@app.route('/planete')
def show_planet():
    """Démontre l'utilisation de request.args.get()"""
    # Récupération du paramètre 'id' de la requête
    planet_id = request.args.get('id', type=int)

    # Vérification si le paramètre existe et est valide
    if planet_id is None:
        return "Erreur: Le paramètre 'id' est requis. Exemple: /planete?id=3", 400

    # Recherche de la planète
    planet_data = get_planet_by_id(planet_id)
    if not planet_data:
        return f"Erreur: Aucune planète trouvée avec l'ID {planet_id}", 404

    # Récupération des satellites
    planet_satellites = [s for s in satellites if s['planetId'] == planet_id]

    previous_planet_id = planet_id-1 if planet_id-1 > 0 else None
    previous_planet = None if previous_planet_id is None else get_planet_by_id(previous_planet_id)

    next_planet_id = planet_id+1 if planet_id+1 <= len(planets) else None
    next_planet = None if next_planet_id is None else get_planet_by_id(next_planet_id)

    return render_template('planet.html',
                         planet=planet_data,
                         previous_planet = previous_planet,
                         next_planet = next_planet,
                         satellites=planet_satellites,
                         request_args=dict(request.args))  # Pour démo pédagogique

@app.route('/satellite')
def show_satellite():
    """Montre comment gérer plusieurs paramètres"""

    # A FAIRE

    # récupérer l'id du sattelite depuis la requete
    satellite_id = request.args.get('id', type=int)
    # Si l'id n'est pas trouvé, retourner un message d'erreur et un status 404
    if satellite_id is None:
        return "Erreur: Le paramètre 'id' est requis. Exemple: /satellite?id=1", 404

    # Récuperer les données du satellite
    satellite_data = get_satellite_by_id(satellite_id)
    # Si aucune donnée trouvée, retourner un message d'erreur et un status 404
    if not satellite_data:
        return f"Erreur: Aucune planète trouvée avec l'ID {satellite_id}", 404

    # récupérer les données de la planète associée.
    asso_planet = planets[satellite_data["planetId"]-1]

    previous_satellite_id = satellite_id-1 if satellite_id-1 > 0 else None
    previous_satellite = None if previous_satellite_id is None else get_satellite_by_id(previous_satellite_id)

    next_satellite_id = satellite_id+1 if satellite_id+1 <= len(satellites) else None
    next_satellite = None if next_satellite_id is None else get_satellite_by_id(next_satellite_id)
    # retourner le template 'satellite.html' avec les variables:
    # - satellite
    # - planet
    return render_template('satellite.html',
                         satellite=satellite_data,
                         planet = asso_planet,
                         previous_satellite = previous_satellite,
                         next_satellite = next_satellite
                         )


def get_planet_by_id(planet_id:int)->dict|None:
    """Retourne la planète sous forme de dictionnaire

    :param planet_id: l'id de la planète
    :type planet_id: int
    :return:la planète ou None
    :rtype: dict|None
    """
    for planet in planets:
        if planet['id'] == planet_id:
            return planet
    return None  # Si aucune planète trouvée

def get_satellite_by_id(satellite_id:int)->dict|None:
    """Retourne la planète sous forme de dictionnaire

    :param planet_id: l'id de la planète
    :type planet_id: int
    :return:la planète ou None
    :rtype: dict|None
    """
    for satellite in satellites:
        if satellite['id'] == satellite_id:
            return satellite
    return None  # Si aucune planète trouvée

if __name__ == '__main__':
    app.run(debug=True)
