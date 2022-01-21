# -*- coding: utf-8 -*-
# @Author: Antoine Tavant
# @Date:   2021-12-17 16:22:30
# @Last Modified by:   Antoine Tavant
# @Last Modified time: 2022-01-21 13:34:51

import numpy as np
import matplotlib.pyplot as plt
import pythermica
from pythermica.analyse_nwk import (extract_nodes, get_useful_files,
                                        generate_correlation_matrixes,
                                        read_gb_file,
                                        get_all_dict_of_gb_lines,
                                        analyse_GR_nwk_data,
                                        analyse_GL_nwk_data, 
                                        get_nth_max_coupling)

def main():
    """This exemple process the network coefficients of one exemple thermica result."""
    
    root = pythermica.__path__[0]+"/../exemples/model_test/"
    print(root)
    save_file_folder=root
    filename_gb, filename_nod, filename_gr, filename_gl = get_useful_files(root)

    list_of_nodes_numbers, list_of_nodes_names = extract_nodes(filename_nod)
    
    
    # GebHart Factors
    
    list_nodes_numbers_bg, index_lines_with_new_node, lines_with_new_node = read_gb_file(
        filename_gb,)
    
    print("missing entry for nodes : ")


    for idx, n in enumerate(list_of_nodes_numbers):
        if n not in list_nodes_numbers_bg:
            print(n, ":", list_of_nodes_names[idx])
            
    mat_gb_vf, mat_gb_ir = get_all_dict_of_gb_lines(
        filename_gb, list_of_nodes_numbers, index_lines_with_new_node, lines_with_new_node)
            
    fig, axarr = generate_correlation_matrixes(list_mats=[mat_gb_ir, mat_gb_vf],
                                               list_node_names=list_of_nodes_names,
                                               list_titles=[
        "Gebhart factor IR", "Gebhart factor VF"],
        use_log=False,
        save_fig=True,
        filename=save_file_folder+"matrices_Gebhart_factors_values",
        cmap="Blues")

    mat_GR = analyse_GR_nwk_data(
        filename_gr, list_of_nodes_numbers, list_of_nodes_names)
    fig, axarr = generate_correlation_matrixes(list_mats=[mat_GR],
                                               list_node_names=list_of_nodes_names,
                                               list_titles=[
                                                   "Radiative couplings (IR) computed by Thermica"],
                                               use_log=True,
                                               save_fig=True,
                                               filename=save_file_folder+"matrices_IR_GR_factors_values"
                                               )
    
    mat_GL = analyse_GL_nwk_data(
        filename_gl, list_of_nodes_numbers, list_of_nodes_names)

    fig, axarr =  generate_correlation_matrixes( [mat_GL],
                                                list_of_nodes_names,
                                                ["conductives couplings computed by Thermica"],
                                                use_log=True,
                                                save_fig=True,
                                                 filename=save_file_folder+"matrices_GL_factors_values"
    )


if __name__ == "__main__":
    main()
