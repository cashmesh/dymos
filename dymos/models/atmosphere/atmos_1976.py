"""
United States standard atmosphere 1976 tables, data
obtained from http://www.digitaldutch.com/atmoscalc/index.htm
"""
from collections import namedtuple

import numpy as np
from scipy.interpolate import Akima1DInterpolator as Akima
from openmdao.components.interp_util.interp import InterpND

import openmdao.api as om


USatm1976Data = namedtuple('USatm1976Data', ['alt', 'temp', 'pres', 'rho', 'a', 'viscosity'])
USatm1976Data.__doc__ = \
    """
    A namedtuple to hold data for the 1976 standard atmosphere model.

    Parameters
    ----------
    alt : float
        Altitude in feet.
    temp : float
        Temperature in degR.
    pres : float
        Pressure in psi.
    rho : float
        Density in slug/ft**3.
    a : float
        Speed of sound in ft/s.
    viscosity : float
        Dynamic viscosity in lbf*s/ft**2.
    """

# units='ft'
USatm1976Data.alt = np.array([-1000, 0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                              11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                              21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000,
                              31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000,
                              41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000,
                              51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000,
                              61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000,
                              71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000,
                              81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000,
                              91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000,
                              105000, 110000, 115000, 120000, 125000, 130000, 135000, 140000,
                              145000, 150000], dtype=float)

# units='degR'
USatm1976Data.T = np.array([522.236, 518.67, 515.104, 511.538, 507.972, 504.405, 500.839, 497.273,
                            493.707, 490.141, 486.575, 483.008, 479.442, 475.876, 472.31, 468.744,
                            465.178, 461.611, 458.045, 454.479, 450.913, 447.347, 443.781, 440.214,
                            436.648, 433.082, 429.516, 425.95, 422.384, 418.818, 415.251, 411.685,
                            408.119, 404.553, 400.987, 397.421, 393.854, 390.288, 389.97, 389.97,
                            389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97,
                            389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97,
                            389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97, 389.97,
                            390.18, 390.729, 391.278, 391.826, 392.375, 392.923, 393.472, 394.021,
                            394.569, 395.118, 395.667, 396.215, 396.764, 397.313, 397.861, 398.41,
                            398.958, 399.507, 400.056, 400.604, 401.153, 401.702, 402.25, 402.799,
                            403.348, 403.896, 404.445, 404.994, 405.542, 406.091, 406.639, 407.188,
                            407.737, 408.285, 408.834, 411.59, 419.271, 426.952, 434.633, 442.314,
                            449.995, 457.676, 465.357, 473.038, 480.719])

# units='psi'
USatm1976Data.P = np.array([15.2348, 14.6959, 14.1726, 13.6644, 13.1711, 12.6923, 12.2277, 11.777,
                            11.3398, 10.9159, 10.5049, 10.1065, 9.7204, 9.34636, 8.98405, 8.63321,
                            8.29354, 7.96478, 7.64665, 7.33889, 7.04123, 6.75343, 6.47523, 6.20638,
                            5.94664, 5.69578, 5.45355, 5.21974, 4.9941, 4.77644, 4.56651, 4.36413,
                            4.16906, 3.98112, 3.8001, 3.6258, 3.45803, 3.29661, 3.14191, 2.99447,
                            2.85395, 2.72003, 2.59239, 2.47073, 2.35479, 2.24429, 2.13897, 2.0386,
                            1.94293, 1.85176, 1.76486, 1.68204, 1.60311, 1.52788, 1.45618, 1.38785,
                            1.32272, 1.26065, 1.20149, 1.14511, 1.09137, 1.04016, 0.991347,
                            0.944827, 0.900489, 0.858232, 0.817958, 0.779578, 0.743039, 0.708261,
                            0.675156, 0.643641, 0.613638, 0.585073, 0.557875, 0.531976, 0.507313,
                            0.483825, 0.461455, 0.440148, 0.419853, 0.400519, 0.382101, 0.364553,
                            0.347833, 0.331902, 0.31672, 0.302253, 0.288464, 0.275323, 0.262796,
                            0.250856, 0.239473, 0.228621, 0.218275, 0.20841, 0.199003, 0.190032,
                            0.181478, 0.173319, 0.165537, 0.158114, 0.12582, 0.10041, 0.08046,
                            0.064729, 0.0522725, 0.0423688, 0.0344637, 0.0281301, 0.0230369,
                            0.0189267])

