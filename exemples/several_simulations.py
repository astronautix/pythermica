# the main script, mainly to test and develop the package

import numpy as np
import matplotlib.pyplot as plt
from pythermica import Thermica

plot_style = {
    "axes.grid": True,
    "axes.grid.axis": 'y',
    "axes.labelsize": 12,
    "axes.titlesize": 16,
    "figure.autolayout": True,
    "figure.dpi": 300,
    "figure.figsize": [6.4, 4.8],
    "font.family": "STIXGeneral",
    "grid.alpha": 0.5,
    "grid.color": "grey",
    "grid.linestyle": "dotted",
    "grid.linewidth": 0.8,
    "image.aspect": "auto",
    "image.cmap": "plasma",
    "image.interpolation": "nearest",
    "image.origin": "lower",
    "lines.linewidth": 1,
    "lines.markersize": 5,
    "mathtext.fontset": "stix",
    "savefig.format": "eps",
    "xtick.labelsize": 10,
    "xtick.minor.visible": True,
    "xtick.top": True,
    "ytick.labelsize": 10,
    "ytick.minor.visible": True,
    "ytick.right": True
}

plt.rcParams.update(plot_style)
path = ["./simulation_1/results_1/", "./simulation_1/results_2/"]
case_names = ["Hot case",
              "Typical case",
              ]
n_path = len(case_names)
n_orbits: int = 8
therm_results = []
temperatures = []
time = []
for i in range(n_path):
    therm_results.append(Thermica(path[i]))
    temperatures.append(therm_results[i].read_temperature("Results", "Thermal", "Temperatures"))
    time.append(therm_results[i].return_time_temperature())
period = time[0][-1] / n_orbits

list_of_labels_to_plot = ["/Chassis top", "/Transponder (1)", "/Batteries"]

for node_label, nodes_list_for_label in zip(therm_results[0].names_unique, therm_results[0].nodes_per_names):
    if node_label in list_of_labels_to_plot:
        index_nodes = []
        for i, node in enumerate(therm_results[0].nodes_value):
            if node in nodes_list_for_label:
                index_nodes.append(i)
        index_nodes = np.array(index_nodes)  # index of nodes corresponding to label
        temperatures_node_average = []  # n_path lists of node-averaged temperature corresponding to n_path cases
        temperature_max = []  # maximum temperatures corresponding to n_path cases
        temperature_min = []  # minimum temperatures corresponding to n_path cases
        temperature_time_average = []  # time-averaged temperatures corresponding to n_path cases
        for i in range(n_path):
            _max_temp = []
            _min_temp = []
            _average_temp = []
            for _temp in temperatures[i].T[:, index_nodes]:
                _max_temp.append(max(_temp))
                _min_temp.append(min(_temp))
                _average_temp.append(np.mean(_temp))
            temperatures_node_average.append(_average_temp)
            temperature_max.append(int(max(_max_temp)))
            temperature_min.append(int(min(_min_temp)))
            temperature_time_average.append(int(np.mean(_average_temp)))
        plt.figure()
        for i in range(n_path):
            plt.plot(time[i], temperatures_node_average[i],
                     label=case_names[i] + ' (max=' + str(temperature_max[i]) + ', min=' +
                           str(temperature_min[i]) + ', average=' +
                           str(temperature_time_average[i]) + ')')
        plt.vlines([period*k for k in range(1, n_orbits+1)], max(temperature_max), min(temperature_min), linestyles="--")
        plt.title(node_label[1:])
        plt.xlabel('Time (hr)')
        plt.ylabel('Temperature (Celsius)')
        plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15))
        plt.savefig(node_label[1:] + '.png')
