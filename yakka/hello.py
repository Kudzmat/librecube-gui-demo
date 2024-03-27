from pathlib import Path
from enum import IntEnum
from gui_executor.exec import exec_task, FileName, Directory

HERE = Path(__file__).parent.resolve()

images = {"test picture": "FRONT_VIEW8K"}

# rover starts at base
distance_travelled = {
    "NORTH": 0,
    "SOUTH": 0,
    "EAST": 0,
    "WEST": 0
}


class CameraName(IntEnum):
    FRONT_View8k = 1
    BACK_VIEW8k = 2
    DRONE_VIEW4k = 3
    DRONE_VIEW360 = 4


class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


def north_movement():
    # north movement
    if distance_travelled["SOUTH"] == 0:
        distance_travelled["NORTH"] += 5

    elif distance_travelled["SOUTH"] > 0:
        distance_travelled["SOUTH"] -= 5

        # reset to zero if it goes past
        if distance_travelled["SOUTH"] < 0:
            distance_travelled["SOUTH"] = 0

    else:
        pass


def south_movement():
    if distance_travelled["NORTH"] == 0:
        distance_travelled["SOUTH"] += 5

    elif distance_travelled["NORTH"] > 0:
        distance_travelled["NORTH"] -= 5

        # reset to zero if it goes past
        if distance_travelled["NORTH"] < 0:
            distance_travelled["NORTH"] = 0

    else:
        pass


def west_movement():
    if distance_travelled["EAST"] == 0:
        distance_travelled["WEST"] += 5

    elif distance_travelled["EAST"] > 0:
        distance_travelled["EAST"] -= 5

        # reset to zero if it goes past
        if distance_travelled["EAST"] < 0:
            distance_travelled["EAST"] = 0

    else:
        pass


def east_movement():
    if distance_travelled["WEST"] == 0:
        distance_travelled["EAST"] += 5

    elif distance_travelled["WEST"] > 0:
        distance_travelled["WEST"] -= 5

        # reset to zero if it goes past
        if distance_travelled["WEST"] < 0:
            distance_travelled["WEST"] = 0

    else:
        pass


@exec_task(capture_response="total_distance")
def move_rover(direction: Direction, distance: int = 5):
    # north movement
    if direction.name == "NORTH":
        north_movement()

    # south movement
    elif direction.name == "SOUTH":
        south_movement()

    # east movement
    elif direction.name == "EAST":
        east_movement()

    # west movement
    elif direction.name == "WEST":
        west_movement()

    total_distance = sum(distance_travelled.values())

    message = f"Rover has moved 5km {direction.name} and is now {total_distance}km from the base"

    return message, str(total_distance)


@exec_task()
def get_rover_location():
    total_distance = sum(distance_travelled.values())
    if total_distance == 0:
        print("Rover is currently parked at the base camp.")

    else:
        print("Rover is currently:")
        for direction, distance in distance_travelled.items():
            if distance > 0:
                print(f"{distance}km {direction}")
            else:
                pass


@exec_task()
def image_gallery():
    from rich.table import Table
    table = Table(title=f"Image Gallery")

    table.add_column("Image Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Camera", style="magenta")
    # table.add_column("Number", justify="center", style="green")

    for name, camera in images.items():
        table.add_row(name, camera)

    return table


@exec_task(capture_response='new_image')
def capture_image(camera: CameraName, image_name: str, location: Directory = Path("~/data/images")):
    images[image_name] = f'{camera.name}'

    message = (
        f"Captured image '{image_name}' from camera '{camera.name}.'"
        f"saving it as {image_name=} at {location=}."
    )

    return message