# units='slug/ft**3'
USatm1976Data.rho = np.array([0.00244752, 0.00237717, 0.00230839, 0.00224114, 0.00217539,
                              0.00211114, 0.00204834, 0.00198698, 0.00192704, 0.0018685, 0.00181132,
                              0.00175549, 0.00170099, 0.00164779, 0.00159588, 0.00154522, 0.00149581,
                              0.00144761, 0.00140061, 0.00135479, 0.00131012, 0.00126659, 0.00122417,
                              0.00118285, 0.0011426, 0.00110341, 0.00106526, 0.00102812, 0.000991984,
                              0.000956827, 0.000922631, 0.000889378, 0.00085705, 0.000825628,
                              0.000795096, 0.000765434, 0.000736627, 0.000708657, 0.000675954,
                              0.000644234, 0.000614002, 0.000585189, 0.000557728, 0.000531556,
                              0.000506612, 0.000482838, 0.00046018, 0.000438586, 0.000418004,
                              0.000398389, 0.000379694, 0.000361876, 0.000344894, 0.000328709,
                              0.000313284, 0.000298583, 0.000284571, 0.000271217, 0.00025849,
                              0.00024636, 0.000234799, 0.000223781, 0.000213279, 0.000203271,
                              0.000193732, 0.000184641, 0.000175976, 0.000167629, 0.000159548,
                              0.000151867, 0.000144566, 0.000137625, 0.000131026, 0.000124753,
                              0.000118788, 0.000113116, 0.000107722, 0.000102592, 9.77131E-05,
                              9.30725E-05, 8.86582E-05, 0.000084459, 8.04641E-05, 7.66632E-05,
                              7.30467E-05, 6.96054E-05, 6.63307E-05, 6.32142E-05, 6.02481E-05,
                              5.74249E-05, 5.47376E-05, 5.21794E-05, 4.97441E-05, 4.74254E-05,
                              4.52178E-05, 4.31158E-05, 0.000041114, 3.92078E-05, 3.73923E-05,
                              3.56632E-05, 3.40162E-05, 3.24473E-05, 2.56472E-05, 2.00926E-05,
                              1.58108E-05, 1.24948E-05, 9.9151E-06, 7.89937E-06, 6.3177E-06,
                              5.07154E-06, 4.08586E-06, 3.30323E-06])

# units='ft/s'
USatm1976Data.a = np.array([1120.28, 1116.45, 1112.61, 1108.75, 1104.88, 1100.99, 1097.09, 1093.18,
                            1089.25, 1085.31, 1081.36, 1077.39, 1073.4, 1069.4, 1065.39, 1061.36,
                            1057.31, 1053.25, 1049.18, 1045.08, 1040.97, 1036.85, 1032.71, 1028.55,
                            1024.38, 1020.19, 1015.98, 1011.75, 1007.51, 1003.24, 998.963, 994.664,
                            990.347, 986.01, 981.655, 977.28, 972.885, 968.471, 968.076, 968.076,
                            968.076, 968.076, 968.076, 968.076, 968.076, 968.076, 968.076, 968.076,
                            968.076, 968.076, 968.076, 968.076, 968.076, 968.076, 968.076, 968.076,
                            968.076, 968.076, 968.076, 968.076, 968.076, 968.076, 968.076, 968.076,
                            968.076, 968.076, 968.076, 968.337, 969.017, 969.698, 970.377, 971.056,
                            971.735, 972.413, 973.091, 973.768, 974.445, 975.121, 975.797, 976.472,
                            977.147, 977.822, 978.496, 979.169, 979.842, 980.515, 981.187, 981.858,
                            982.53, 983.2, 983.871, 984.541, 985.21, 985.879, 986.547, 987.215,
                            987.883, 988.55, 989.217, 989.883, 990.549, 991.214, 994.549, 1003.79,
                            1012.94, 1022.01, 1031, 1039.91, 1048.75, 1057.52,
                            1066.21, 1074.83])

# units='lbf*s/ft**2'
USatm1976Data.viscosity = np.array([3.81E-07, 3.78E-07, 3.76E-07, 3.74E-07, 3.72E-07, 3.70E-07,
                                    3.68E-07, 3.66E-07, 3.64E-07, 3.62E-07, 3.60E-07, 3.57E-07,
                                    3.55E-07, 3.53E-07, 3.51E-07, 3.49E-07, 3.47E-07, 3.45E-07,
                                    3.42E-07, 3.40E-07, 3.38E-07, 3.36E-07, 3.34E-07, 3.31E-07,
                                    3.29E-07, 3.27E-07, 3.25E-07, 3.22E-07, 3.20E-07, 3.18E-07,
                                    3.16E-07, 3.13E-07, 3.11E-07, 3.09E-07, 3.06E-07, 3.04E-07,
                                    3.02E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07,
                                    2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07,
                                    2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07,
                                    2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07,
                                    2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07, 2.99E-07,
                                    2.99E-07, 2.99E-07, 3.00E-07, 3.00E-07, 3.00E-07, 3.01E-07,
                                    3.01E-07, 3.01E-07, 3.02E-07, 3.02E-07, 3.03E-07, 3.03E-07,
                                    3.03E-07, 3.04E-07, 3.04E-07, 3.04E-07, 3.05E-07, 3.05E-07,
                                    3.05E-07, 3.06E-07, 3.06E-07, 3.06E-07, 3.07E-07, 3.07E-07,
                                    3.08E-07, 3.08E-07, 3.08E-07, 3.09E-07, 3.09E-07, 3.09E-07,
                                    3.10E-07, 3.10E-07, 3.10E-07, 3.11E-07, 3.11E-07, 3.11E-07,
                                    3.13E-07, 3.18E-07, 3.23E-07, 3.28E-07, 3.33E-07, 3.37E-07,
                                    3.42E-07, 3.47E-07, 3.51E-07, 3.56E-07])

