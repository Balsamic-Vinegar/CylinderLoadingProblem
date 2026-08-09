import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from matplotlib.patches import Rectangle


def calculate_centre_of_mass(placements):
    total_weight = 0.0
    weighted_x = 0.0
    weighted_y = 0.0

    for placement in placements:
        cylinder_weight = placement.cylinder.weight

        total_weight += cylinder_weight
        weighted_x += placement.x * cylinder_weight
        weighted_y += placement.y * cylinder_weight

    if total_weight == 0:
        return None, None

    centre_x = weighted_x / total_weight
    centre_y = weighted_y / total_weight

    return centre_x, centre_y


def draw_solution(instance, placements, title, fitness):
    container = instance.container

    figure, axis = plt.subplots(
        figsize=(10, 7)
    )

    container_shape = Rectangle(
        (0, 0),
        container.width,
        container.depth,
        fill=False,
        linewidth=3,
        label="Container"
    )

    axis.add_patch(container_shape)

    safe_zone_x = container.width * 0.2
    safe_zone_y = container.depth * 0.2

    safe_zone_width = container.width * 0.6
    safe_zone_depth = container.depth * 0.6

    safe_zone_shape = Rectangle(
        (
            safe_zone_x,
            safe_zone_y
        ),
        safe_zone_width,
        safe_zone_depth,
        fill=False,
        linestyle="--",
        linewidth=2,
        edgecolor="green",
        label="Centre of mass safe zone"
    )

    axis.add_patch(safe_zone_shape)

    for placement_index in range(len(placements)):
        placement = placements[placement_index]

        cylinder_shape = Circle(
            (
                placement.x,
                placement.y
            ),
            placement.radius,
            alpha=0.5,
            label=(
                "Cylinders"
                if placement_index == 0
                else None
            )
        )

        axis.add_patch(cylinder_shape)

        axis.text(
            placement.x,
            placement.y,
            str(placement.cylinder.id),
            horizontalalignment="center",
            verticalalignment="center"
        )

    centre_x, centre_y = calculate_centre_of_mass(
        placements
    )

    if centre_x is not None and centre_y is not None:
        axis.scatter(
            centre_x,
            centre_y,
            marker="x",
            s=100,
            color="red",
            linewidth=3,
            label="Centre of mass"
        )

    margin = max(
        container.width,
        container.depth
    ) * 0.05

    axis.set_xlim(
        -margin,
        container.width + margin
    )

    axis.set_ylim(
        -margin,
        container.depth + margin
    )

    axis.set_aspect("equal")

    axis.set_xlabel("Container width")
    axis.set_ylabel("Container depth")

    axis.set_title(
        f"{title}\n"
        f"{instance.name} — fitness: {fitness:.2f}"
    )

    axis.text(
        container.width / 2,
        container.depth + (margin * 0.4),
        "REAR",
        horizontalalignment="center",
        fontweight="bold"
    )

    axis.text(
        container.width / 2,
        -(margin * 0.7),
        "FRONT",
        horizontalalignment="center",
        fontweight="bold"
    )

    axis.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    axis.legend()

    plt.tight_layout()
    plt.show()