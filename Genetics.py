import random
from data.utils import init_population, fitness_function, roulette, crossingover, mutation, selection

nbr={} #dico avec {chiffre initial: []}
with open("data/data1.txt", 'r') as f:
    n= int(f.readline())
    e=int(f.readline())
    b=int(f.readline())
    for elem in range(n):
        nbr[(int(f.readline()))]=[random.randint(0,10) for i in range(3)]

'''Définition des paramètres de la simulation:'''
nbr_nombres = n
nbr_emplacement = e
nbr_boites = b

pop_size = 20
emplacements = nbr_emplacement*nbr_boites
generations = 2000

#dic ={7660: [3450, 4210], 7290: [3549, 3143, 85, 513], 7040: [3824, 750, 806, 1254, 50, 3, 353], 6890: [4591, 2261, 31, 4, 1, 2], 5860: [1407, 95, 4358], 5090: [3590, 1500], 4640: [21, 3415, 1204], 3830: [3656, 43, 131], 3460: [3143, 87, 43, 187], 580: [309, 222, 49]}
#print(fitness_function(dic,nbr_emplacement,nbr_boites))

'''Récupération des nombres pour initialiser la population de dictionaire'''
numbers = []
for key, value in nbr.items():
    numbers.append(key)


'''Iniialisation de la population'''
new = []
old = []
population = init_population(numbers, pop_size, emplacements)

'''Boucle de l'algo'''
for generation in range(generations):
    new = population
    population = roulette(population, nbr_emplacement, nbr_boites)
    population = crossingover(population, numbers)
    population = mutation(population, numbers)
    old = population + new
    population = selection(old,nbr_emplacement,nbr_boites, pop_size)
    BestScore = fitness_function(population[0], nbr_emplacement, nbr_boites)
    if generation % 100 == 0:
        print(f"Itération {generation} -> Score de {BestScore}")

solution = population


with open("Output1.txt",'w') as s:
    compt=1
    complete_elem = []
    for key,value in solution[0].items():
        for i in value:
            complete_elem.append(i)
        s.write(f"{str(compt)} ")
        s.write(f"{str(key)} ")
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

