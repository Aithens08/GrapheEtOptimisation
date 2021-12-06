import random
import numpy as np
#définition des fonctions:

def fitness_function(dic, emplacement, boxes):
    Total_sum = 0
    Split_sum = 0
    Solution = []
    fitness = 0
    for key, value in dic.items():
        Total_sum += key
        for i in value:
            Split_sum += i
            Solution.append(i)
    if len(Solution) != emplacement*boxes:
        return 10000000000
    else:
        Solution.sort(reverse= True)
        for box in range(boxes):
            if box != 0:
                fitness += Solution[int(box*(emplacement))]
            else:
                fitness += Solution[0]
        return fitness

def calculate_score(population, emplacement, boxes):
    sum_score = 0
    for chromosome in population:
        sum_score += fitness_function(chromosome, emplacement, boxes)
    return sum_score

def init_split(emplacement,numbers) :
    split=[1 for i in range(numbers)]
    weights = [(np.log(i)+1) for i in range(1,numbers+1)]
    weights.sort(reverse=True)
    while sum(split)<emplacement:
        a = random.choices(range(len(split)),weights=weights, k = 1)
        a = a[0]
        split[a]+=1
    return split

def divide(nbr, split_nbr):
    division = [0 for i in range(split_nbr)]
    if nbr%10 == 0:
        while sum(division) < nbr:
            a=random.randint(0,len(division)-1)
            division[a]+=10
    else:
        while sum(division) < nbr:
            a=random.randint(0,len(division)-1)
            division[a]+=1
    return division

def init_population(numbers,pop_size, emplacement):
    population = []
    number_size = len(numbers)
    for i in range(pop_size):
        chromosome = {}
        split = init_split(emplacement, number_size)
        for i in range(number_size):
            chromosome[numbers[i]] = divide(numbers[i], split[i])
        population.append(chromosome)
    return population

def roulette(population, nbr_emplacement, nbr_boite):

    rotation_roulette = []
    selected_chromosomes = []
    score_population = []

    sum_score = calculate_score(population, nbr_emplacement, nbr_boite)
    prev_score = 0
    rotation_roulette = np.random.randint(1,10, size=len(population))/10.0

    for chromosome in population:
        score_population.append(fitness_function(chromosome, nbr_emplacement, nbr_boite))

    roulette_sector = []
    for chromosome, score in zip(population, score_population ):
        roulette_sector.append((np.round(prev_score,2), np.round((score/sum_score)+prev_score, 2)))
        prev_score += np.float(score/sum_score)

    for chromosome, score_chromosome in zip(population, roulette_sector):
        for selected_sector in rotation_roulette:
            if score_chromosome[0] < selected_sector <= score_chromosome[1]:
                selected_chromosomes.append(chromosome)

    return selected_chromosomes

def crossingover(population, numbers):

    len_chr = len(population)
    slice_chr = int(len_chr/2)
    new_population = []

    for husband, wife in zip(population[:slice_chr], population[slice_chr:len_chr]):
        children1 = {}
        children2 = {}
        crossing = np.random.randint(1, len(husband))
        for i in range(len(numbers)):
            key = numbers[i]
            if i < crossing:
                children1[key] = husband[key]
            else:
                children1[key] = wife[key]
        new_population.append(children1)
        for i in range(len(numbers)):
            key = numbers[i]
            if i < crossing:
                children2[key] = wife[key]
            else:
                children2[key] = husband[key]
        new_population.append(children2)
    return new_population

def mutation(population, numbers):
    new_population = []

    for chromosome in population:
        if np.random.randint(0,100) <= 50:
            genedel = np.random.choice(numbers)
            split_nbr = len(chromosome[genedel])
            if split_nbr != 1:
                chromosome[genedel] = divide(genedel, split_nbr-1)
                geneadd = np.random.choice(numbers)
                while geneadd == genedel:
                    geneadd = np.random.choice(numbers)
                split_nbr = len(chromosome[geneadd])
                chromosome[geneadd] = divide(geneadd, split_nbr+1)

            new_population.append(chromosome)
        else:
            new_population.append(chromosome)
    return new_population

def takefirst(elem):
    return elem[0]

def selection(population, nbr_emplacement, nbr_boxes, nbr_gene):
    result = []
    new_population = []
    score = 0
    for chromosome in population:
        score = fitness_function(chromosome, nbr_emplacement, nbr_boxes)
        new_population.append((score, chromosome))
    new_population = sorted(new_population, key= takefirst)
    i = 0
    for key, val in new_population:
        if i < nbr_gene:
            result.append(val)
            i +=1
        else:
            break
    return result

def final_selection(population, nbr_emplacement, nbr_boxes, nbr_gene):
    result = []
    new_population = []
    score = 0
    for chromosome in population:
        score = fitness_function(chromosome, nbr_emplacement, nbr_boxes)
        new_population.append((score, chromosome))
    new_population = sorted(new_population, key= takefirst)
    i = 0
    for key, val in new_population:
        if i < nbr_gene:
            result.append(val)
            i +=1
        else:
            break
    return result
