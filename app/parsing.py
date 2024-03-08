
from definitions import *

def parse_mem_file(fPath, get_swap_info: bool = False, file_pattern="-mem.log"):
    """Parser for a file from free command.
    Args:
        fPath (str): _description_
        get_swap_info (bool, optional): Parse swap also. Defaults to False.
        file_pattern (str, optional): File name pattern for the hostname. 
            Defaults to "-mem.log".

    Returns:
        MemoryResults: all the information from the fPath file.
    """
    
    # 1. Generate hostname str:
    filename = fPath.split('/')[-1] if "/" in fPath else fPath
    hostname = filename.split(file_pattern)[0]
    results = MemoryResults(hostname, get_swap_info)

    # 2. Parse the file and accum data:
    print(f"Parsing {fPath} file ...", end="")
    with open(fPath, mode='r') as mem_file:
        for line in mem_file.readlines():
            if "Mem: " in line:
                results.append_main_mem(tuple(line.strip().split()[1:4]))
            if get_swap_info and "Swap: " in line:
                results.append_swap_mem(tuple(line.strip().split()[1:4]))

    # 3. Check integrity of the results
    results.check_integrity()
        
    print(f" DONE! Found {results.get_num_records()} records")

    return results