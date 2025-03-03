def load_testcases(filepath):
    """
    Read test cases from a text file structured with multiple blocks as:
    [n1]
    [block1_element 1]
    [block1_element 2]
    ...
    [block1_element n1]
    [n2]
    [block2_element 1]
    [block2_element 2]
    ...
    [block2_element n2]
    ...and so on
    
    Args:
        filepath (str): Path to the test case file
        
    Returns:
        list: List of lists, where each inner list contains the elements of one block
    """
    all_blocks = []
    
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            i = 0
            
            while i < len(lines):
                try:
                    # Try to read the block size
                    n = int(lines[i].strip())
                    i += 1
                    
                    # Read n elements for this block
                    block_elements = []
                    for j in range(n):
                        if i + j < len(lines):
                            element = lines[i + j].strip()
                            # Try to convert to integer or float if possible
                            try:
                                if '.' in element:
                                    element = float(element)
                                else:
                                    element = int(element)
                            except ValueError:
                                # Keep as string if conversion fails
                                pass
                            
                            block_elements.append(element)
                    
                    # Verify we read exactly n elements
                    if len(block_elements) != n:
                        print(f"Warning: Block starting at line {i-1}: Expected {n} elements but read {len(block_elements)}")
                    
                    all_blocks.append(block_elements)
                    i += n
                
                except ValueError:
                    # Skip non-integer lines that might be separators or comments
                    i += 1
                    continue
                    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
    except Exception as e:
        print(f"Error reading test case file: {e}")
    
    return all_blocks