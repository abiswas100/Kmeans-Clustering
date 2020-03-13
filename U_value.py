import os
import csv
import numpy as np
import statistics as stats
import json
import re
'''
Section for functions that are responsible for converting variables from one set of
units to another.
'''
def convert_to_kelvin(temperature):
    '''
    Function takes in a celsius temperature value and returns the kelvin equivilant.
    :param temperature: Temperature in celsius
    :return: Temperature in Kelvin
    '''
    return temperature + 273.15

def convert_to_mps(wind_speed):
    '''
    Function takes in wind speed in mph and converts to m/s
    :param wind_speed: Windspeed in MPH
    :return: Windspeed in m/s
    '''
    return wind_speed * .44704




'''
Function responsible for u-value calcualtions. One function is now responsible for calculating
all u-values. (The parameters for each u-value calculation are quite similar)
'''
def u_value_calculation(pixel_temperature):

    #Setting up variables that will be used throughout equations
    Ev = 1.00 # emissivity (based on material of object)
    sigma = 5.67 * (10 ** -8) #constant 
    Tw = convert_to_kelvin(pixel_temperature) #wall temperature (from the csv)
    Tout = convert_to_kelvin(7.1) #needs to be fetched from some source (webscraping)
    v = convert_to_mps(22) #converts windspeed in m/h to m/s
    Tin = convert_to_kelvin(20) #inside temperature of the building (should be from thermocouple)
 
    #Extra variables for u_value_2-4
    L = 12.192 #height of building in meters (this is twamleys height)
    Ac = 1.365 * ((((abs(Tw - Tout)) / L)) ** (1/4))

    #Extra variable for u_value_4
    Tm = (Tw + Tout) / 2

    #u_value_1 calcualtion
    numerator_u1 = Ev * (sigma * (((Tw) ** 4) - ((Tout) ** 4))) + 3.8054 * (v * (Tw - Tout))
    denominator_u1 = Tin - Tout
    try:
        u_value_1 = numerator_u1 / denominator_u1
    except ZeroDivisionError:
        print("ERROR: Inside temperature: {} and Outside temperature: {} are the same. Cannot divide by 0. Skipping data point.".format(Tin, Tout))

    #u_value_2 calculation
    numerator_u2 = (4 * Ev * (sigma * (((Tw) ** 4) - ((Tout) ** 4))) + Ac * (Tw - Tout))
    denominator_u2 = (Tin - Tout)
    try:
        u_value_2 = numerator_u2 / denominator_u2
    except:
        print("ERROR: Inside temperature: {} and Outside temperature: {} are the same. Cannot divide by 0. Skipping data point.".format(Tw, Tout))


    #u_value_3 calculation
    numerator_u3 = (4 * Ev * (sigma * ((Tw) ** 3) * ((Tw) - (Tout))) + Ac * (Tw - Tout))
    denominator_u3 = (Tin - Tout)
    try:
        u_value_3 = numerator_u3 / denominator_u3
    except ZeroDivisionError:
        print("ERROR: Inside temperature: {} and Outside temperature: {} are the same. Cannot divide by 0. Skipping data point.".format(Tw, Tout))

    #u_value_4 calculation
    numerator_u4 = (4 * Ev * sigma * ((Tm) ** 3) * ((Tw) - (Tout)) + Ac * (Tw - Tout))
    denominator_u4 = (Tin - Tout)
    try:
        u_value_4 = numerator_u4 / denominator_u4
    except ZeroDivisionError:
        print("ERROR: Inside temperature: {} and Outside temperature: {} are the same. Cannot divide by 0. Skipping data point.".format(Tw, Tout))

    return u_value_1, u_value_2, u_value_3, u_value_4
