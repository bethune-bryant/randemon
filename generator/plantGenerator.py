from noise import snoise2
import random


# Checks if enough space is available to plant a tree
# No trees above the highest path height
# Adds an overlay to decoration_layer if the top of the tree overlaps with another tree
def create_trees(pmap, spawn_rate, x_offset, y_offset):
    octaves = 2
    freq = 40
    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            if pmap.tile_heights.get((x, y), -1) <= pmap.highest_path:
                if (x, y) not in pmap.ground_layer.keys() and (x, y - 1) not in pmap.ground_layer.keys() and (x, y) not in pmap.buildings.keys() and (x, y) not in pmap.decoration_layer.keys() and (x, y - 1) not in pmap.decoration_layer.keys():
                    if snoise2((x + x_offset) / freq, (y + y_offset) / freq, octaves) + 0.5 < spawn_rate / 100 and random.random() > 0.5:
                        pmap.ground_layer[(x, y)] = "st_0"
                        pmap.ground_layer[(x, y - 1)] = "st_1"
                        if (x, y - 2) not in pmap.ground_layer.keys():
                            pmap.ground_layer[(x, y - 2)] = "st_2"
                        else:
                            pmap.decoration_layer[(x, y - 2)] = "st_2_d"


# The whole map is filled with random green tiles
# Tall gras and flowers are spawned with a perlin noise field
def grow_grass(pmap, tall_grass_coverage, x_offset, y_offset):
    def random_grass(gx, gy):
        octaves = 1
        freq = 7
        sne_probability = snoise2((gx + x_offset) / freq, (gy + y_offset) / freq, octaves) + 0.5

        if pmap.tile_heights.get((gx, gy), -1) <= pmap.highest_path:
            if sne_probability > (tall_grass_coverage / 100) or "l_1" in pmap.decoration_layer.get((gx, gy), "") or "l_5" in pmap.decoration_layer.get((gx, gy), ""):
                grass_type = random.randint(0, 3)
                return "g_" + str(grass_type)
            else:
                sne_type = random.randint(0, 1) * 2
                # Turn 80 percent of the flowers into tall grass
                if sne_type == 2 and random.random() < 0.8: sne_type = 0
                # Turn 0.5 percent of the tall grass into tall grass with a hidden item
                if sne_type == 0 and random.random() < 0.005: sne_type = "0_p"
                return "sne_" + str(sne_type)
        else:
            return "m_0"

    for y in range(pmap.height):
        for x in range(pmap.width):
            if (x, y) not in pmap.ground_layer.keys():
                pmap.grass_layer[(x, y)] = random_grass(x, y)


# Creates an overlay for the entire map showing rain
# The amount of rain is given with rain_rate
def create_rain(pmap, odds,  rain_rate):
    if random.random() * 100 < odds:
        for y in range(pmap.height):
            for x in range(pmap.width):
                if random.randint(0, 100) < rain_rate:
                    if random.random() < 0.5 and "st" not in pmap.ground_layer.get((x, y), "") and "fe_" not in pmap.ground_layer.get((x, y), "") and "m_" not in pmap.ground_layer.get((x, y), ""):
                        pmap.rain[(x, y)] = "r_" + str(random.randint(3, 5))
                    else:
                        pmap.rain[(x, y)] = "r_" + str(random.randint(1, 2))
                else:
                    pmap.rain[(x, y)] = "r_0"
