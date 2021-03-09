# the main script, mainly to test and developp the package


import numpy as np
import matplotlib.pyplot as plt
from pythermica import  Thermica

path = "./ionsat_deployed_ver3.1/ionsat_deployed_3.1_ionsat_deployed_3.1/"

therm_results = Thermica(path)

time_temperature = therm_results.return_time_temperature()
temperatures = therm_results.read_temperature("Results", "Thermal", "Temperatures" )

fg, axarr = plt.subplots(4,6, figsize=(8,3))


for ax, node_label, nodes_list_for_label in zip(axarr.flatten(), therm_results.names_unique, therm_results.nodes_per_names):
    if node_label == "Space Node":
        pass
    else:
        index_nodes_chassis = []
        for i, node in enumerate(therm_results.nodes_value):
            if node in nodes_list_for_label:
                index_nodes_chassis.append(i)

        index_nodes_chassis = np.array(index_nodes_chassis)


        ax.plot(time_temperature, temperatures.T[:, index_nodes_chassis])
        ax.set_title(node_label)
        #ax.set_xlabel("time [?]")
        #ax.set_ylabel("Temperature [°C]")
        ax.grid(c="grey")

#plt.tight_layout()

#plt.savefig("test_node_labels.png", dpi=300)
plt.show()
