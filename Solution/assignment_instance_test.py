from core import load_instances
from ga import GeneticAlgorithm
from visualisation import draw_solution


if __name__ == "__main__":
    instances = load_instances()

    basic_count = len(instances.get("basic", []))
    challenging_count = len(instances.get("challenging", []))

    print(
        f"Loaded {basic_count} basic instances\n"
        f"Loaded {challenging_count} challenging instances"
    )

    for group in ("basic", "challenging"):
        for test_instance in instances[group]:

            print(
                f"\nTesting GA on "
                f"{test_instance.name}..."
            )

            ga = GeneticAlgorithm(test_instance)

            best_solution, fitness_history = ga.run()

            fitness = best_solution.fitness(test_instance)
            order = best_solution.order
            placements = best_solution.placements

            print(f"Best fitness: {fitness:.2f}")
            print(f"Order: {order}")
            print(f"Generations used: {len(fitness_history)}")
            print(f"Cylinders placed: {len(placements)}")

            draw_solution(test_instance, placements, "GA solution", fitness)