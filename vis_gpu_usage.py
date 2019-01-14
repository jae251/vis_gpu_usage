import subprocess
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import click
import sys
import os
from time import time

if sys.version_info[0] != 3:
    print("Python 3 is required")
    quit()


def get_gpu_usage(nr_devices):
    usages = []
    for device in range(nr_devices):
        s = subprocess.check_output(["nvidia-smi", "--id={}".format(device)])
        s = s.decode("utf-8").split(os.linesep, 8)[8].split()[12]
        usage = int(s[:-1])
        usages.append(usage)
    return usages


def find_gpu_devices():
    s = subprocess.check_output(["nvidia-smi", "-L"])
    s = s.decode("utf-8").split(os.linesep)
    s = list(filter(None, s))
    devices = [substr.split(" (")[0] for substr in s]
    return devices


class GPUVisualizer:
    def __init__(self, interval=.5, maxlen=100):  # interval in seconds
        self.interval = interval
        self.fig = plt.figure()

        self.devices = find_gpu_devices()
        self.nr_devices = len(self.devices)

        if self.nr_devices == 1:
            def set_axes(self):
                ax = self.axes[0]
                ax.set_xlabel("Time in seconds")
                ax.set_ylabel("GPU usage in %")

            self.set_axes = set_axes
        else:
            ax_ = self.fig.add_subplot(1, 1, 1)
            ax_.set_xlabel("Time in seconds")
            ax_.set_ylabel("GPU usage in %")
            ax_.spines['top'].set_color('none')
            ax_.spines['bottom'].set_color('none')
            ax_.spines['left'].set_color('none')
            ax_.spines['right'].set_color('none')
            ax_.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
            self.set_axes = None

        self.axes = []
        self.usage_data = []
        self.time_series = deque(maxlen=maxlen)
        for n, device in enumerate(self.devices):
            self.axes.append(self.fig.add_subplot(self.nr_devices, 1, n + 1))
            self.usage_data.append(deque(maxlen=maxlen))

    @staticmethod
    def update_graph(_, self):
        usage = get_gpu_usage(self.nr_devices)
        self.time_series.append(time() - self.start_time)

        for n, ax in enumerate(self.axes):
            self.usage_data[n].append(usage[n])
            ax.clear()
            ax.set_ylim(0, 100)
            ax.set_title(self.devices[n])
            ax.plot(self.time_series, self.usage_data[n])

        self.set_axes(self)
        self.fig.tight_layout()

    def start(self):
        self.start_time = time()
        ani = FuncAnimation(self.fig, self.update_graph, fargs=[self], interval=self.interval * 1000)
        plt.show()


@click.command()
def cli():
    GPUVisualizer().start()


if __name__ == "__main__":
    GPUVisualizer().start()
