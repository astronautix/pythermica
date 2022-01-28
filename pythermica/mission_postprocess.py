# -*- coding: utf-8 -*-
# @Author: Antoine Tavant
# @Date:   2022-01-27 14:41:23
# @Last Modified by:   Antoine Tavant
# @Last Modified time: 2022-01-27 16:34:03


from .plot_variables import plot_style
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
import numpy as np

plt.rcParams.update(plot_style)

def parse_misson_report(repport_filename, wanted_data_list=["Beta Angle (°)",
                                                            "Sun constant (W/m2)", "Eclipse/Penumbra", ]):
    """
    parse the HTML repport to get the imteresting data on the mission.

    Args:
        repport_filename (str): filename of the html mission repport
        wanted_data_list (list[str]): list of data to extract, from the available : ["Beta Angle (°)", "Elapsed Time in sec (sec)",
                   "Sun constant (W/m2)", "Eclipse/Penumbra", "Misalignment"]

    Returns:
        datasets (dict): dict of the different data
    """
    
    with open(repport_filename, "r") as file:
        soup = BeautifulSoup(file.read(), features="html.parser")

    # Get all the column names of the Main table

    table = soup.find("table", attrs={"id": "mainTable"})
    headings = [td.get_text() for td in table.find("thead").find_all("td")]

    # `wanted_data_list` is the list of the column name that we want to extract
    assert type(wanted_data_list) == list, "The argument `wanted_data_list` should be a list"
    
    header_time = "Elapsed Time in sec (sec)"
    if not header_time in wanted_data_list:
        wanted_data_list.append(header_time)
        

    if "Misalignment" in wanted_data_list:
        wanted_data_list.remove("Misalignment")
        for head in headings:
            if "Misalignment" in head:
                wanted_data_list.append(head)

    # Find the index of the column for each wanted data
    indexes = [headings.index(w) for w in wanted_data_list]

    # Extract all the Data !!
    datasets = {h: [] for h in wanted_data_list}

    for table_row in table.find("tbody").find_all("tr"):

        row_data = [td.get_text() for td in table_row.find_all("td")]

        for index, key in zip(indexes, wanted_data_list):
            datasets[key].append(row_data[index])

    # Translate the text in numbers exect for the Eclipse dataset

    for k in wanted_data_list:
        if k != "Eclipse/Penumbra":
            datasets[k] = np.array([float(d) for d in datasets[k]])

    return datasets, wanted_data_list


def get_beta_angle(filename):
    
    datasets, wanted_data_list = parse_misson_report(
        filename, ["Beta Angle (°)"])
    
    return datasets
    

def get_eclipse(filename):

    datasets, wanted_data_list = parse_misson_report(
        filename, ["Eclipse/Penumbra", "Sun constant (W/m2)"])

    return datasets


def get_misalignment(filename):

    datasets, wanted_data_list = parse_misson_report(
        filename, ["Misalignment"])

    return datasets, wanted_data_list

    
def plot_eclipses(filename, output_path='./', savefig=False):
    
    datasets = get_eclipse(filename)
    time_hours = datasets["Elapsed Time in sec (sec)"]/3600
    eclipse_bool = np.array([d == "Light" for d in datasets["Eclipse/Penumbra"]])
    
    plt.figure(figsize=(4, 4))

    plt.plot(time_hours, eclipse_bool*datasets["Sun constant (W/m2)"])
    plt.xlabel("Time (h)")
    plt.ylabel("Sun Flux to the Satellite (W/m²)")

    plt.tight_layout()
    a=45
    winting=6.35
    if savefig:
        plt.savefig(output_path+"/Sun_flux_on_satellite.png", dpi=200)



def plot_betaangle(filename, output_path='./', savefig=False):

    datasets = get_beta_angle(filename)
    time_hours = datasets["Elapsed Time in sec (sec)"]/3600
    
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))
    ax.plot(time_hours, datasets["Beta Angle (°)"])
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Beta Angle (°)")
    ax.set_title("Evolution of the Beta angle during the mission")
    fig.tight_layout()
    if savefig:
        plt.pause(0.1)
        fig.savefig(output_path + "/beta_angle.png",
                    dpi=200, bbox_inches="tight")

    return fig, ax


def plot_misalignment(filename, output_path="./", savefig=False):
    
    datasets, wanted_data_list = get_misalignment(filename)
    time_hours = datasets["Elapsed Time in sec (sec)"]/3600
    
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))

    for key in wanted_data_list:
        if key != "Elapsed Time in sec (sec)":
            ax.plot(time_hours, datasets[key], label=key)
            
    ax.set_xlabel("Time (h)", fontsize=10)
    ax.set_ylabel("misalignment [°]", fontsize=10)
    ax.set_title("Misalignment of the Kinematic law as function of time")
    
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15))


    fig.tight_layout(rect=[0.1, 0.1, 0.9, 0.95])
    if savefig:
        fig.savefig(output_path + "/misselignment.png",
                    dpi=200, bbox_inches="tight")


    return fig, ax
