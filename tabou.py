import random
import math

def calcule_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisins_complets(solution, nombre_voisins):
    voisins = []
    for _ in range(nombre_voisins):
        voisin = solution[:]
        i, j = random.sample(range(len(solution)), 2)
        voisin[i], voisin[j] = voisin[j], voisin[i]
        voisins.append(voisin)
    return voisins

def est_dans_tabou(mouvement, liste_tabou, taille_tabou):
    return mouvement in liste_tabou[-taille_tabou:]

def mettre_a_jour_tabou(liste_tabou, mouvement, taille_tabou):
    liste_tabou.append(mouvement)
    if len(liste_tabou) > taille_tabou:
        liste_tabou.pop(0)
    return liste_tabou

def get_mouvement(solution1, solution2):
    for i in range(len(solution1)):
        if solution1[i] != solution2[i]:
            for j in range(i + 1, len(solution1)):
                if solution1[j] != solution2[j]:
                    return (min(i, j), max(i, j))
    return None

def recherche_tabou(matrice_distances, taille_liste_tabou, iterations_max, nombre_voisins):
    nombre_villes = len(matrice_distances)
    
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calcule_distance_totale(solution_actuelle, matrice_distances)
    
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    
    liste_tabou = []
    stagnation = 0
    max_stagnation = 100
    
    for iteration in range(iterations_max):
        voisins = generer_voisins_complets(solution_actuelle, nombre_voisins)
        
        meilleur_voisin = None
        meilleure_distance_voisin = float('inf')
        meilleur_mouvement = None
        
        for voisin in voisins:
            distance_voisin = calcule_distance_totale(voisin, matrice_distances)
            mouvement = get_mouvement(solution_actuelle, voisin)
            
            if distance_voisin < meilleure_distance:
                meilleur_voisin = voisin
                meilleure_distance_voisin = distance_voisin
                meilleur_mouvement = mouvement
                break
            
            if not est_dans_tabou(mouvement, liste_tabou, taille_liste_tabou):
                if distance_voisin < meilleure_distance_voisin:
                    meilleur_voisin = voisin
                    meilleure_distance_voisin = distance_voisin
                    meilleur_mouvement = mouvement
        
        if meilleur_voisin is None:
            for voisin in voisins:
                distance_voisin = calcule_distance_totale(voisin, matrice_distances)
                if distance_voisin < meilleure_distance_voisin:
                    meilleur_voisin = voisin
                    meilleure_distance_voisin = distance_voisin
                    meilleur_mouvement = get_mouvement(solution_actuelle, voisin)
        
        if meilleur_voisin is not None:
            solution_actuelle = meilleur_voisin
            distance_actuelle = meilleure_distance_voisin
            
            if distance_actuelle < meilleure_distance:
                meilleure_solution = solution_actuelle[:]
                meilleure_distance = distance_actuelle
                stagnation = 0
            else:
                stagnation += 1
            
            if meilleur_mouvement is not None:
                liste_tabou = mettre_a_jour_tabou(liste_tabou, meilleur_mouvement, taille_liste_tabou)
        
        if stagnation >= max_stagnation:
            break
        
        if iteration % 100 == 0:
            print(f"Itération {iteration}: Meilleure distance = {meilleure_distance}")
    
    return meilleure_solution, meilleure_distance

def recherche_tabou_intensification(matrice_distances, taille_liste_tabou, iterations_max, nombre_voisins, cycles_intensification=3):
    meilleure_solution_globale = None
    meilleure_distance_globale = float('inf')
    
    for cycle in range(cycles_intensification):
        print(f"\n=== CYCLE D'INTENSIFICATION {cycle + 1} ===")
        
        if cycle == 0:
            meilleure_solution, meilleure_distance = recherche_tabou(
                matrice_distances, taille_liste_tabou, iterations_max, nombre_voisins
            )
        else:
            solution_depart = meilleure_solution_globale[:]
            for _ in range(3):
                i, j = random.sample(range(len(solution_depart)), 2)
                solution_depart[i], solution_depart[j] = solution_depart[j], solution_depart[i]
            
            meilleure_solution, meilleure_distance = recherche_tabou(
                matrice_distances, taille_liste_tabou, iterations_max // 2, nombre_voisins
            )
        
        if meilleure_distance < meilleure_distance_globale:
            meilleure_solution_globale = meilleure_solution
            meilleure_distance_globale = meilleure_distance
        
        print(f"Meilleure distance après cycle {cycle + 1}: {meilleure_distance_globale}")
    
    return meilleure_solution_globale, meilleure_distance_globale

matrice_distances = [
    [0, 2, 3, 3, 7, 7, 0, 1, 7, 2],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [3, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [3, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 7, 4, 2, 0, 7, 3, 2, 2, 7],
    [7, 3, 3, 15, 7, 0, 1, 0, 2, 10],
    [0, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [1, 15, 4, 7, 2, 0, 2, 0, 1, 10],
    [7, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [2, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]

print("=== RECHERCHE TABOU POUR TSP ===")
meilleure_solution_tabou, meilleure_distance_tabou = recherche_tabou(
    matrice_distances,
    taille_liste_tabou=10,
    iterations_max=1000,
    nombre_voisins=50
)

print("\nMeilleure solution trouvée (Recherche Tabou):", meilleure_solution_tabou)
print("Distance minimale:", meilleure_distance_tabou)

print("\n=== RECHERCHE TABOU AVEC INTENSIFICATION ===")
meilleure_solution_intense, meilleure_distance_intense = recherche_tabou_intensification(
    matrice_distances,
    taille_liste_tabou=15,
    iterations_max=800,
    nombre_voisins=40,
    cycles_intensification=3
)

print("\nMeilleure solution finale (Recherche Tabou Intensifiée):", meilleure_solution_intense)
print("Distance minimale finale:", meilleure_distance_intense)