from utils import *

DT = 0.01
MDOT = 1.0

FUEL_TANK = {
    "V_total": gal_to_m3(10),
    "initial_P": psi_to_pa(600),
    "initial_T": f_to_k(70),
    "fill_level": 0.8,
    "gamma": 1.4,
}

OX_TANK = {
    "V_total": gal_to_m3(15),
    "initial_P": psi_to_pa(600),
    "initial_T": f_to_k(70),
    "fill_level": 0.8,
    "gamma": 1.4,
}

ENGINE = {
    "Pc": psi_to_pa(300),
}

COMBUSTOR = {
    "Isp_max": 250,
    "OF_optimal": 1.3,
    "Isp_dropoff": 0.05,
    "cstar_max": 1500,
    "cstar_dropoff": 0.05,
}


RHO_FUEL = 800.0
RHO_OX = 1140.0