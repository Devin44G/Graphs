from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def bfs(starting_vertex):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    q = Queue()
    q.enqueue([starting_vertex])
    travelled_to = []
    while q.size() is not None:
        path = q.dequeue()
        current_node = path[-1]

        if '?' in visited[current_node].values():
            return path

        if current_node not in travelled_to:
            travelled_to.append(current_node)
            for room in visited[current_node].values():
                new_path = path[:]
                new_path.append(room)
                q.enqueue(new_path)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
trav = []


def map_to_visited():
    visited[player.current_room.id] = {}
    for exit in player.current_room.get_exits():
        visited[player.current_room.id][exit] = '?'


map_to_visited()


# def get_random():  <= PART OF PHASE 2
#     rand = random.randint(0, 3)
#     if rand == 0:
#         return 'n'
#     elif rand == 1:
#         return 'e'
#     elif rand == 2:
#         return 's'
#     elif rand == 3:
#         return 'w'


def get_opposite(letter):
    if letter == 'n':
        return 's'
    elif letter == 's':
        return 'n'
    elif letter == 'e':
        return 'w'
    elif letter == 'w':
        return 'e'


def traverse():
    travelled_to = []
    while len(trav) < len(room_graph):  # <= FINAL PHASE - PHASE 3
        travelled_to.append(player.current_room.id)
        not_visited = [key for key, val in visited[player.current_room.id].items() if val == '?']
        next = None
        if not_visited:
            next = random.choice(not_visited)
            came_from = player.current_room.id
            player.travel(next)
            traversal_path.append(next)
            if player.current_room.id not in trav:
                trav.append(player.current_room.id)
            visited[came_from][next] = player.current_room.id
            if player.current_room.id not in visited:
                map_to_visited()
            visited[player.current_room.id][get_opposite(next)] = came_from

        if next == None:
            origin = bfs(player.current_room.id)
            if origin:
                for room in origin:
                    for key, val in visited[player.current_room.id].items():
                        if val == room:
                            player.travel(key)
                            traversal_path.append(key)
                            if player.current_room.id not in trav:
                                trav.append(player.current_room.id)

        # rand = get_random()  <= PHASE 2
        # if player.current_room.get_room_in_direction(rand) is not None:
        #     traversal_path.append(rand)
        #     player.travel(rand)
        #     print("ROOM", player.current_room.get_room_in_direction(rand))
        #     if player.current_room.id not in trav:
        #         trav.append(player.current_room.id)
        #     exit = player.current_room.get_exits()
        #     for e in exit:
        #         traversal_path.append(e)
        #         player.travel(e)
        #         if player.current_room.id not in trav:
        #             trav.append(player.current_room.id)
        #         traversal_path.append(get_opposite(e))
        #         player.travel(get_opposite(e))
        #         if player.current_room.id not in trav:
        #             trav.append(player.current_room.id)
        # else:
        #     rand = get_random()
        print("TRAV", trav)


traverse()

# def get_direction():  <= PHASE 1
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
