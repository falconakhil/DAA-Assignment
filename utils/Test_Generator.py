import random

STEP_SIZE = 50
START = 50
END = 2000

def generator_1(element_count): # Generates list sorted in increasing order
    arr = []
    for element in range(1,element_count+1):
        arr.append(element)
    return arr

def generator_2(element_count): # Generates list sorted in decreasing order
    arr = []
    for element in range(element_count, 0, -1):
        arr.append(element)
    return arr

def generator_3(element_count): # Generates list as if the elements were obtained from preorder traversal of balanced BST
    arr = []

    def bst_traversal(lower, upper):
        if lower > upper:
            return
        mid = (lower+upper)//2
        arr.append(mid)
        bst_traversal(lower, mid-1)
        bst_traversal(mid+1, upper)
    
    bst_traversal(1, element_count)

    return arr

def generator_4(element_count): # Generates list as if the elements were obtained from postorder traversal of balanced BST
    arr = []

    def bst_traversal(lower, upper):
        if lower > upper:
            return
        mid = (lower+upper)//2
        bst_traversal(mid+1, upper)
        bst_traversal(lower, mid-1)
        arr.append(mid)

    bst_traversal(1, element_count)
    
    return arr

def generator_5(element_count, seed=42): # Generates list with elements arranged randomly
    arr = list(range(1, element_count + 1))
    
    random.seed(seed)
    random.shuffle(arr)
    
    return arr

def write_array(arr): # Function for writing into a file
    with open("test_data.txt", "a") as file:  # "a" mode appends to the existing content
        file.write(f'{len(arr)}\n')
        for num in arr:
            file.write(f'{num}\n')

if __name__ == '__main__':

    for element_count in range(START, END+1, STEP_SIZE):
        
        arr = generator_1(element_count)
        write_array(arr)

        arr = generator_2(element_count)
        write_array(arr)

        arr = generator_3(element_count)
        write_array(arr)

        arr = generator_4(element_count)
        write_array(arr)

        # Dynamically varying the number of randomly generated examples for all files
        for arr_num in range(element_count):
            arr = generator_5(element_count, seed = ((arr_num * 43) % 7))
            write_array(arr)
