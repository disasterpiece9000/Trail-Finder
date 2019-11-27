from tkinter import Canvas, Tk
master = Tk()


def read_maze():
    file = open("maze.txt", "r")
    lines = file.readlines()
    maze = []
    for line in lines:
        maze.append([int(char) for char in line if char != "\n"])
    return maze


def get_original_seeds(maze):
    seeds = []
    for y in range(2):
        for x in range(len(maze[y])):
            if maze[y][x] == 0:
                seeds.append((x, y))
    return seeds


def get_neighbors(current_pixel, maze):
    neighbors = []
    neighbor_diffs = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
    
    for diff in neighbor_diffs:
        new_x = current_pixel[0] + diff[0]
        new_y = current_pixel[1] + diff[1]
        
        if new_x < 0 or new_x > len(maze[0]) - 1 or new_y < 0 or new_y > len(maze) - 1:
            continue
            
        neighbors.append((new_x, new_y))
    
    return neighbors


def find_path(seed, original_seeds, maze):
    path = []
    to_explore = [seed]
    while len(to_explore) > 0:
        current_pixel = to_explore[0]
        to_explore.remove(current_pixel)
        
        if current_pixel[1] == len(maze) - 1:
            return path
        
        current_value = maze[current_pixel[1]][current_pixel[0]]
        neighbors = get_neighbors(current_pixel, maze)
        
        for neighbor in neighbors:
            if neighbor in path or neighbor in to_explore:
                continue
                
            neighbor_value = maze[neighbor[1]][neighbor[0]]
            if current_value == 0 or neighbor_value == 0:
                path.append(neighbor)
                to_explore.append(neighbor)
                
    return False
    

def main():
    maze = read_maze()
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                color = "red"
            else:
                color = "white"
            Canvas(master, width=25, height=25, bg=color).grid(row=y, column=x)
    
    original_seeds = get_original_seeds(maze)
    
    path = False
    for seed in original_seeds:
        path_found = find_path(seed, original_seeds, maze)
        if path_found:
            path = path_found
            break
    
    for pixel in path:
        Canvas(master, width=25, height=25, bg="yellow").grid(row=pixel[1], column=pixel[0])
    
    master.mainloop()


main()
