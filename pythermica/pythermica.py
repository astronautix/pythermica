"""Main module."""

import numpy as np
import h5py as hp
import os, sys, glob

import datetime

class Thermica():
    """Main class to analyse the simulation results"""

    def __init__(self, path):
        """Init the class"""
        self.path = path  #: path were the simulation results are stored
        self.names_unique = []  #: list of the names used to label the nodes
        self.nodes_per_names = [[]]  #: list of the lists of the nodes for each unique names
        self.nodes_value = np.array([])  #: list of the node value, order in the same way as the temperatures

        print("Initializing Thermica at path :")
        print(path)
        print("Files present in the path :")
        [ print(n) for n in glob.glob(self.path+"/*.h5", )]

        try:
            self.process_model_nodes()
        except:
            raise RuntimeWarning("Cannot process the nodes. Maybe the temperature file is not present.")

    def get_filename(self, type="none"):
        """general fonction to get the filename depending of the type of results wanted"""

        if type == "solarflux":
            extention = "*.sf.h5"
        elif type == "earthflux":
            extention = "*.pf.h5"
        elif type == "temperature":
            extention = "*.temp.h5"


        return glob.glob(self.path + extention)

    def get_solarflux_file(self):
        """return the h5 file name with the solar flux"""

        filename = self.get_filename("solarflux")
        print(filename)
        if len(filename) != 1:
            raise RuntimeError("Error with the Solaf Flux files")

        filename = filename[0]

        return filename

    def get_temperature_file(self):
        """return the h5 file name with the solar flux"""

        filename = self.get_filename("temperature")
        #print("the filename is :")
        #print(filename)
        if len(filename) == 0:
            raise RuntimeError("Error with the temperature files")
        elif len(filename) > 1:
          print("WARNING !!!  Too many temperature files ! \n We will use the first one in the list")

        filename = filename[0]

        return filename

    def dump_result_file_structure(self):
        """print the file data structure"""
        from .hdf5_process import h5dump
        fname = self.get_temperature_file()
        h5dump(fname)

    def read_solarflux(self, groupname, datasetname ):
        solarfluxname = self.get_solarflux_file()

        with hp.File(solarfluxname, "r") as h5file:
            value = h5file[groupname][datasetname][()]

        return value

    def read_groupe_subgroup(self, filename, groupname, subgroup, datasetname ):


        with hp.File(filename, "r") as h5file:
            value = h5file[groupname][subgroup][datasetname][()]

        return value

    def get_temperature(self):
        fname = self.get_temperature_file()

        return self.read_groupe_subgroup( filename=fname, groupname="Results", subgroup="Thermal", datasetname="Temperatures" )

    def read_temperature2(self, groupname, datasetname ):
        """Open the temperature h5 file, but access the dataset with only one groupe of hyerachi"""
        solarfluxname = self.get_temperature_file()

        with hp.File(solarfluxname, "r") as h5file:
            value = h5file[groupname][datasetname][()]

        return value

    def return_time_temperature(self):
        """the time vector is stor in all of the h5 files, in Hours from the start of the simulation"""

        solarfluxname = self.get_temperature_file()

        with hp.File(solarfluxname, "r") as h5file:
            value = h5file["Time"]["Frequency 1"][()]
        value -= value[0]
        value *= 24
        return value

    def return_datetime_temperature(self):
        """return the time array as datetime objects"""
        time = self.return_time_temperature()

        return
    def process_model_nodes(self):
        """The nodes are accessible, but this model is meat to understand better their information
        """

        try :
            node_liste = self.read_temperature2("Model", "Nodes")
        except OSError :
            raise RuntimeError("Cannot open the file. You should close any application using the file")

        self.node_liste = np.array([n[1] for n in node_liste])

        names = [ d[2] for d in node_liste]
        self.nodes_value = np.array([d[1] for d in node_liste])

        names_unique = []
        for n in names:
            name_in_str = n.decode("utf-8")
            if not name_in_str  in names_unique:
                if len(name_in_str) > 0:
                    names_unique.append(n.decode("utf-8") )

        self.names_unique = np.array(names_unique)

        nodes_per_names = [[] for n in self.names_unique]

        for i, n in enumerate(self.names_unique):
            for b in node_liste:
                if b[2].decode("utf-8") == n:
                    nodes_per_names[i].append(b[1])
        self.nodes_per_names = nodes_per_names

        print("We have some names :")
        for name in self.names_unique:
            print(name)
        print()
        for i, n in enumerate(self.names_unique):
            print(len(self.nodes_per_names[i]), "nodes in ", n, " starting at", self.nodes_per_names[i][0])

