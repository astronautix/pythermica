# -*- coding: utf-8 -*-
# @Author: Antoine Tavant
# @Date:   2022-01-27 15:03:53
# @Last Modified by:   Antoine Tavant
# @Last Modified time: 2022-01-27 15:08:22


import pytest

import pythermica
from pythermica import plot_betaangle, plot_eclipses, plot_misalignment

filename = pythermica.__path__[0]+"/../exemples/simulation_1/results_1/ionsat_deployed_3.0.html"
output_path = pythermica.__path__[0] +"/../exemples/"

def test_plot_betaangle():
    
    plot_betaangle(filename=filename, output_path=output_path)


def test_plot_eclipses():

    plot_eclipses(filename=filename, output_path=output_path)


def test_plot_misalignment():

    plot_misalignment(filename=filename, output_path=output_path)
