#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:34:49 2020

@author: amelielaurens

Source : A simple model for nanofiber formation by rotary jet-spinning
by mellado et al.

Goal : Prediction of the final radius for various polymer density.

Select the machine and the polymer for which we want to run the code.

Inputs : Concerning the polymer : the surface tension, the viscosity
         Concerning the machine : the reservoir radius, the collector radius,
                                  the orifice radius,
                                  the angular viscosity of the spinneret.

All data are in SI units.
"""

from deck import Deck
from machine import RJSMachine
from polymer import Polymer
from modelling import RJSModel
import numpy
import matplotlib.pyplot as plt

deck = Deck("deck.yaml")
machine = RJSMachine(deck)
polymer = Polymer(deck)
model = RJSModel(polymer, machine)

# Reach machine parameters
name_machine = machine.name
s0 = machine.reservoir_radius
Rc = machine.collector_radius
omega = machine.omega
orifice_radius = machine.orifice_radius

# Reach polymer parameters
name_polymer = polymer.name
mu = polymer.viscosity
surface_tension = polymer.surface_tension

discretisation = int(deck.doc['Discretisation'])
# The higher the discretisation number is, the finer the discretisation will be,
# there will be more points on the graphic.

rho = numpy.linspace(900, 1500, discretisation)

omega_th = []
initial_velocity = []
nu = []
for l in range(discretisation):
    omega_th.append(model.critical_rotational_velocity_threshold(surface_tension, orifice_radius,
                                                           s0, rho[l]))
    initial_velocity.append(model.Initial_velocity(omega_th[l], s0))
    nu.append(model.kinematic_viscosity(mu, rho[l]))
omega_th = numpy.array(omega_th)
initial_velocity = numpy.array(initial_velocity)
nu = numpy.array(nu)

Final_radius = []
for k in range(discretisation):
    Final_radius.append(model.final_radius(orifice_radius, initial_velocity[k], nu[k], Rc, omega))
Final_radius = numpy.array(Final_radius)

fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)
axes.plot(rho, Final_radius, 'ro')
axes.grid()
axes.set_xlabel("Density (kg/m^3)", fontsize=16)
axes.set_ylabel("Final radius (m)", fontsize=16)
axes.set_title(" %s / %s " % (name_machine, name_polymer), fontsize=16, y=1.)

# Plot a zoomed graphic on the small radius below 0.00002 m
fig2 = plt.figure()
axes = fig2.add_subplot(1, 1, 1)

for i in range(discretisation):
    if Final_radius[i] <= 0.00002:
        axes.plot(rho[i], Final_radius[i], 'bo')
axes.grid()
axes.set_xlabel("Density (kg/m^3)", fontsize=16)
axes.set_ylabel("Final radius  (m)", fontsize=16)
axes.set_title("ZOOM %s / %s " % (name_machine, name_polymer), fontsize=16, y=1.05)

plt.show()