T_interp = InterpND(method='akima', points=USatm1976Data.alt, values=USatm1976Data.T, extrapolate=True)
P_interp = InterpND(method='akima', points=USatm1976Data.alt, values=USatm1976Data.P, extrapolate=True)
rho_interp = InterpND(method='akima', points=USatm1976Data.alt, values=USatm1976Data.rho, extrapolate=True)
visc_interp = InterpND(method='akima', points=USatm1976Data.alt, values=USatm1976Data.viscosity, extrapolate=True)

_, _drho_dh = rho_interp.interpolate(USatm1976Data.alt, compute_derivative=True)
drho_dh_interp = InterpND(method='akima', points=USatm1976Data.alt, values=_drho_dh.ravel(), extrapolate=True)


class USatm1976Comp(om.ExplicitComponent):
    """
    Component model for the United States standard atmosphere 1976 tables.

    Data for the model was obtained from http://www.digitaldutch.com/atmoscalc/index.htm.

    Parameters
    ----------
    **kwargs : dict
        Dictionary of optional arguments.
    """
    def initialize(self):
        """
        Declare component options.
        """
        self.options.declare('num_nodes', types=int,
                             desc='Number of nodes to be evaluated in the RHS')

        gamma = 1.4  # Ratio of specific heads
        gas_c = 1716.49  # Gas constant (ft lbf)/(slug R)
        self._K = gamma * gas_c

    def setup(self):
        """
        Add component inputs and outputs.
        """
        nn = self.options['num_nodes']
        self.add_input('h', val=1.*np.ones(nn), units='ft')

        self.add_output('temp', val=1.*np.ones(nn), units='degR')
        self.add_output('pres', val=1.*np.ones(nn), units='psi')
        self.add_output('rho', val=1.*np.ones(nn), units='slug/ft**3')
        self.add_output('viscosity', val=1.*np.ones(nn), units='lbf*s/ft**2')
        self.add_output('drhos_dh', val=1.*np.ones(nn), units='slug/ft**4')
        self.add_output('sos', val=1*np.ones(nn), units='ft/s')

        arange = np.arange(nn)
        self.declare_partials(['temp', 'pres', 'rho', 'viscosity', 'drhos_dh', 'sos'], 'h',
                              rows=arange, cols=arange)

    def compute(self, inputs, outputs):
        """
        Interpolate atmospheric properties for a given altitude.

        Parameters
        ----------
        inputs : `Vector`
            `Vector` containing inputs.
        outputs : `Vector`
            `Vector` containing outputs.
        """
        outputs['temp'] = T_interp.interpolate(inputs['h'], compute_derivative=False)
        outputs['pres'] = P_interp.interpolate(inputs['h'], compute_derivative=False)
        outputs['rho'], outputs['drhos_dh'] = rho_interp.interpolate(inputs['h'], compute_derivative=True)
        outputs['viscosity'] = visc_interp.interpolate(inputs['h'], compute_derivative=False)
        outputs['sos'] = np.sqrt(self._K*outputs['temp'])

    def compute_partials(self, inputs, partials):
        """
        Compute sub-jacobian parts. The model is assumed to be in an unscaled state.

        Parameters
        ----------
        inputs : Vector
            Unscaled, dimensional input variables read via inputs[key].
        partials : Jacobian
            Subjac components written to partials[output_name, input_name].
        """
        T, dT_dh = T_interp.interpolate(inputs['h'], compute_derivative=True)
        _, dP_dh = P_interp.interpolate(inputs['h'], compute_derivative=True)
        _, drho_dh = rho_interp.interpolate(inputs['h'], compute_derivative=True)
        _, dvisc_dh = visc_interp.interpolate(inputs['h'], compute_derivative=True)
        _, d2rho_dh2 = drho_dh_interp.interpolate(inputs['h'], compute_derivative=True)

        partials['temp', 'h'] = dT_dh.ravel()
        partials['pres', 'h'] = dP_dh.ravel()
        partials['rho', 'h'] = drho_dh.ravel()
        partials['viscosity', 'h'] = dvisc_dh.ravel()
        partials['drhos_dh', 'h'] = d2rho_dh2.ravel()
        partials['sos', 'h'][...] = 0.5/np.sqrt(self._K*T)*partials['temp', 'h'] * self._K
