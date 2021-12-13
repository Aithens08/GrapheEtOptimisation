import random
from data.utils import init_population, fitness_function, roulette, crossingover, mutation, selection
import time

start = time.time()


nbr={} #dico avec {chiffre initial: []}
numbers = []
with open("data/data9.txt", 'r') as f:
    n= int(f.readline())
    e=int(f.readline())
    b=int(f.readline())
    for elem in range(n):
        nbr[elem]=[random.randint(0,10) for i in range(3)]
        numbers.append(int(f.readline()))

'''Définition des paramètres de la simulation:'''
nbr_nombres = n
nbr_emplacement = e
nbr_boites = b
nbr_places = b*e

pop_size = 25
emplacements = nbr_emplacement*nbr_boites
generations = 20000

'''Iniialisation de la population'''
new = []
old = []
population = init_population(numbers, pop_size, emplacements)

'''Boucle de l'algo'''
for generation in range(generations):
    new = population
    population = roulette(population, nbr_emplacement, nbr_boites)
    population = crossingover(population, numbers)
    population = mutation(population, numbers,nbr_places)
    old = population + new
    population = selection(old,nbr_emplacement,nbr_boites, pop_size)
    BestScore = fitness_function(population[0], nbr_emplacement, nbr_boites)
    if generation % 100 == 0:
        print(f"Itération {generation} -> Score de {BestScore}")

solution = population

end = time.time()
elapsed = round(end - start,2)


with open("Output1.txt",'w') as s:
    compt=1
    complete_elem = []
    numberscompt = 0
    for key,value in solution[0].items():
        for i in value:
            complete_elem.append(i)
        s.write(f"{str(compt)} ")
        s.write(f"{str(numbers[numberscompt])} ")
        s.write(f"{str(len(value))} ")
        comptesp=0
        value.sort(reverse=True)
        for elem in value:
            if comptesp==len(value)-1:
                s.write(f"{str(elem)}")
            else:
                s.write(f"{str(elem)} ")
            comptesp+=1
        s.write('\n')
        compt+=1
        numberscompt += 1
    complete_elem.sort(reverse=True)

    print("Solution finale : ")

    for elem in range(nbr_boites):
        if elem != 0:
            print(complete_elem[elem*(nbr_emplacement):(elem+1)*(nbr_emplacement)])
            s.write(f"B{str(elem+1)} {complete_elem[int(elem * (nbr_emplacement))]}\n")
        else:
            print(complete_elem[:nbr_emplacement])
            s.write(f"B{str(elem + 1)} {complete_elem[0]}\n")
    
    s.write(f"COST {fitness_function(solution[0], nbr_emplacement, nbr_boites)}")


print(f'Temps d\'exécution : {elapsed} s')

