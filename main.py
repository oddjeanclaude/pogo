from components import *
from utils import *
import config

fuel_tank = BlowdownTank(name="fuel_tank", **config.FUEL_TANK)
ox_tank = BlowdownTank(name="ox_tank", **config.OX_TANK)
fuel_orifice = Orifice(name="fuel_orifice", Cd=0.8, A=1e-4)
ox_orifice = Orifice(name="ox_orifice", Cd=0.8, A=1e-4)
combustor = Combustor(**config.COMBUSTOR)
engine = Engine(name="engine", combustor=combustor, **config.ENGINE)

print(
    f"{'Time':>6} {'F_P (psi)':>10} {'O_P (psi)':>10} {'mdot_f':>8} {'mdot_ox':>8} {'Thrust (lbf)':>13}"
)
print("-" * 62)

for step in range(10):
    t = step * config.DT

    # Orifices compute mdot from tank pressure driving into chamber pressure
    mdot_fuel = fuel_orifice.mdot(fuel_tank.P, engine.Pc, config.RHO_FUEL)
    mdot_ox = ox_orifice.mdot(ox_tank.P, engine.Pc, config.RHO_OX)

    # Engine produces thrust from those flow rates
    engine.update(mdot_fuel, mdot_ox)

    # Tanks drain at those flow rates
    fuel_tank.update(mdot_fuel, config.DT, config.RHO_FUEL)
    ox_tank.update(mdot_ox, config.DT, config.RHO_OX)

    print(
        f"{t:>6.3f} {pa_to_psi(fuel_tank.P):>10.2f} {pa_to_psi(ox_tank.P):>10.2f} {mdot_fuel:>8.4f} {mdot_ox:>8.4f} {n_to_lbf(engine.thrust):>13.2f}"
    )
