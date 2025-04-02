import random
import os
import json
import argparse

def getCyclicKeys(cube):
    keys = []
    keys.append(f"{cube['q']},{cube['r']},{cube['s']}")
    keys.append(f"{cube['r']},{cube['s']},{cube['q']}")
    keys.append(f"{cube['s']},{cube['q']},{cube['r']}")
    return list(set(keys))

def generateDanger(groupArray, selectedCells, radius):
    def checkConnected(dangerCells, radius):
        directions = [
            {"q": 1, "r": -1, "s": 0},
            {"q": 1, "r": 0, "s": -1},
            {"q": 0, "r": 1, "s": -1},
            {"q": -1, "r": 1, "s": 0},
            {"q": -1, "r": 0, "s": 1},
            {"q": 0, "r": -1, "s": 1}
        ]

        def getNeighbors(cube):
            neighbors = []
            for dir in directions:
                neighbor = {"q": cube["q"] + dir["q"], "r": cube["r"] + dir["r"], "s": cube["s"] + dir["s"]}
                if max(abs(neighbor["q"]), abs(neighbor["r"]), abs(neighbor["s"])) <= radius:
                    key = f"{neighbor['q']},{neighbor['r']},{neighbor['s']}"
                    neighbors.append(key)
            return neighbors

        visited = set()
        queue = []

        # Find first non-danger cell to start BFS
        for q in range(-radius, radius + 1):
            r1 = max(-radius, -q - radius)
            r2 = min(radius, -q + radius)
            found = False
            for r in range(r1, r2 + 1):
                s = -q - r
                key = f"{q},{r},{s}"
                if key not in dangerCells:
                    queue.append(key)
                    visited.add(key)
                    found = True
                    break
            if found:
                break

        # BFS to find all reachable non-danger cells
        while queue:
            currentKey = queue.pop(0)
            q, r, s = map(int, currentKey.split(","))
            currentCube = {"q": q, "r": r, "s": s}
            neighbors = getNeighbors(currentCube)

            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in dangerCells:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Check if all non-danger cells are visited
        for q in range(-radius, radius + 1):
            r1 = max(-radius, -q - radius)
            r2 = min(radius, -q + radius)
            for r in range(r1, r2 + 1):
                s = -q - r
                key = f"{q},{r},{s}"
                if key not in dangerCells and key not in visited:
                    return False

        return True

    def validateDanger(dangerCells, radius):
            return checkConnected(dangerCells, radius)

    dangerCells = set()
    for i in range(10):
        dangerProb = (random.random() * 0.6) + 0.2
        for group in groupArray:
            if random.random() < dangerProb:
                for key in group:
                    dangerCells.add(key)

        if validateDanger(dangerCells, radius):
            break
        dangerCells.clear()

    for key in dangerCells:
        selectedCells[key] = {"type": "danger"}

def generateShield(groupArray, selectedCells):
    shieldAvailableGroups = [g for g in groupArray if len(g) == 3 and g[0] not in selectedCells]
    if shieldAvailableGroups:
        shieldGroup = shieldAvailableGroups[random.randint(0, len(shieldAvailableGroups) - 1)]
        for key in shieldGroup:
            selectedCells[key] = {"type": "shield"}

def generateGold(groupArray, selectedCells):
    goldProd = 0.2
    countGold = 0
    while countGold < 300:
        group = groupArray[random.randint(0, len(groupArray) - 1)]
        if countGold >= 300:
            return
        if group[0] in selectedCells and selectedCells[group[0]]["type"] != "gold":
            continue
        count = 0
        if group[0] in selectedCells:
            count += selectedCells[group[0]]["count"]
        if count >= 6:
            continue
        addedCount = min(round((300 - countGold) / 3), 6 - count, round(random.random() * 2) + 1)
        if len(group) == 1:
            addedCount = min(300 - countGold, 6 - count, 3)
        for key in group:
            selectedCells[key] = {"type": "gold", "count": count + addedCount}
        countGold += addedCount * len(group)

def exportMap(selectedCells, radius, max_moves):
    mapData = {
        "map_radius": radius,
        "max_moves": max_moves,
        "cells": []
    }

    for key in selectedCells:
        q, r, s = map(int, key.split(","))
        tile = selectedCells[key]
        value = None

        if tile["type"] == "gold":
            value = tile["count"]
        elif tile["type"] == "danger":
            value = "D"
        elif tile["type"] == "shield":
            value = "S"

        mapData["cells"].append({"q": q, "r": r, "s": s, "value": value})

    existing_files = [f for f in os.listdir("maps") if f.startswith("map_") and f.endswith(".json")]

    if existing_files:
        map_numbers = [int(f.split("_")[1].split(".")[0]) for f in existing_files]
        next_map_number = max(map_numbers) + 1
    else:
        next_map_number = 1

    file_path = os.path.join("maps", f"map_{next_map_number}.json")

    with open(file_path, "w") as f:
        json.dump(mapData, f, indent=2)

    return mapData

def generateMap(radius=10, max_moves=100):
    groups = {}
    for q in range(-radius, radius + 1):
        r1 = max(-radius, -q - radius)
        r2 = min(radius, -q + radius)
        for r in range(r1, r2 + 1):
            s = -q - r
            cube = {"q": q, "r": r, "s": s}
            keys = getCyclicKeys(cube)
            canonical = "|".join(sorted(keys))
            if canonical not in groups:
                groups[canonical] = keys

    groupArray = list(groups.values())
    selectedCells = {}

    activeTile = ""
    if activeTile == "danger":
        pass
    elif activeTile == "shield":
        pass
    elif activeTile == "gold":
        pass
    else:
        generateDanger(groupArray,selectedCells,radius)
        generateShield(groupArray,selectedCells)
        generateGold(groupArray,selectedCells)

    exportMap(selectedCells, radius, max_moves)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate Map")
    parser.add_argument("--num", default=10, help="Number of maps for each radius")
    return parser.parse_args()

def main():
    args = parse_args()

    folder_path = "maps"
    if os.path.exists(folder_path):
       os.system(f"rm -rf {folder_path}")
    os.makedirs(folder_path)

    radiuss = []
    for num in range(8,16):
        radiuss.extend([num] * int(args.num))

    for radius in radiuss:
        max_moves = random.randint(50,150)
        generateMap(radius, max_moves)

if __name__ == "__main__":
    main()
