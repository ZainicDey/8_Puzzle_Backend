from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from queue import Queue

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    for r, c in moves:
        new_row, new_col = r + row, c + col
        if 0 <= new_row <= 2 and 0 <= new_col <= 2:
            new_index = 3 * new_row + new_col
            neighbor = state[:]
            neighbor[new_index], neighbor[zero_index] = neighbor[zero_index], neighbor[new_index]
            neighbors.append(neighbor)
    return neighbors

from queue import Queue

def bfs_puzzle(start, goal):
    queue = Queue()
    visited = set()
    queue.put((start, []))  

    while not queue.empty():
        current_state, path = queue.get()

        if current_state == goal:
            return path + [current_state]

        if tuple(current_state) not in visited:
            visited.add(tuple(current_state))

            for neighbor in get_neighbors(current_state):
                if tuple(neighbor) not in visited:
                    queue.put((neighbor, path + [current_state]))

    print("No solution found using BFS.")
    return None


@csrf_exempt
def solve_puzzle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        initial_state = data.get('state')
        solution_paths = bfs_puzzle(initial_state, [1, 2, 3, 4, 5, 6, 7, 8, 0])
        if solution_paths:
            return JsonResponse({'solution_paths': solution_paths})
        else :
            return JsonResponse({'error': 'No solution found'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
