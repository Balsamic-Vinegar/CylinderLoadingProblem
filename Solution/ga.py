import random
from core import Solution, load_instances

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

    instance = instances["basic"][0]

    ga = GeneticAlgorithm(instance,population_size=50,tournament_size=4)

    population = ga.initialise_population()

    assert len(population) == ga.population_size

    for sol in population:
        assert sorted(sol.order) == list(
            range(len(instance.cylinders))
        )

    selected = ga.tournament_select(population)

    assert selected in population
    assert isinstance(selected, Solution)