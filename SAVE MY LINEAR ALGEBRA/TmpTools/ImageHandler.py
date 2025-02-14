import pygame

pygame.init()


def HandleRoomImage():

    room_name = "catacombs"

    image = pygame.image.load(f"data/textures/room/{room_name}.png")

    # Get the dimensions of the full image
    image_width, image_height = image.get_size()

    # Calculate the size of each tile
    tile_width = image_width // 2
    tile_height = image_height // 2

    # Extract the four tiles using subsurface
    top_left = image.subsurface((0, 0, tile_width, tile_height))
    top_right = image.subsurface((tile_width, 0, tile_width, tile_height))
    bottom_left = image.subsurface((0, tile_height, tile_width, tile_height))
    bottom_right = image.subsurface((tile_width, tile_height, tile_width, tile_height))

    # Transform the four corners
    transformed_top_left = pygame.transform.flip(top_left, False, False)
    transformed_top_right = pygame.transform.flip(
        top_right, True, False  # Flip horizontally
    )
    transformed_bottom_left = pygame.transform.flip(
        bottom_left, False, True  # Flip Vertically
    )
    transformed_bottom_right = pygame.transform.rotate(
        bottom_right, 180
    )  # Rotate 180 degrees

    # Create a new surface to assemble the room
    room_width = tile_width * 2
    room_height = tile_height * 2
    room = pygame.Surface((room_width, room_height))

    # Blit the transformed tiles into the correct positions
    room.blit(transformed_top_left, (0, 0))  # Top-left corner
    room.blit(transformed_top_right, (tile_width, 0))  # Top-right corner
    room.blit(transformed_bottom_left, (0, tile_height))  # Bottom-left corner
    room.blit(
        transformed_bottom_right, (tile_width, tile_height)
    )  # Bottom-right corner

    # Save the resulting room image
    pygame.image.save(room, f"Src/Textures/Map/{room_name}.png")


def HandleDoorImage():

    door_image = pygame.image.load("data/textures/room/doors.png")

    image_width, image_height = door_image.get_size()

    door_types = ["Stone", "BlueWomb", "Blood", "Devil", "Treasure"]

    for i in range(5):
        door_closed = door_image.subsurface(
            ((3 + i) * image_width // 11, 0, image_width // 11, image_height // 6)
        )
        door_open = door_image.subsurface(
            (
                (3 + i) * image_width // 11,
                image_height // 5,
                image_width // 11,
                image_height // 6,
            )
        )
        pygame.image.save(
            door_closed, f"Src/Textures/Map/Closed{door_types[i]}Door.png"
        )
        pygame.image.save(door_open, f"Src/Textures/Map/Open{door_types[i]}Door.png")


# HandleRoomImage()
# HandleDoorImage()

pygame.quit()
