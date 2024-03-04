
from definitions import *

def plot_plt_memory_results(results: list[MemoryResults], sample_time: int,
                            plot_format : str, plot_legend : bool = False,
                            plot_total : bool = False, save_name : str = None, 
                            output_scale: int = 1, output_units: str = "KiB"):

    import matplotlib.pyplot as plt
    import numpy as np
    
    # Check configs for the plot:
    if plot_format != 'perc' and plot_format != 'amount':
        raise Exception(f"invalid plotting format selected {plot_format}")
    
    plot_percentatge = plot_format == 'perc'

    # Iterate all results and plot, according to the options
    fig, ax = plt.subplots()

    for result in results:
        host = result.get_hostname()
        end_time = result.get_num_records()
        timing = np.arange(0, sample_time * end_time, sample_time)

        # Plot main memory (perc or used) and total
        if plot_percentatge:
            ax.plot(timing, result.get_main_mem_perc(), 
                    label=host+" main memory")
        else:
            ax.plot(timing, result.get_main_mem_used(output_scale), 
                    label=host+" main memory")
            if plot_total:
                ax.plot(timing, result.get_main_mem_avail(output_scale),
                        label=host+" total memory")
        
        # Plot swap if there's data and total:
        if result.is_swap_enabled():
            if plot_percentatge:
                ax.plot(timing, result.get_swap_mem_perc(), 
                        label=host + " swap memory")
            else:
                ax.plot(timing, 
                        result.get_swap_mem_used(output_scale),
                        label=host + " swap memory")
                if plot_total:
                    ax.plot(timing, result.get_swap_mem_avail(output_scale), 
                            label=host+" total swap memory")
    
    # Complete the plot & show or store:
    if plot_legend:
        ax.legend(loc='upper left', bbox_to_anchor=(1,1))

    if plot_percentatge:
        ax.set_ylabel(f'Memory [%]')
        ax.set_ylim(-1,100)
    else:
        ax.set_ylabel(f'Memory [{output_units}]')
            
    ax.set_xlabel('Time [s]')
    fig.set_tight_layout(True)
    if save_name is not None:
        print(save_name+ " generated")
        fig.savefig(save_name)
    else:
        plt.show()
