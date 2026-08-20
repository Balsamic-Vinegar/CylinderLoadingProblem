import random
from core import Solution, load_instances, evaluate_solution
import time

class GeneticAlgorithm:
    def __init__(self, instance, population_size=200, mutation_rate=0.015,
                 tournament_size=4, elitism_count=2, max_generations=500):
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
        length = len(parent1_order)

        crossover_points = random.sample(
            range(length),
            2
        )

        crossover_points.sort()

        start = crossover_points[0]
        end = crossover_points[1]

        child = [None] * length

        for i in range(start, end):
            child[i] = parent1_order[i]

        child_values = set(
            parent1_order[start:end]
        )

        remaining_genes = []

        for offset in range(length):
            index = (end + offset) % length
            gene = parent2_order[index]

            if gene not in child_values:
                remaining_genes.append(gene)

        fill_index = end % length

        for gene in remaining_genes:
            while child[fill_index] is not None:
                fill_index = (
                                     fill_index + 1
                             ) % length

            child[fill_index] = gene

            fill_index = (
                                 fill_index + 1
                         ) % length

        return child

    def swap_mutation(self, order):
        mutated_order = order.copy()

        if random.random() < self.mutation_rate:
            positions = random.sample(range(len(mutated_order)),2)

            i = positions[0]
            j = positions[1]

            temporary_value = mutated_order[i]

            mutated_order[i] = mutated_order[j]
            mutated_order[j] = temporary_value

        return mutated_order

    def local_search(self, order, max_attempts=100):
        current_order = order.copy()

        current_fitness, current_placements = evaluate_solution(current_order, self.instance)

        for attempt in range(max_attempts):

            if current_fitness == 0:
                break

            positions = random.sample(range(len(current_order)), 2)

            i = positions[0]
            j = positions[1]

            candidate_order = current_order.copy()

            candidate_order[i], candidate_order[j] = (
                candidate_order[j],
                candidate_order[i]
            )

            candidate_fitness, candidate_placements = evaluate_solution(candidate_order, self.instance)

            if candidate_fitness < current_fitness:
                current_order = candidate_order
                current_fitness = candidate_fitness
                current_placements = candidate_placements

        return current_order, current_fitness, current_placements

    def run(self):
        population = self.initialise_population()

        best_solution = None
        best_fitness = float("inf")

        fitness_history = []

        for i in range(self.max_generations):
            generation_best_solution = population[0]
            generation_best_fitness = population[0].fitness(
                self.instance
            )

            for j in range(1, len(population)):
                solution = population[j]

                solution_fitness = solution.fitness(
                    self.instance
                )

                if solution_fitness < generation_best_fitness:
                    generation_best_solution = solution
                    generation_best_fitness = solution_fitness

            if generation_best_fitness < best_fitness:
                best_solution = generation_best_solution
                best_fitness = generation_best_fitness

            fitness_history.append(best_fitness)

            if best_fitness == 0:
                break

            next_population = []

            if self.elitism_count > 0:
                ranked_population = sorted(
                    population,
                    key=lambda solution: solution.fitness(
                        self.instance
                    )
                )

                for j in range(self.elitism_count):
                    elite_solution = ranked_population[j]

                    if j == 0:
                        improved_order, improved_fitness, improved_placements = (
                            self.local_search(elite_solution.order,max_attempts=50))

                        if improved_fitness < elite_solution.fitness(self.instance):
                            elite_solution = Solution(improved_order)

                    next_population.append(elite_solution)

            while len(next_population) < self.population_size:
                parent1 = self.tournament_select(population)

                parent2 = self.tournament_select(population)

                child1_order = self.order_crossover(
                    parent1.order,
                    parent2.order
                )

                child2_order = self.order_crossover(
                    parent2.order,
                    parent1.order
                )

                child1_order = self.swap_mutation(
                    child1_order
                )

                child2_order = self.swap_mutation(
                    child2_order
                )

                child1 = Solution(child1_order)

                next_population.append(child1)

                if len(next_population) < self.population_size:
                    child2 = Solution(child2_order)

                    next_population.append(child2)

            population = next_population

        return best_solution, fitness_history

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