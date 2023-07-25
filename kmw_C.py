import kmw_main as im

class dp:
    def __init__(self, _rti):
        self.rti = _rti
        self.rt = []
        self.sn = []
    def enscribe(self, _rt, _sn):
        self.rt.append(_rt)
        self.sn.append(_sn)

def scrape_rt(sample_array, rt_set):
    for sample in sample_array:
        rt_set.add(sample.rt)

def compile_hs(rt_set, fin_dict):
    rt_set = sorted(rt_set)
    print(rt_set)
    slow = 0
    fast = 1
    arr = []
    arr.append(rt_set[slow])
    while slow != fast and fast != len(rt_set):
        current_rt = rt_set[slow]
        fast_rt = rt_set[fast]
        if(fast_rt < (current_rt + 0.1)):
            arr.append(rt_set[fast])
            fast += 1
        else:
            fin_dict[rt_set[slow]] = arr
            slow += 1
            arr = []
            arr.append(rt_set[slow])
            fast = slow + 1
    
    print(fin_dict)

            


def kmw_C(sample_array):
    rt_set = set()
    scrape_rt(sample_array, rt_set)
    fin_dict = {}
    compile_hs(list(rt_set), fin_dict)

        
