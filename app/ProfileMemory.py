from collections import namedtuple
import numpy as np
import os

MemRecord = namedtuple("MemRecord", "total used free")
MemTrace = namedtuple("MemTrace", "host main_mem_info swap_meminfo", defaults=([], []))

class ProfileMemory:

    def __init__(self, memData: dict[MemTrace] = None, sampling_time: int = None, units: str = None) -> None:
        self.sampling_time = int(sampling_time)
        self.units = units
        if memData is None:
            self.data_per_host = {}
        else:
            self.data_per_host = memData

    def NewplotDataPLT(self, plot_format: str, plot_tota_avail: bool=False, 
                    plot_swap: bool = False, plot_legend: bool = False,
                    save : str = None, output_units: str = None):
        
        import matplotlib.pyplot as plt
        import numpy as np

        plot_percentatge=False
        scale_factor=1

        # Check inputs for the plot:
        if len(self.data_per_host) == 0:
            raise Exception("Empty data, can't generate any plot")
        
        if plot_format != 'perc' and plot_format != 'amount':
            raise Exception(f"invalid plotting format selected {plot_format}")
        plot_percentatge = plot_format == 'perc'
        
        if output_units is not None and output_units == "GiB":
            self.units = "GiB"
            scale_factor=2**20

        # Convert data & plot, taking care of plot_percentatge
        fig, ax = plt.subplots()

        for mem_per_host in self.data_per_host.values():
            host = mem_per_host.host
            samp_time = self.getSamplingTime()

            main_mem_used = list(map(lambda x: float(x.used), mem_per_host.main_mem_info))
            main_mem_total = list(map(lambda x: float(x.total), mem_per_host.main_mem_info))
            timing = np.arange(0,  samp_time * len(main_mem_used), samp_time)
            
            if plot_percentatge:
                main_mem_perc = list(map(
                        lambda x : (float(x[0])/float(x[1]))*100,
                        zip(main_mem_used, main_mem_total)
                        )
                    )
                ax.plot(timing, main_mem_perc, label=host+" main mem. % used")
                
                if plot_swap:
                    #TODO: Finish this
                    pass
            else:
                if scale_factor != 1:
                    main_mem_used = list(map(lambda x : x/scale_factor, main_mem_used))
                ax.plot(timing, main_mem_used, label=host+" main mem. used GiB")

                if plot_swap:
                    swap_mem_used = list(map(lambda x: float(x.used), mem_per_host.swap_meminfo))
                    ax.plot(timing, swap_mem_used, label=host+" swap mem. used")
                    if plot_tota_avail:
                        swap_mem_total = list(map(lambda x: float(x.total), mem_per_host.swap_meminfo))
                        ax.plot(timing, swap_mem_total, label=host+" total swap mem.")

                if plot_tota_avail:
                    if scale_factor != 1:
                        main_mem_total = list(map(lambda x : x/scale_factor, main_mem_total))
                    ax.plot(timing, main_mem_total, label=host+" total main mem.")                    


        # Complete the plot & show or store:
        if plot_legend:
            ax.legend()
        if plot_percentatge:
            ax.set_ylabel(f'Memory [%]')
            ax.set_ylim(0,100)
        else:
            plt.ylabel(f'Memory [{self.units}]')

        plt.xlabel(f'Time [s]')
        plt.title('Memory sampling results')

        if save is not None:
            print(save+" generated")
            fig.savefig(save)
        else:
            plt.show()

    def getSamplingTime(self):
        return self.sampling_time

    @staticmethod
    def __parsefile__(file_name, file_pattern="-mem.log") -> MemTrace:
        hostName = file_name.split("-mem.log")[0]
        ret = MemTrace(hostName, [], [])
        print(f"Parsing {file_name} ...", end="")

        with open(file_name, mode='r') as memFile:
            for line in memFile.readlines():
                if "total" in line:
                    continue
                if "Mem:" in line:
                    aux = MemRecord._make(line.strip().split()[1:4])
                    ret.main_mem_info.append(aux)
                if "Swap: " in line:
                    aux = MemRecord._make(line.strip().split()[1:4])
                    ret.swap_meminfo.append(aux)

        if len(ret.main_mem_info) != len(ret.swap_meminfo):
            print("")
            raise Exception("File corrupted, different swap and mem information")
        else:
            print(f" DONE! Found {len(ret.main_mem_info)} records")

        return ret

    @classmethod
    def from_files(cls, file_names, sampling_time, units="KiB"):
        aux_info = dict()
        for file in file_names:
            try:
                info = cls.__parsefile__(file)
                if info.host in aux_info:
                    print(f"WARNING! Same node name in the log files detected! ({info.host})")
                    print("This file will not be plotted!")
                else:
                    aux_info[info.host] = info
            except Exception:
                print(f"Can't parse {file} file, skipping")

        return ProfileMemory(aux_info, sampling_time, units)

    @classmethod
    def from_folder(cls, folder, sampling_time, units="KiB"):
        aux_info = dict()
        for dirpath, _, files in os.walk(folder):
            for file in files:
                try:
                    p = os.path.join(dirpath, file)
                    info = cls.__parsefile__(p)
                    if info.host in aux_info:
                        print(f"WARNING! Same node name in the log files detected! ({info.host})")
                        print("This file will not be plotted!")
                    else:
                        aux_info[info.host] = info
                except Exception:
                    print(f"Can't parse {file} file, skipping")
        return ProfileMemory(aux_info, sampling_time, units)

    @classmethod
    def from_tracing_file(cls, file_name, sampling_time):
        pass
