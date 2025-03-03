import random

STEP_SIZE = 50
START = 50
END = 2000
RANDOM_GEN_COUNT = 5

def generator_1(element_count):
    arr = []
    for element in range(1,element_count+1):
        arr.append(element)
    return arr

def generator_2(element_count):
    arr = []
    for element in range(element_count, 0, -1):
        arr.append(element)
    return arr

def generator_3(element_count):
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

def generator_4(element_count):
    arr = []

    def bst_traversal(lower, upper):
        if lower > upper:
            return
        mid = (lower+upper)//2
        bst_traversal(lower, mid-1)
        bst_traversal(mid+1, upper)
        arr.append(mid)

    bst_traversal(1, element_count)
    
    return arr

def generator_5(element_count, seed=42):
    arr = list(range(1, element_count + 1))
    
    random.seed(seed)
    random.shuffle(arr)
    
    return arr

def write_array(arr):
    with open("test_data.txt", "a") as file:  # "w" mode overwrites existing content
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

        for arr_num in range(RANDOM_GEN_COUNT):
            arr = generator_5(element_count, arr_num)
            write_array(arr)
