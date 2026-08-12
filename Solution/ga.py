import random
from core import Solution, load_instances
import time

class GeneticAlgorithm:
    def __init__(self, instance, population_size=200, mutation_rate=0.015,
                 tournament_size=4, elitism_count=1, max_generations=500):
        self.instance = instance
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism_count = elitism_count
        self.max_generations = max_generations

    def initialise_population(self):
        population = []

        for i in range(self.population_size):
            order = list(range(len(self.instance.cylinders)))

            random.shuffle(order)

            solution = Solution(order)

            population.append(solution)

        return population

    def tournament_select(self, population):
        contestants = random.sample(population, self.tournament_size)

        best_contestant = contestants[0]
        best_fitness = best_contestant.fitness(self.instance)

        for i in range(1, len(contestants)):
            contestant = contestants[i]
            contestant_fitness = contestant.fitness(self.instance)

            if contestant_fitness < best_fitness:
                best_contestant = contestant
                best_fitness = contestant_fitness

        return best_contestant

    def order_crossover(self, parent1_order, parent2_order):
        pass

    def swap_mutation(self, order):
        pass

    def run(self):
        pass

if __name__ == "__main__":
    instances = load_instances()

    instance = instances["challenging"][2]

    ga = GeneticAlgorithm(instance,population_size=200,tournament_size=4)

    population = ga.initialise_population()

    for sol in population:
        assert sorted(sol.order) == list(
            range(len(instance.cylinders))
        )

    parent_pairs = ga.population_size // 2
    selected_parents = []

    start_time = time.perf_counter()

    for i in range(parent_pairs):
        parent1 = ga.tournament_select(population)
        parent2 = ga.tournament_select(population)

        selected_parents.append(parent1)
        selected_parents.append(parent2)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    elapsed_ms = elapsed_time * 1000

    print(
        "GA population and one generation of "
        "parent selection tests passed \n"
        f"time: {elapsed_time:.2f}s"
    )