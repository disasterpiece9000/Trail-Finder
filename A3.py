from tkinter import Canvas, Tk, messagebox


# Create the 2D maze array from the text file
def read_maze():
    file = open("maze.txt", "r")
    lines = file.readlines()
    maze = []
    for line in lines:
        # Strip out new line character from each line
        maze.append([int(char) for char in line if char != "\n"])
    return maze


# Find the coordinates of each cell with a value of 0 on the first two rows
def get_original_seeds(maze):
    seeds = []
    for y in range(2):
        for x in range(len(maze[y])):
            if maze[y][x] == 0:
                seeds.append((x, y))
    return seeds


# Get a list of all neighboring cells from the current one
def get_neighbors(current_pixel, maze):
    # Difference in X/Y coordinates from current cell to neighbors
    neighbor_diffs = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
    neighbors = []
    
    for diff in neighbor_diffs:
        new_x = current_pixel[0] + diff[0]
        new_y = current_pixel[1] + diff[1]
        
        # Don't return neighbor if it's out of bounds
        if new_x < 0 or new_x > len(maze[0]) - 1 or new_y < 0 or new_y > len(maze) - 1:
            continue
            
        neighbors.append((new_x, new_y))
    
    return neighbors


# Explore a given starting point
def find_path(seed, maze):
    path = []   # Cells that are accessible from starting point
    to_explore = [seed]  # Cells that have not been fully explored
    path_found = False   # Was a path found that reached the bottom of the grid
    
    while len(to_explore) > 0:
        current_pixel = to_explore[0]
        to_explore.remove(current_pixel)
        
        # Check if the path reached the bottom of the grid
        if current_pixel[1] == len(maze) - 1:
            path_found = True
        
        current_value = maze[current_pixel[1]][current_pixel[0]]
        neighbors = get_neighbors(current_pixel, maze)
        
        valid_neighbor_found = False
        for neighbor in neighbors:
            # Skip neighbors that have already been seen
            if neighbor in path or neighbor in to_explore:
                continue
                
            neighbor_value = maze[neighbor[1]][neighbor[0]]
            
            if current_value == 0 or neighbor_value == 0:
                path.append(neighbor)
                to_explore.append(neighbor)
                valid_neighbor_found = True
        
        # Remove the current cell if it doesn't expand the path
        if not valid_neighbor_found:
            path.remove(current_pixel)
      
    if path_found:
        return path
    else:
        return False
    

def main():
    maze = read_maze()
    
    # Create the initial maze grid
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                color = "black"
            else:
                color = "white"
            Canvas(master, width=25, height=25, bg=color).grid(row=y, column=x)
    
    path = None
    original_seeds = get_original_seeds(maze)
    
    # Explore all original seeds
    for seed in original_seeds:
        path_found = find_path(seed, maze)
        
        if path_found:
            path = path_found
            break
     
    # No path found
    if not path:
        messagebox.showinfo(":(", "No path was found")
        master.destroy()
        
    # Display path on grid
    else:
        for pixel in path:
            master.after(50, Canvas(master, width=25, height=25, bg="green").grid(row=pixel[1], column=pixel[0]))
            master.update()

    master.mainloop()
    

master = Tk()
main()
