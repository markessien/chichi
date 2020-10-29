
import subprocess
from dataclasses import dataclass, field
from typing import List

@dataclass
class ChiaStats:
    """Class for keeping track of an item in inventory."""
    netspace: float = 0
    plot_dirs: List[str] = field(default_factory=list)
    loaded_plot_count: int = 0
    loaded_plot_tb: float = 0
    heights: List[int] = field(default_factory=list)
    proof_times: List[float] = field(default_factory=list)
    connected: bool = False

    def avg_proof_time(self):
        total = 0.0
        for proof_time in self.proof_times:
            total = total + proof_time
        return round(total / len(self.proof_times), 2)

def get_netspace():
    res = str(subprocess.check_output(["/home/ubuntu/chia-blockchain/venv/bin/chia netspace -d 48"], shell = True))
    space_start = res.find("estimated ") + 10
    space_end = res.find("TiB")
    netspace = res[space_start : space_end]
    return float(netspace)


def get_chiaplots():
    res = str(subprocess.check_output(["/home/ubuntu/chia-blockchain/venv/bin/chia plots show"], shell = True))
    space_start = res.find("chia plots check")
    plots = res[space_start + 16: ]
    plots = plots.split('\\n')

    final_plots = []
    for plot in plots:
        if plot.find('/') >= 0:
            final_plots.append(plot)

    return final_plots

def get_connected_status(c):
    connected = False
    res = str(subprocess.check_output(["/home/ubuntu/chia-blockchain/venv/bin/chia show -s"], shell = True))
    if res.find("Current Blockchain Status: Full Node Synced") >= 0:
        connected = True

    p0 = res.find("Heights of tips:")
    if p0 >= 0:
        p1 = res.find("]", p0)
        tips = res[p0+18 : p1]

        final_tip_list = []
        tips_list = tips.split(',')
        for t in tips_list:
            final_tip_list.append(int(t))
        c.heights = final_tip_list

    c.conected = connected

def parse_logfile(c):

    print("starting parse")
    with open("/home/ubuntu/.chia/beta-1.0b15/log/debug.log") as fp:
        for cnt, line in enumerate(fp):
            # print(line)
            p = line.find("Loaded a total of ")
            if p >= 0:
                c.loaded_plot_count = line[p + 18 : line.find(' ', p + 19)]
                c.loaded_plot_tb = line[line.find('size ') + 5 : line.find(' TiB')]

            p = line.find("were eligible for farming")
            if p >= 0:
                proof_time = line[line.find('Time: ', p) + 6: line.find('. Total', p)]
                # print("Proof Time: " + proof_time)
                c.proof_times.append(float(proof_time))

                if len(c.proof_times) > 20:
                    c.proof_times.pop(0)

def get_chia_stats():
    c = ChiaStats()
    c.netspace = get_netspace()
    c.plot_dirs = get_chiaplots()

    get_connected_status(c)
    parse_logfile(c)

    return c
