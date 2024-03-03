#!/bin/python3

import argparse
from ProfileMemory import *

def main():
    # Arg parsing:
    parser = argparse.ArgumentParser(description="Memory tracing postprocessing")
    parser.add_argument('-f', help="Input files", nargs="+")
    parser.add_argument('-s', required=True, help='Sampling time')
    parser.add_argument('--folder', help="Input folder")
    parser.add_argument('--unit', default="KiB", help="Memory units for the input files, KiB by default.")
    parser.add_argument('--save', default=None, help="Enable and define save file name")
    parser.add_argument('--swap', action='store_true', help="Enable swap plotting")
    parser.add_argument('--total', action='store_true', help="Enable total memory available?")
    parser.add_argument('--percentatge', action='store_true', help="Plot % of usage")
    parser.add_argument('--legend', action='store_true', help="Plot legend")
    parser.add_argument('--output_units', default=None, help="Set output units for the plots (Supported GiB)")
    #parser.add_argument('--file_pattern', help="Set the file pattern for the input files", default="-mem.log")
    args = parser.parse_args()

    files  : list[str] = args.f
    folder : str  = args.folder
    sampl  : int  = args.s
    save   : str  = args.save
    swap   : bool = args.swap
    total  : bool = args.total
    percnt : bool = args.percentatge
    legend : bool = args.legend
    units  : str  = args.unit
    units_o: str  = args.output_units
    #f_pat  : str  = args.file_pattern
    plot_format='perc' if percnt else 'amount'

    # Parse & plot:
    if files is not None:
        pf_mem = ProfileMemory.from_files(files, sampl, units)
    elif folder is not None:
        print(f"Parsing directory {folder}!")
        pf_mem = ProfileMemory.from_folder(folder, sampl, units)
    else:
        print("You must either provide files or a folder (-f or --folder)")
        exit(1)

    print("Generating the plot...")
    pf_mem.NewplotDataPLT(plot_format, total, swap, legend, save, units_o)

if __name__ == "__main__":
    main()
