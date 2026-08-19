from container_instances import Cylinder, Container, Instance
from core import Solution, evaluate_solution, greedy_random
from ga import GeneticAlgorithm
from visualisation import draw_solution


def create_stress_instances():
    instances = []

    # 18 barrels

    stress_easy_cylinders = [
        Cylinder(1, 2.2, 27),
        Cylinder(2, 2.9, 24),
        Cylinder(3, 2.3, 28),
        Cylinder(4, 1.8, 25),
        Cylinder(5, 2.4, 34),
        Cylinder(6, 1.6, 19),
        Cylinder(7, 1.6, 34),
        Cylinder(8, 2.5, 11),
        Cylinder(9, 3.0, 39),
        Cylinder(10, 2.5, 28),
        Cylinder(11, 1.7, 10),
        Cylinder(12, 2.3, 12),
        Cylinder(13, 1.8, 17),
        Cylinder(14, 1.6, 24),
        Cylinder(15, 2.2, 35),
        Cylinder(16, 2.3, 29),
        Cylinder(17, 2.3, 30),
        Cylinder(18, 2.2, 18),
    ]

    stress_easy_container = Container(
        13,
        11,
        670
    )

    instances.append(
        Instance(
            "stress_easy_18_cylinders",
            stress_easy_container,
            stress_easy_cylinders
        )
    )

    # 20 barrels

    stress_medium_cylinders = stress_easy_cylinders + [
        Cylinder(19, 3.0, 40),
        Cylinder(20, 2.8, 31),
    ]

    stress_medium_container = Container(
        13,
        11,
        800
    )

    instances.append(
        Instance(
            "stress_medium_20_cylinders",
            stress_medium_container,
            stress_medium_cylinders
        )
    )

    # 23 barrels

    stress_hard_cylinders = stress_medium_cylinders + [
        Cylinder(21, 2.0, 17),
        Cylinder(22, 1.9, 12),
        Cylinder(23, 1.9, 12)
    ]

    stress_hard_container = Container(
        13,
        11,
        1000
    )

    instances.append(
        Instance(
            "stress_hard_23_cylinders",
            stress_hard_container,
            stress_hard_cylinders
        )
    )

    return instances


if __name__ == "__main__":
    instances = create_stress_instances()

    test_instance = instances[2]

    print(
        f"\nTesting {test_instance.name}"
    )

    ga = GeneticAlgorithm(test_instance,population_size=200,tournament_size=4,mutation_rate=0.015,elitism_count=2,max_generations=100)

    best_solution, fitness_history = ga.run()

    best_fitness = best_solution.fitness(
        test_instance
    )

    print("\nGA")

    print(
        f"Best fitness: "
        f"{best_fitness:.2f}"
    )

    print(
        f"Generations used: "
        f"{len(fitness_history)}"
    )

    print(
        f"Cylinders placed: "
        f"{len(best_solution.placements)}/"
        f"{len(test_instance.cylinders)}"
    )

    draw_solution(test_instance,best_solution.placements,"GA solution",best_fitness)

    fitness, order, placements = greedy_random(test_instance,trials=1000)

    print("\nGreedy random")

    print(
        f"Best fitness: "
        f"{fitness:.2f}"
    )

    print(
        f"Cylinders placed: "
        f"{len(placements)}/"
        f"{len(test_instance.cylinders)}"
    )

    print(
        f"Order: "
        f"{order}"
    )

    draw_solution(
        test_instance,
        placements,
        "Greedy random solution",
        fitness
    )