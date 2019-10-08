import math


def create_rivers(layer, map_size_x, map_size_y, tile_heights):

    def apply_water_sprites(layer):

        def calculate_water_sprite(x, y):
            from mapGenerator2 import out_of_bounds

            tiles_around = []
            for around in range(0, 9):
                path_around = (layer.get((x + (around % 3) - 1, y + math.floor(around / 3) - 1), "0"))
                if "p_" not in str(path_around) and (
                        "pd_" in str(path_around) or "b_" in str(path_around) or "pl_" in str(
                        path_around) or out_of_bounds(x + (around % 3) - 1, y + math.floor(around / 3) - 1)):
                    tiles_around.append(1)
                else:
                    tiles_around.append(0)
            if tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return 0
            elif tiles_around[1] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "1"
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[5] == 1:
                return "2"
            elif tiles_around[1] == 1 and tiles_around[3] == 1 and tiles_around[7] == 1:
                return "3"
            elif tiles_around[3] == 1 and tiles_around[5] == 1 and tiles_around[7] == 1:
                return "4"
            elif tiles_around[5] == 1 and tiles_around[7] == 1:
                return "5"
            elif tiles_around[1] == 1 and tiles_around[5] == 1:
                return "6"
            elif tiles_around[1] == 1 and tiles_around[3] == 1:
                return "7"
            elif tiles_around[3] == 1 and tiles_around[7] == 1:
                return "8"
            elif tiles_around[3] == 1 and tiles_around[5] == 1:
                return "13"
            elif tiles_around[1] == 1 and tiles_around[7] == 1:
                return "14"
            elif tiles_around[1] == 1:
                return "9"
            elif tiles_around[3] == 1:
                return "10"
            elif tiles_around[5] == 1:
                return "12"
            elif tiles_around[7] == 1:
                return "11"
            return "15"

        for (x, y) in layer:
            if "pd_" in layer.get((x, y), "") or "b_" in layer.get((x, y), ""):
                water_sprite = calculate_water_sprite(x, y)
                layer[(x, y)] = str(layer[(x, y)]) + str(water_sprite)

    for y in range(0, map_size_y):
        for x in range(0, map_size_x):
            tile_height = tile_heights[(x, y)]
            if tile_height == 0:
                layer[(x, y)] = "pd_"

    apply_water_sprites(layer)


def create_beach(layer, map_size_x, map_size_y, tile_heights):

    def check_for_water_around(layer, x, y, beach_width):
        for around in range(0, (beach_width + 2) ** 2):
            check_x = x + around % (beach_width + 2) - beach_width + 1
            check_y = y + around // (beach_width + 2) - beach_width + 1
            water_around = layer.get((check_x, check_y), "")
            if "pd_" in str(water_around):  # or "p_4" in str(water_around):
                return True
        return False

    for y in range(0, map_size_y):
        for x in range(0, map_size_x):
            if check_for_water_around(layer, x, y, 4) and (x, y) not in layer.keys() and tile_heights.get((x, y), 0) == 1: layer[(x, y)] = "p_4"
