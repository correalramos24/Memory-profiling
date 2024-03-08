#!/bin/python3

from arguments import *
from parsing import *
from plot import *

def main():

    plot_format='perc' if percnt else 'amount'

    # Parse the input file:
    results = []

    if files is not None:
        for file in files:
            try:
                results.append(parse_mem_file(file, swap, f_pat))
            except Exception:
                print(f"Can't parse {file} file, skipping")
    else:
        print("Error: No input files found")
        exit(1)
        
    plot_plt_memory_results(results, sampl, plot_format, 
                            legend,total, save, unit_s, unit_o)


if __name__ == "__main__":
    main()
