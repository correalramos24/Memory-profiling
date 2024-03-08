
import argparse

parser = argparse.ArgumentParser(description="Memory sampling script")

parser.add_argument('--files', 
                    help="Input files, can use wildcard like *", nargs="+")
parser.add_argument('--samp', required=True, 
                    help='Sampling time')
parser.add_argument('--save', default=None, 
                    help="Enable and define save file name")
parser.add_argument('--swap', action='store_true', 
                    help="Enable swap plotting")
parser.add_argument('--total', action='store_true', 
                    help="Enable total memory available?")
parser.add_argument('--percentage', action='store_true', 
                    help="Plot perc of usage")
parser.add_argument('--legend', action='store_true', 
                    help="Plot legend")
parser.add_argument('--output_units', default="KiB", 
                    help="Set output units for the plots")
parser.add_argument('--output_scale', default=1, 
                    help="Factor that will be divide the memory results")
parser.add_argument('--file_pattern', 
                    help="Set the file pattern for the input files", 
                    default="mem.log")
app_args = parser.parse_args()

files  : list[str] = app_args.files
sampl  : int  = int(app_args.samp)

swap   : bool = app_args.swap
total  : bool = app_args.total
percnt : bool = app_args.percentage

legend : bool = app_args.legend
save   : str  = app_args.save

unit_o : str  = app_args.output_units
unit_s : int  = int(app_args.output_scale)

f_pat  : str  = app_args.file_pattern