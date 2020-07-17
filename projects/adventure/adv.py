from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
trav = []


# def get_direction():
#     if player.current_room.get_room_in_direction('n') is not None:
#         traversal_path.append('n')
#         player.travel('n')
#         if player.current_room.id not in trav:
#             trav.append(player.current_room.id)
#     elif player.current_room.get_room_in_direction('e') is not None and i not in trav:
#         traversal_path.append('e')
#         player.travel('e')
#         trav.append(i)
#     elif player.current_room.get_room_in_direction('w') is not None and i not in trav:
#         traversal_path.append('w')
#         player.travel('w')
#         trav.append(i)
#     elif player.current_room.get_room_in_direction('s') is not None:
#         traversal_path.append('s')
#         player.travel('s')
#         trav.append(player.current_room.id)

def get_random():
    rand = random.randint(0, 3)
    if rand == 0:
        return 'n'
    elif rand == 1:
        return 'e'
    elif rand == 2:
        return 's'
    elif rand == 3:
        return 'w'


trav.append(player.current_room.id)


def traverse():
    # print(player.current_room.get_room_in_direction('n').get_coords())
    while len(trav) < len(room_graph):
        rand = get_random()
        if player.current_room.get_room_in_direction(rand) is not None:
            traversal_path.append(rand)
            player.travel(rand)
            if player.current_room.id not in trav:
                trav.append(player.current_room.id)
        traverse()
        # elif player.current_room.get_room_in_direction('e') is not None and i not in trav:
        #     traversal_path.append('e')
        #     player.travel('e')
        #     trav.append(i)
        # elif player.current_room.get_room_in_direction('w') is not None and i not in trav:
        #     traversal_path.append('w')
        #     player.travel('w')
        #     trav.append(i)
        # elif player.current_room.get_room_in_direction('s') is not None:
        #     traversal_path.append('s')
        #     player.travel('s')
        #     trav.append(player.current_room.id)
        # else:
        #     trav.append('No place left to go')
        print("TRAV", trav)


traverse()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
