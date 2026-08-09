import random
from visualisation import draw_solution
from container_instances import Cylinder, Container, Instance, generate_all_instances


class Placement:

    def __init__(self, cylinder, x, y):
        self.cylinder = cylinder
        self.x = x
        self.y = y
        self.radius = cylinder.diameter / 2

    def to_dict(self):
        placement_data = {
            "id": self.cylinder.id,
            "x": self.x,
            "y": self.y,
            "diameter": self.cylinder.diameter
        }

        return placement_data


def distance(x1, y1, x2, y2):
    x_difference = x1 - x2
    y_difference = y1 - y2

    return (x_difference ** 2 + y_difference ** 2) ** 0.5


def check_overlap(placement1, placement2):
    minimum_distance = placement1.radius + placement2.radius
    actual_distance = distance(
        placement1.x,
        placement1.y,
        placement2.x,
        placement2.y
    )

    return actual_distance < minimum_distance - 0.001


def is_in_bounds(placement, container):
    radius = placement.radius

    x_in_bounds = (
        radius <= placement.x <= container.width - radius
    )

    y_in_bounds = (
        radius <= placement.y <= container.depth - radius
    )

    return x_in_bounds and y_in_bounds


class Solution:

    def __init__(self, order, placements=None):
        self.order = order

        if placements is None:
            self.placements = []
        else:
            self.placements = placements

    def fitness(self, instance):
        fitness, placements = evaluate_solution(self.order,instance)

        self.placements = placements

        return fitness


def load_instances():
    output = generate_all_instances()

    basic_instances = []
    challenging_instances = []

    for instance_data in output["basic_instances"]:
        container = Container(
            **instance_data["container"]
        )

        cylinders = []

        for cylinder_data in instance_data["cylinders"]:
            cylinders.append(Cylinder(**cylinder_data))

        instance = Instance(
            name=instance_data["name"],
            container=container,
            cylinders=cylinders
        )

        basic_instances.append(instance)

    for instance_data in output["challenging_instances"]:
        container = Container(**instance_data["container"])

        cylinders = []

        for cylinder_data in instance_data["cylinders"]:
            cylinders.append(
                Cylinder(**cylinder_data)
            )

        instance = Instance(
            name=instance_data["name"],
            container=container,
            cylinders=cylinders
        )

        challenging_instances.append(instance)

    instances = {
        "basic": basic_instances,
        "challenging": challenging_instances
    }

    return instances


def place_cylinder_greedy(cylinder, existing_placements, container, running_com, running_weight):
    radius = cylinder.diameter / 2
    best_pos = None
    best_score = float("inf")

    step = radius * 0.5

    y_positions = []

    for i in range(int(container.depth / step) + 1):
        y = container.depth - radius - (i * step)
        y_positions.append(y)

    x_positions = []

    for i in range(int((container.width - (2 * radius)) / step) + 1):
        x = radius + (i * step)
        x_positions.append(x)

    target_x = container.width / 2
    target_y = container.depth / 2
    com_x, com_y = running_com

    for y in y_positions:
        for x in x_positions:
            candidate = Placement(cylinder,x,y)

            if not is_in_bounds(candidate, container):
                continue

            overlaps = False

            for placement in existing_placements:
                if check_overlap(candidate, placement):
                    overlaps = True
                    break

            if overlaps:
                continue

            new_weight = running_weight + cylinder.weight
            new_com_x = (com_x * running_weight + x * cylinder.weight) / new_weight
            new_com_y = (com_y * running_weight + y * cylinder.weight) / new_weight

            score = distance(new_com_x, new_com_y, target_x, target_y)

            if score < best_score:
                best_score = score
                best_pos = (x, y)

    if best_pos is not None:
        return Placement(cylinder,best_pos[0],best_pos[1])

    return None


def evaluate_solution(order, instance):
    container = instance.container
    cylinders = instance.cylinders

    placements = []
    total_weight = 0.0

    running_com = (container.width / 2, container.depth / 2)
    running_weight = 0.0

    for idx in order:
        cylinder = cylinders[idx]

        placement = place_cylinder_greedy(cylinder, placements, container, running_com, running_weight)

        if placement is None:
            unplaced = len(cylinders) - len(placements)
            failure_penalty = 1000 + (unplaced * 10)

            return failure_penalty, placements

        placements.append(placement)
        total_weight += cylinder.weight

        new_weight = running_weight + cylinder.weight
        running_com = (
            (running_com[0] * running_weight + placement.x * cylinder.weight) / new_weight,
            (running_com[1] * running_weight + placement.y * cylinder.weight) / new_weight,
        )
        running_weight = new_weight

    weight_over_limit = max(
        0,
        total_weight - container.max_weight
    )

    weight_penalty = weight_over_limit * 10

    com_penalty = 0
    com_x, com_y = running_com

    safe_min_x = container.width * 0.2
    safe_max_x = container.width * 0.8

    safe_min_y = container.depth * 0.2
    safe_max_y = container.depth * 0.8

    if com_x < safe_min_x:
        com_penalty += (safe_min_x - com_x) * 50

    elif com_x > safe_max_x:
        com_penalty += (com_x - safe_max_x) * 50

    if com_y < safe_min_y:
        com_penalty += (safe_min_y - com_y) * 50

    elif com_y > safe_max_y:
        com_penalty += (com_y - safe_max_y) * 50

    fitness = (weight_penalty + com_penalty)

    return fitness, placements


def greedy_random(instance, trials=50):
    best_fitness = float("inf")
    best_order = None
    best_placements = None

    for _ in range(trials):
        order = list(range(len(instance.cylinders)))

        random.shuffle(order)

        fitness, placements = evaluate_solution(order,instance)

        if fitness < best_fitness:
            best_fitness = fitness
            best_order = order
            best_placements = placements

    return (
        best_fitness,
        best_order,
        best_placements
    )


if __name__ == "__main__":
    instances = load_instances()

    basic_count = len(instances.get("basic", []))
    challenging_count = len(instances.get("challenging", []))

    print(
        f"Loaded {basic_count} basic instances\n"
        f"Loaded {challenging_count} challenging instances"
    )

    test_instance = instances["challenging"][0]

    print(
        f"\nTesting greedy algorithm on "
        f"{test_instance.name}..."
    )

    fitness, order, placements = greedy_random(test_instance, trials=50)

    print(f"Best fitness: {fitness:.2f}")
    print(f"Order: {order}")
    print(f"Cylinders placed: {len(placements)}")

    draw_solution(test_instance,placements,"Greedy random solution", fitness)