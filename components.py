class BlowdownTank:
    """Single polytropic spring model for gaseous blowdown"""

    def __init__(self, name, V_total, initial_T, initial_P, fill_level, gamma=1.4):
        self.name = name
        self.V_total = V_total  # total tank volume (m^3)
        self.P = initial_P  # current pressure (Pa)
        self.T = initial_T  # current temperature (K)
        self.gamma = gamma

        # Initial volumes based on fill percentage
        self.V_liquid = V_total * fill_level  # Liquid volume (m^3)
        self.V_ullage = V_total * (1 - fill_level)  # Ullage volume (m^3)
        self.V_ullage_0 = self.V_ullage  # Initial ullage volume (m^3)
        self.P_0 = initial_P  # Initial pressure (Pa)
        self.T_0 = initial_T  # Initial temperature (K)

    def update(self, mdot, dt, rho_fuel):
        """Update tank pressure based on mass removed"""
        if self.V_liquid <= 0:
            self.V_liquid = 0.0
            self.V_ullage = self.V_total  # ullage is the whole tank
            return  # tank is empty, no further state change

        # Remove fuel mass from tank
        dV = mdot * dt / rho_fuel
        self.V_liquid = max(self.V_liquid - dV, 0.0)

        # Update ullage volume based on new liquid volume
        self.V_ullage = self.V_total - self.V_liquid

        # Update pressure and temperature using polytropic relation
        ratio = self.V_ullage_0 / self.V_ullage
        self.P = self.P_0 * ratio**self.gamma
        self.T = self.T_0 * ratio ** (self.gamma - 1)


class Engine:
    """Simple thrust model based on fuel and ox flow rates"""

    def __init__(self, name, Pc, combustor):
        self.name = name
        self.thrust = 0.0  # Current thrust (N)
        self.mdot_fuel = 0.0
        self.mdot_ox = 0.0
        self.Pc = Pc
        self.combustor = combustor

    def update(self, mdot_fuel, mdot_ox):
        """Update engine state based on fuel and ox flow rates"""
        self.combustor.update(mdot_fuel, mdot_ox)
        mdot_total = mdot_fuel + mdot_ox
        self.thrust = mdot_total * self.combustor.Isp * 9.81  # F = m_dot * Isp * g0

class Orifice:
    """Computes mass flow rate from pressure differennital"""

    def __init__(self, name, Cd, A):
        self.name = name
        self.Cd = Cd  # Discharge coefficient (~0.6-0.8)
        self.A = A  # Orifice area (m^2)

    def mdot(self, P_upstream, P_downstream, rho):
        """Calculate mass flow rate through orifice"""
        dP = P_upstream - P_downstream

        if dP <= 0:
            return 0.0  # No flow if dP <= 0
        return self.Cd * self.A * (2 * rho * dP) ** 0.5

class Combustor:
    """Handles combustion thermochemistry"""
    def __init__(self, Isp_max, OF_optimal, Isp_dropoff, cstar_max, cstar_dropoff):
        self.Isp_max = Isp_max
        self.OF_optimal = OF_optimal
        self.Isp_dropoff = Isp_dropoff
        self.OF_ratio = 0.0
        self.Isp = 0.0
        self.mdot_fuel = 0.0
        self.mdot_ox = 0.0
        self.cstar_max = cstar_max
        self.cstar_dropoff = cstar_dropoff

    def update(self, mdot_fuel, mdot_ox):
        self.mdot_fuel = mdot_fuel
        self.mdot_ox = mdot_ox
        self.OF_ratio = mdot_ox / mdot_fuel if mdot_fuel > 0 else 0.0
        self.Isp = self._compute_Isp()
        self.cstar = self._compute_cstar()  

    def _compute_Isp(self):
        # Simple parabolic dropoff around optimal OF ratio
        if self.OF_ratio <= 0:
            return 0.0
        else:
            isp = self.Isp_max * (1 - self.Isp_dropoff * (self.OF_ratio - self.OF_optimal) ** 2)
            return max(isp, 0.0)
        
    def _compute_cstar(self):
        if self.OF_ratio <= 0:
            return 0.0
        else:
            cstar = self.cstar_max * (1 - self.cstar_dropoff * (self.OF_ratio - self.OF_optimal) ** 2)
            return max(cstar, 0.0)

