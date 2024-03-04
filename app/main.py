#!/bin/python3

import argparse
from parsing import *
from plot import *

def main():
    
    # Argument parsing:
    parser = argparse.ArgumentParser(description="Memory sampling postprocessing")
    parser.add_argument('--files', help="Input files, can use wildcard like *", nargs="+")
    parser.add_argument('--samp', required=True, help='Sampling time')
    parser.add_argument('--save', default=None, help="Enable and define save file name")
    parser.add_argument('--swap', action='store_true', help="Enable swap plotting")
    parser.add_argument('--total', action='store_true', help="Enable total memory available?")
    parser.add_argument('--percentage', action='store_true', help="Plot perc of usage")
    parser.add_argument('--legend', action='store_true', help="Plot legend")
    parser.add_argument('--output_units', default="KiB", help="Set output units for the plots")
    parser.add_argument('--output_scale', default=1, help="Set the factor that will use to divide the data in the files")
    parser.add_argument('--file_pattern', help="Set the file pattern for the input files", default="-mem.log")
    args = parser.parse_args()

    files  : list[str] = args.files
    sampl  : int  = int(args.samp)

    swap   : bool = args.swap
    total  : bool = args.total
    percnt : bool = args.percentage

    legend : bool = args.legend
    save   : str  = args.save
    
    unit_o : str  = args.output_units
    unit_s : int  = int(args.output_scale)

    f_pat  : str  = args.file_pattern

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
