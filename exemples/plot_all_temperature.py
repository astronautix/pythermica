# -*- coding: utf-8 -*-
# @Author: Antoine Tavant
# @Date:   2022-01-21 13:21:37
# @Last Modified by:   Antoine Tavant
# @Last Modified time: 2022-01-26 14:42:52
# the main script, mainly to test and developp the package


import numpy as np
import matplotlib.pyplot as plt
from pythermica import  Thermica


def main():
        
    path = "./simulation_1/results_1/"

    therm_results = Thermica(path)

    time_temperature = therm_results.return_time_temperature()
    temperatures = therm_results.get_temperature( )

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
    
if __name__== "__main__":
    main()
