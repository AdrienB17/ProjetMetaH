import random

def fitness(part1, part2, graph):
    cut = 0
    for node in part1:
        for neighbor, weight in graph[node].items():
            if neighbor in part2:
                cut += weight
    return -cut  # the smaller the cut, the better the fitness function

def random_partition(nodes):
    n = len(nodes)
    part1 = set(random.sample(nodes, n//2))
    part2 = set(nodes) - part1
    return part1, part2

def crossover(parent1, parent2):
    n = len(parent1)
    k = random.randint(1, n-1)
    child1 = parent1.copy()
    child2 = parent2.copy()
    child1.update(parent2)
    child2.update(parent1)
    while len(child1) > n//2:
        child1.remove(random.choice(list(child1)))
    while len(child2) > n//2:
        child2.remove(random.choice(list(child2)))
    return child1, child2

def mutate(partition, mutation_rate):
    for node in partition:
        if random.random() < mutation_rate:
            partition.remove(node)
            partition.add(random.choice(list(set(graph[node]) - partition)))
    return partition

def genetic_algorithm(graph, population_size=100, num_generations=1000, crossover_rate=0.8, mutation_rate=0.1):
    nodes = list(graph.keys())
    best_partition = None
    best_fitness = float('inf')

    # initial population
    population = []
    for i in range(population_size):
        part1, part2 = random_partition(nodes)
        fitness_value = fitness(part1, part2, graph)
        population.append((part1, part2, fitness_value))

        if fitness_value < best_fitness:
            best_fitness = fitness_value
            best_partition = (part1, part2)

    # evolution loop
    for generation in range(num_generations):
        new_population = []

        # keep the best individual
        new_population.append((best_partition[0], best_partition[1], best_fitness))

        # crossover
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1[0], parent2[0])
                child1_fitness = fitness(child1, child2, graph)
                child2_fitness = fitness(child2, child1, graph)
                new_population.append((child1, child2, child1_fitness))
                new_population.append((child2, child1, child2_fitness))

        # mutation
        for i in range(1, population_size):
            new_population[i] = (mutate(new_population[i][0], mutation_rate),
                                 mutate(new_population[i][1], mutation_rate),
                                 fitness(new_population[i][0], new_population[i][1], graph))

        # selection
        population = sorted(new_population, key=lambda x: x[2])
        if population[0][2] < best_fitness:
            best_fitness = population[0][2]
            best_partition = (population[0][0], population[0][1])

    return best_partition
