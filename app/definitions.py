
class MemoryResults:
    """
    Holds the info for the main memory and the swap memory.
    Each memory record contains: 
        0 : the total available in the system.
        1 : the consumed memory in the system.
        2 : the free memory in the system.
    """

    def __init__(self, hostname: str, with_swap_info: bool=False) -> None:
        self.hostname = hostname
        self.main_info = []
        self.swap_info = [] if with_swap_info else None            

    def append_main_mem(self, main_info):
        self.main_info.append(main_info)

    def append_swap_mem(self, swap_info):
        self.swap_info.append(swap_info)
        
    def check_integrity(self):
        if self.swap_info is None: 
            return
        if len(self.swap_info) != len(self.main_info):
            raise Exception("File corrupted, different swap \
                            and mem information")

    def get_num_records(self):
        return len(self.main_info)
    
    def get_hostname(self): 
        return self.hostname
    
    def is_swap_enabled(self):
        return self.swap_info != None
    
    #=========GETTERS MAIN MEM=======
    def get_main_mem_used(self, scale_factor=1):
        return list(map(lambda x : int(x[1])/scale_factor, self.main_info))
    
    def get_main_mem_avail(self, scale_factor=1):
        return list(map(lambda x : int(x[0])/scale_factor, self.main_info))
    
    #=========GETTERS SWAP MEM=======
    def get_swap_mem_used(self, scale_factor=1):
        return list(map(lambda x : int(x[1])/scale_factor, self.swap_info))
    
    def get_swap_mem_avail(self, scale_factor=1):
        return list(map(lambda x : int(x[0])/scale_factor, self.swap_info))

    #=========GETTERS % MEM=======
    def get_main_mem_perc(self):
        mem_used_data = self.get_main_mem_used()
        total_mem_data = self.get_main_mem_avail()

        return list(
                    map(lambda x : (x[0] / x[1]) * 100, 
                    zip(mem_used_data, total_mem_data)
                ))
    
    def get_swap_mem_perc(self):
        swap_used_data = self.get_swap_mem_used()
        total_swap_data = self.get_swap_mem_avail()

        return list(
                    map(lambda x : (x[0] / x[1]) * 100, 
                    zip(swap_used_data, total_swap_data)
                ))