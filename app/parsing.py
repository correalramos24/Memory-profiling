
from definitions import *

# Memtrace tuples fields = host_info, main_mem_info, swap_info
# Each of _mem_info contain total used free fileds


def parse_mem_file(fPath, get_swap_info: bool = False, file_pattern="-mem.log"):
    # Parse the hostname from the input file:
    filename = fPath
    if "/" in fPath:
        filename = fPath.split('/')[-1]
    
    hostname = filename.split(file_pattern)[0]

    results = MemoryResults(hostname, get_swap_info)

    # Parse the file and accum data:
    print(f"Parsing {fPath} file ...", end="")
    with open(fPath, mode='r') as mem_file:
        for line in mem_file.readlines():
            if "Mem: " in line:
                results.append_main_mem(tuple(line.strip().split()[1:4]))
            if get_swap_info and "Swap: " in line:
                results.append_swap_mem(tuple(line.strip().split()[1:4]))

    results.check_integrity()
        
    print(f" DONE! Found {results.get_num_records()} records")

    return results