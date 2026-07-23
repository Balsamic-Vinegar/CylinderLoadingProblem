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
        return 0.0


def load_instances():
    output = generate_all_instances()

    basic_instances = []
    challenging_instances = []

    for instance_data in output["basic_instances"]:
        basic_instances.append(Instance(**instance_data))

    for instance_data in output["challenging_instances"]:
        challenging_instances.append(Instance(**instance_data))

    instances = {
        "basic": basic_instances,
        "challenging": challenging_instances
    }

    return instances


if __name__ == "__main__":
    instances = load_instances()

    basic_count = len(instances.get("basic", []))
    challenging_count = len(instances.get("challenging", []))

    print(
        f"Loaded {basic_count} basic instances \n"
        f"Loaded {challenging_count} challenging instances"
    )