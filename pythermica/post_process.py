# -*- coding: utf-8 -*-
# @Author: Antoine Tavant
# @Date:   2022-01-26 14:31:18
# @Last Modified by:   Antoine Tavant
# @Last Modified time: 2022-01-27 19:20:07

from .thermal_results import Thermica
from .analyse_nwk import *
from .plot_variables import *
from pathlib import Path, PosixPath, WindowsPath

def process_nwk_and_temperature( path_results,
                                output_dir=None,
                                nodes_names_to_discard=[],
                                verbose=False):
    
    """analyse everythin needed for one simulation"""

    if type(path_results) in [PosixPath, WindowsPath]:
        path_results = path_results  #: path were the simulation results are stored
    elif type(path_results) is str:
        #: path were the simulation results are stored
        path_results = Path(path_results)
    else:
        raise RuntimeError("path Not with rigth Type")
    
    if output_dir is None:
        output_dir = path_results
    
    """First the NWK data"""
    if verbose:
        print("Sarting with analysing the NWK coefs")
        
    filename_gb, filename_nod, filename_gr, filename_gl = get_useful_files(
        path_results)

    list_of_nodes_numbers, list_of_nodes_names = extract_nodes(filename_nod)
    
    list_node_names_to_process = []
    list_node_numbers_to_process = []
    
    assert len(list_of_nodes_names) == len(list_of_nodes_numbers)
    
    for num, name in zip(list_of_nodes_numbers, list_of_nodes_names):
        if not name in nodes_names_to_discard and not name in list_node_names_to_process:
            list_node_names_to_process.append(name)
            list_node_numbers_to_process.append(num)

    
    """Analysing the Gebhart Factor"""
    if verbose:
        print("Analysing the GB factors")
    list_nodes_numbers_bg, index_lines_with_new_node, lines_with_new_node = read_gb_file(
        filename_gb,)

    """Is ther any missing factor ?"""
    if verbose:
        print("missing Gebhart Factor entry for nodes : ")

        for idx, n in enumerate(list_node_numbers_to_process):
            if n not in list_nodes_numbers_bg:
                print(n, ":", list_node_names_to_process[idx])
        
        print("")
        
    """ generating the GB matrix figure"""
    if verbose:
        print("Generating the BG matrix")
    mat_gb_vf, mat_gb_ir = get_all_dict_of_gb_lines(
        filename_gb,
        list_node_numbers_to_process,
        index_lines_with_new_node,
        lines_with_new_node)

    print("Generating Correlation Matrix for BG factors")
    fig, axarr = generate_correlation_matrixes(list_mats=[mat_gb_ir, mat_gb_vf],
                                               list_node_names=list_node_names_to_process,
                                               list_titles=[
        "Gebhart factor IR", "Gebhart factor VF"],
        use_log=False,
        save_fig=True,
        filename=output_dir / "matrices_Gebhart_factors_values.png",
        cmap="Blues")
    
    """ generating the GR matrix figure"""
    mat_GR = analyse_GR_nwk_data(
        filename_gr,
        list_node_numbers_to_process,
        list_node_names_to_process)
    
    print("Generating Correlation Matrix for GR coefs")

    fig, axarr = generate_correlation_matrixes(list_mats=[mat_GR],
                                               list_node_names=list_node_names_to_process,
                                               list_titles=[
                                                   "Radiative couplings (IR) computed by Thermica"],
                                               use_log=True,
                                               save_fig=True,
                                               filename=output_dir / "matrices_IR_GR_factors_values.png"
                                               )
    
    mat_GL = analyse_GL_nwk_data(
        filename_gl,
        list_node_numbers_to_process,
        list_node_names_to_process)

    fig, axarr = generate_correlation_matrixes([mat_GL],
                                               list_node_names_to_process,
                                               ["conductives couplings computed by Thermica"],
                                               use_log=True,
                                               save_fig=True,
                                               filename=output_dir / "matrices_GL_factors_values.png"
                                               )
    
    """Second, the thermal data"""
    
    thermal_result = Thermica(path_results, verbose=False)
    
    time_temperature = thermal_result.return_time_temperature()
    temperatures = thermal_result.get_temperature()

    fig, axarr = plt.subplots(4, 6, figsize=(10, 5))

    for ax, node_label, nodes_list_for_label in zip(axarr.flatten(),
                                                    thermal_result.names_unique,
                                                    thermal_result.nodes_per_names):
        if not node_label in nodes_names_to_discard:
            index_nodes_chassis = []
            for i, node in enumerate(thermal_result.nodes_value):
                if node in nodes_list_for_label:
                    index_nodes_chassis.append(i)

            index_nodes_chassis = np.array(index_nodes_chassis)

            ax.plot(time_temperature, temperatures.T[:, index_nodes_chassis])
            ax.set_title(node_label)
            ax.grid(c="grey")

    plt.savefig(output_dir / "all_node_temp.png", dpi=300)
    
    
    if verbose:
        print("ploting figures for temperature")
        print("for nodes : ")
        print(list_node_names_to_process)
        
    figure_over_nodes(therm_results=[thermal_result],
                      temperatures=[temperatures],
                      times=[time_temperature],
                      n_orbits=8,
                      path_list=[path_results],
                      case_names=[""],
                      nodes_to_process=list_node_names_to_process,
                      path_root=output_dir,
                      name_yaxis="Temperature",
                      filename_prefix="")
    
    internal_dissipations = thermal_result.get_internal_dissipation()
    
    figure_over_nodes(therm_results=[thermal_result],
                      temperatures=[internal_dissipations],
                      times=[time_temperature],
                      n_orbits=8,
                      path_list=[path_results],
                      case_names=[""],
                      nodes_to_process=list_node_names_to_process,
                      path_root=output_dir,
                      name_yaxis="Internal Dissipation [W]",
                      filename_prefix="IQ_")
    
    totalInternalDissipation([thermal_result],
                             [internal_dissipations],
                             [time_temperature],
                             n_orbits = 8,
                             path_list = [path_results],
                             case_names = [""],
                             nodes_to_process=list_node_names_to_process,
                             path_root=output_dir,
                             filename_prefix="Total_IQ")



    


