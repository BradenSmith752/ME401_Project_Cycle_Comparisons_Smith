"""
============================================================
 ME401 Project: Otto and Diesel Cycle Comparisons
 Only Using Engines, Fuel Consumption, and Carbon Emissions
============================================================
 Written by: Denny Smith
 Date: 10/30/2026
 Description:
     Computes and compares ideal, air-standard efficiences, real world efficiencies, fuel consumption rates,
     and CO2 emissions between a spark-ignition Otto Engine and a compression ignition Diesel Engine
"""
import numpy as np
import matplotlib.pyplot as plt

"""
=======================================
 Establishing Constants and Properties
 Assuming constant cv and cp values
=======================================
"""
# Thermodynamic Constants
R_air = .287    # [kJ/kg*K] The specific gas constant for air
k_air = 1.4     # [] The specific heat ratio (cp / cv) for air
T_1 = 298.15    # [K] The ambient temperature of the enviroment the cycle uses (~25*C)
P_1 = 101.325   # [kPa] The ambient pressure of the enviroment the cycle uses (~1atm)

# Evaluation Properties for Engine Testing
Trip_distance = 100   # [miles] EPA standard baseline distance for CO2 emissions

Fuel_properties = {
    "Gasoline: Otto Cycle": {
        "name": "Gasoline Spark Ignition (Otto Cycle)",
        "LHV": 43400,                    # [kJ/kg] The lower heating value for gasoline
        "density": 2.81,                 # [kg/gal] The density of gasoline
        "carbon percentage": .870,       # [%] Mass fraction of carbon in gasoline
        "CO2_g_per_gal": 8887,           # [g/gal] EPA Tailpipe CO2 for gasoline
        "eta_brake": .35,                # [%] Peak break thermal efficiency for gasoline engines
        "r_min": 8.0,                    # Minimum compression ratio for gasoline engines
        "r_max": 12.0,                   # Maximum compression ratio for gasoline engines
        "mpg_ranges": (14.0, 22.0),      # [mpg] Real world fuel economy range of a Gasoline powered 5.3L V8 engine (representing the otto cycle)
        },
    "Diesel: Diesel Cycle": {
        "name": "Diesel Compression Ignition (Diesel Cycle)",
        "LHV": 42600,                    # [kJ/kg] The lower heating value for diesel
        "density": 3.14,                 # [kg/gal] The density of diesel
        "carbon percentage": .870,       # [%] Mass fraction of carbon in diesel
        "CO2_g_per_gal": 10180,          # [g/gal] EPA Tailpipe CO2 for diesel
        "eta_brake": .41,                # [%] Peak break thermal efficiency for diesel engines
        "r_min": 15.0,                   # Minimum compression ratio for diesel engines
        "r_max": 22.0,                   # Maximum compression ratio for diesel engines
        "mpg_ranges": (23, 33),          # [mpg] Real world fuel economy range of a diesel powered 3.0L Duramax Diesel Engine (representing the diesel cycle)
        }
}

"""
================================
 Computing Thermal Efficiencies
 And Emissions Outputs
================================
"""
def calc_otto_efficiency(r,k=k_air):
    """
    Parameters:
        r : 
            float
            The compression ratios for gasoline engines
        k : 
            float
            The specific heat ratio of air
    Computes:
        Ideal air standard Otto cycle thermal efficiency
    Equation:
        eta_otto = 1 - (1/r^(k-1))
    """
    return (1.0 - (1.0 / r**(k - 1.0)))

def calc_diesel_efficiency(r,r_c,k=k_air):
    """
    Parameters:
        r: 
            float
            Compression ratio for diesel engines
        r_c: 
            float
            Cutoff ratio for diesel engines
        k: 
            float
            the specific heat ratio of air
        Computes:
            Ideal air-standard diesel cycle thermal efficiency
        Equations:
            eta_diesel = 1 - (1/(k*r^(k-1))) * [ (r_c^k - 1) / (r_c - 1)]
    """
    return (1 - (1/(k*r**(k-1))) * ((r_c**k - 1) / (r_c - 1)))

def calc_emissions_from_mpg(distance_miles,mpg,fuel_dictionary):
    """
    Calculates total fuel volume in gallons, the mass of the fuel (kg),
    total tailpipe CO2 (kg), and distance specific CO2 emissions (g/mile)
    based on real world fuel economy taken from maufacturer data (mpg)
    """
    gallons_used = distance_miles / mpg
    fuel_mass_kg = gallons_used * fuel_dictionary["density"]
    total_CO2_g = gallons_used * fuel_dictionary["CO2_g_per_gal"]
    CO2_kg = total_CO2_g / 1000.00
    CO2_per_mile_g = total_CO2_g / distance_miles    
    return {
        "gallons used": gallons_used,
        "Mass_kg": fuel_mass_kg,
        "CO2_used_kg": CO2_kg,
        "CO2_per_mile_g": CO2_per_mile_g
        }

"""
===============================
 State Calculations
===============================
"""
# ------------P-v and T-s Calculations--------------------
# Using average r values froom my ranges for cycle calculations
r_otto_avg = np.mean([Fuel_properties["Gasoline: Otto Cycle"]["r_min"],Fuel_properties["Gasoline: Otto Cycle"]["r_max"]])
r_diesel_avg = np.mean([Fuel_properties["Diesel: Diesel Cycle"]["r_min"],Fuel_properties["Diesel: Diesel Cycle"]["r_max"]])
c_v = R_air / (k_air - 1.0)
c_p = k_air*c_v

# ---------- Otto States ------------
# State 1
v_otto_1 = (R_air * T_1) / P_1
p_otto_1 = P_1
t_otto_1 = T_1
s_otto_1 = 0 # Because I can not for the life of me find the actual s value of air at this state
# State 2
v_otto_2 = v_otto_1 / r_otto_avg
p_otto_2 = p_otto_1 * (r_otto_avg**k_air)
t_otto_2 = t_otto_1 * (r_otto_avg**(k_air-1.0))
s_otto_2 = s_otto_1
# State 3
LHV_otto = Fuel_properties["Gasoline: Otto Cycle"]["LHV"]
stoich_air_gas_ratio = 14.7 # Standard air-fuel ratio for air to gasoline (m_air / m_gas)
q_otto_in = (LHV_otto) / (stoich_air_gas_ratio + 1.0) # Setting for 1kg of fuel
v_otto_3 = v_otto_2
t_otto_3 = t_otto_2 + (q_otto_in / c_v)
p_otto_3 = p_otto_2 * (t_otto_3 / t_otto_2)
s_otto_3 = s_otto_2 + c_v * np.log(t_otto_3 / t_otto_2)
# State 4
v_otto_4 = v_otto_1
p_otto_4 = p_otto_3 / r_otto_avg**(k_air)
t_otto_4 = t_otto_3 / r_otto_avg**(k_air-1.0)
s_otto_4 = s_otto_3

# -----------Diesel States----------------
# State 1
v_diesel_1 = (R_air * T_1) / P_1
p_diesel_1 = P_1
t_diesel_1 = T_1
s_diesel_1 = 0
# State 2
v_diesel_2 = v_diesel_1 / r_diesel_avg
p_diesel_2 = p_diesel_1 * (r_diesel_avg**k_air)
t_diesel_2 = t_diesel_1 * r_diesel_avg**(k_air-1)
s_diesel_2 = s_diesel_1
# State 3
stoich_air_diesel_ratio = 14.4 # Standard air-fuel ratio for air to diesel (m_air / m_diesel) (taken from an online source)
lhv_diesel = Fuel_properties["Diesel: Diesel Cycle"]["LHV"]
q_diesel_in = (lhv_diesel) / (stoich_air_diesel_ratio + 1.0) # Setting for 1kg of fuel
t_diesel_3 = t_diesel_2 + q_diesel_in / c_p
r_cutoff_diesel = t_diesel_3 / t_diesel_2
v_diesel_3 = v_diesel_2 * r_cutoff_diesel
p_diesel_3 = p_diesel_2
s_diesel_3 = s_diesel_2 + c_p*np.log(t_diesel_3 / t_diesel_2)
# State 4
v_diesel_4 = v_diesel_1
p_diesel_4 = p_diesel_3 * (r_cutoff_diesel/r_diesel_avg)**k_air
t_diesel_4 = t_diesel_3 * (r_cutoff_diesel/r_diesel_avg)**(k_air-1.0)
s_diesel_4 = s_diesel_3

"""
============================================================
        P-v and T-s diagrams
============================================================
"""
fig, axes = plt.subplots(2, 2, figsize = (14,10))
ax_otto_pv, ax_otto_ts = axes[0,0], axes[0,1]
ax_diesel_pv, ax_diesel_ts = axes[1,0], axes[1,1]

# --- Otto Cycle P-v diagram (Keeping your working P-v logic) ---
v_o_12 = np.linspace(v_otto_1, v_otto_2, 50)
p_o_12 = p_otto_1 * (v_otto_1 / v_o_12)**k_air
v_o_34 = np.linspace(v_otto_3, v_otto_4, 50)
p_o_34 = p_otto_3 * (v_otto_3 / v_o_34)**k_air
ax_otto_pv.plot(v_o_12, p_o_12, color="#E53E3E", linewidth=3)
ax_otto_pv.plot([v_otto_2, v_otto_3],[p_otto_2, p_otto_3], color="#E53E3E", linewidth=3)
ax_otto_pv.plot(v_o_34, p_o_34, color="#E53E3E", linewidth=3)
ax_otto_pv.plot([v_otto_4, v_otto_1], [p_otto_4, p_otto_1], color="#E53E3E", linewidth=3, label="Otto Cycle")
ax_otto_pv.set_title("Otto Cycle: Pressure-Volume (P-v)", fontsize=12, fontweight='bold', pad=8)
ax_otto_pv.set_xlabel("Specific Volume ($v$) [$m^3/kg$]", fontsize=10)
ax_otto_pv.set_ylabel("Pressure ($P$) [$kPa$]", fontsize=10)
ax_otto_pv.set_yscale('log')
ax_otto_pv.legend(fontsize=9, loc="upper right")
ax_otto_pv.grid(True, linestyle='--', alpha=0.6)
ax_otto_pv.plot([v_otto_1, v_otto_2, v_otto_3, v_otto_4], [p_otto_1, p_otto_2, p_otto_3, p_otto_4], "ko")
for n, x, y in zip([1,2,3,4], [v_otto_1, v_otto_2, v_otto_3, v_otto_4], [p_otto_1, p_otto_2, p_otto_3, p_otto_4]):
    ax_otto_pv.text(x, y, f"  {n}", fontsize=12, fontweight="bold")
# --- Otto Cycle T-s diagram ---
t_o_12 = np.linspace(t_otto_1, t_otto_2, 50)
s_o_12 = np.full_like(t_o_12, s_otto_1)
t_o_23 = np.linspace(t_otto_2, t_otto_3, 50)
s_o_23 = s_otto_2 + c_v * np.log(t_o_23 / t_otto_2)
t_o_34 = np.linspace(t_otto_3, t_otto_4, 50)
s_o_34 = np.full_like(t_o_34, s_otto_3)
t_o_41 = np.linspace(t_otto_4, t_otto_1, 50)
s_o_41 = s_otto_1 + c_v * np.log(t_o_41 / t_otto_1)  # Or connecting s_otto_3 down to 0
ax_otto_ts.plot(s_o_12, t_o_12, color="#E53E3E", linewidth=2.5)
ax_otto_ts.plot(s_o_23, t_o_23, color="#E53E3E", linewidth=2.5)
ax_otto_ts.plot(s_o_34, t_o_34, color="#E53E3E", linewidth=2.5)
ax_otto_ts.plot(s_o_41, t_o_41, color="#E53E3E", linewidth=2.5, label="Otto Cycle")
ax_otto_ts.set_title("Otto Cycle: Temperature-Entropy (T-s)", fontsize=12, fontweight='bold', pad=8)
ax_otto_ts.set_xlabel("Specific Entropy ($s$) [$kJ/kg\cdot K$]", fontsize=10)
ax_otto_ts.set_ylabel("Temperature ($T$) [$K$]", fontsize=10)
ax_otto_ts.legend(fontsize=8, loc="upper left")
ax_otto_ts.grid(True, linestyle='--', alpha=0.6)
ax_otto_ts.plot([s_otto_1, s_otto_2, s_otto_3, s_otto_4], [t_otto_1, t_otto_2, t_otto_3, t_otto_4], "ko")
for n, x, y in zip([1,2,3,4], [s_otto_1, s_otto_2, s_otto_3, s_otto_4], [t_otto_1, t_otto_2, t_otto_3, t_otto_4]):
    ax_otto_ts.text(x, y, f"  {n}", fontsize=12, fontweight="bold")

# --- Diesel Cycle P-v diagram ---
v_d_12 = np.linspace(v_diesel_1, v_diesel_2, 50)
p_d_12 = p_diesel_1 * (v_diesel_1 / v_d_12)**k_air
v_d_34 = np.linspace(v_diesel_3, v_diesel_4, 50)
p_d_34 = p_diesel_3 * (v_diesel_3 / v_d_34)**k_air
ax_diesel_pv.plot(v_d_12, p_d_12, color="#3182CE", linewidth=3)
ax_diesel_pv.plot([v_diesel_2, v_diesel_3],[p_diesel_2, p_diesel_3], color="#3182CE", linewidth=3)
ax_diesel_pv.plot(v_d_34, p_d_34, color="#3182CE", linewidth=3)
ax_diesel_pv.plot([v_diesel_4, v_diesel_1], [p_diesel_4, p_diesel_1], color="#3182CE", linewidth=3, label="Diesel Cycle")
ax_diesel_pv.set_title("Diesel Cycle: Pressure-Volume (P-v)", fontsize=12, fontweight='bold', pad=8)
ax_diesel_pv.set_xlabel("Specific Volume ($v$) [$m^3/kg$]", fontsize=10)
ax_diesel_pv.set_ylabel("Pressure ($P$) [$kPa$]", fontsize=10)
ax_diesel_pv.set_yscale('log')
ax_diesel_pv.legend(fontsize=9, loc="upper right")
ax_diesel_pv.grid(True, linestyle='--', alpha=0.6)
ax_diesel_pv.plot([v_diesel_1, v_diesel_2, v_diesel_3, v_diesel_4], [p_diesel_1, p_diesel_2, p_diesel_3, p_diesel_4], "ko")
for n, x, y in zip([1,2,3,4], [v_diesel_1, v_diesel_2, v_diesel_3, v_diesel_4], [p_diesel_1, p_diesel_2, p_diesel_3, p_diesel_4]):
    ax_diesel_pv.text(x, y, f"  {n}", fontsize=12, fontweight="bold")
# --- Diesel Cycle T-s diagram ---
t_d_12 = np.linspace(t_diesel_1, t_diesel_2, 50)
s_d_12 = np.full_like(t_d_12, s_diesel_1)
t_d_23 = np.linspace(t_diesel_2, t_diesel_3, 50)
s_d_23 = s_diesel_2 + c_p * np.log(t_d_23 / t_diesel_2)
t_d_34 = np.linspace(t_diesel_3, t_diesel_4, 50)
s_d_34 = np.full_like(t_d_34, s_diesel_3)
t_d_41 = np.linspace(t_diesel_4, t_diesel_1, 50)
s_d_41 = s_diesel_1 + c_v * np.log(t_d_41 / t_diesel_1)
ax_diesel_ts.plot([s_diesel_1, s_diesel_2, s_diesel_3, s_diesel_4], [t_diesel_1, t_diesel_2, t_diesel_3, t_diesel_4], "ko")
ax_diesel_ts.plot(s_d_12, t_d_12, color="#3182CE", linewidth=2.5)
ax_diesel_ts.plot(s_d_23, t_d_23, color="#3182CE", linewidth=2.5)
ax_diesel_ts.plot(s_d_34, t_d_34, color="#3182CE", linewidth=2.5)
ax_diesel_ts.plot(s_d_41, t_d_41, color="#3182CE", linewidth=2.5, label="Diesel Cycle")
ax_diesel_ts.set_title("Diesel Cycle: Temperature-Entropy (T-s)", fontsize=12, fontweight='bold', pad=8)
ax_diesel_ts.set_xlabel("Specific Entropy ($s$) [$kJ/kg\cdot K$]", fontsize=10)
ax_diesel_ts.set_ylabel("Temperature ($T$) [$K$]", fontsize=10)
ax_diesel_ts.legend(fontsize=8, loc="upper left")
ax_diesel_ts.grid(True, linestyle='--', alpha=0.6)
for n, x, y in zip([1,2,3,4], [s_diesel_1, s_diesel_2, s_diesel_3, s_diesel_4], [t_diesel_1, t_diesel_2, t_diesel_3, t_diesel_4]):
    ax_diesel_ts.text(x, y, f"  {n}", fontsize=12, fontweight="bold")
plt.suptitle("ME 401 Project: Ideal Air-Standard Cycle Thermodynamic Diagrams", fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()
"""
===============================
 Main Code and Swept Variables
===============================
"""
# Compression Ratio Swept Variables
r_otto_range = np.linspace(Fuel_properties["Gasoline: Otto Cycle"]["r_min"],Fuel_properties["Gasoline: Otto Cycle"]["r_max"],25)
r_diesel_range = np.linspace(Fuel_properties["Diesel: Diesel Cycle"]["r_min"],Fuel_properties["Diesel: Diesel Cycle"]["r_max"],25)
r_cutoff_diesel_real = 1.55          # average cut off ratio for a diesel engine

otto_effic = [calc_otto_efficiency(r) for r in r_otto_range]
diesel_effic = [calc_diesel_efficiency(r, r_cutoff_diesel_real) for r in r_diesel_range]

# Fuel Economy
gas_mpg_sweep = np.linspace(Fuel_properties["Gasoline: Otto Cycle"]["mpg_ranges"][0], Fuel_properties["Gasoline: Otto Cycle"]["mpg_ranges"][1], 25)
diesel_mpg_sweep = np.linspace(Fuel_properties["Diesel: Diesel Cycle"]["mpg_ranges"][0], Fuel_properties["Diesel: Diesel Cycle"]["mpg_ranges"][1], 25)

gas_emissions = [calc_emissions_from_mpg(Trip_distance, mpg, Fuel_properties["Gasoline: Otto Cycle"]) for mpg in gas_mpg_sweep]
diesel_emissions = [calc_emissions_from_mpg(Trip_distance, mpg, Fuel_properties["Diesel: Diesel Cycle"]) for mpg in diesel_mpg_sweep]

gas_CO2_perMile = [res["CO2_per_mile_g"] for res in gas_emissions]
diesel_CO2_perMile = [res["CO2_per_mile_g"] for res in diesel_emissions]
"""
Printing Outputs
"""
print(f"\n[Baseline Comparison of a Gasoline Diesel Engines Over {Trip_distance}-Mile Driving Distance]\n")
print(f"{'Performance Metric':<40} | {'Gasoline (Otto Cycle)':<22} | {'Diesel (Diesel Cycle)':<22}")
print("=" * 90)
print(f"{'Peak Break Thermal Efficiency (η_b)':<40} | {Fuel_properties['Gasoline: Otto Cycle']['eta_brake']*100:5.1f}%                 | {Fuel_properties['Diesel: Diesel Cycle']['eta_brake']*100:5.1f}%")
print(f"{'Fuel Economy Range (MPG)':<40} | {Fuel_properties['Gasoline: Otto Cycle']['mpg_ranges'][0]} - {Fuel_properties['Gasoline: Otto Cycle']['mpg_ranges'][1]} MPG        | {Fuel_properties['Diesel: Diesel Cycle']['mpg_ranges'][0]} - {Fuel_properties['Diesel: Diesel Cycle']['mpg_ranges'][1]} MPG")
print(f"{'CO2 Emissions at Min MPG (g/mile)':<40} | {gas_CO2_perMile[0]:5.1f} g/mi             | {diesel_CO2_perMile[0]:5.1f} g/mile")
print(f"{'CO2 Emissions at Max MPG (g/mile)':<40} | {gas_CO2_perMile[-1]:5.1f} g/mi             | {diesel_CO2_perMile[-1]:5.1f} g/mile")
print("="*90)
# Plotting
fig = plt.figure(figsize=(16,14))
# Subplot 1
ax1 = plt.subplot2grid((2,2),(0,0))
ax1.plot(r_otto_range,otto_effic,label="Otto Cycle",color="#E53E3E",linewidth=2.5)
ax1.plot(r_diesel_range,diesel_effic,label=f"Diesel Cycle (Cutoff $r_c$ = {r_cutoff_diesel_real})", color="#3182CE", linewidth=2.5)
ax1.set_title("Ideal Thermal Efficiency vs. Compression Ratio",fontsize=15, fontweight='bold', pad=10)
ax1.set_xlabel("Compression Ratio ($r$)",fontsize=12)
ax1.set_ylabel("Air Standard Efficiency ($\eta_{th}$)",fontsize=12)
ax1.legend(fontsize=12,loc="lower right")
ax1.grid(True, linestyle='--',alpha=.6)
# Subplot 2
ax2 = plt.subplot2grid((2,2),(1,0),colspan=2)
ax2.plot(gas_mpg_sweep,gas_CO2_perMile,label="Gasoline (Otto Cycle) Range",color="#E53E3E",linestyle="--",marker="o",linewidth=1.5)
ax2.plot(diesel_mpg_sweep,diesel_CO2_perMile,label="Diesel (Diesel Cycle) Range",color="#3182CE",linestyle=":",marker="x",linewidth=1.5)
ax2.set_title("Tailpipe $\t{CO}_2$ Emissions vs. Real World Fuel Economy",fontsize=15,fontweight='bold',pad=10)
ax2.set_xlabel("Fuel Economy [MPG]",fontsize=12)
ax2.set_ylabel("Tailpipe $\t{CO}_2$ Emissions [g/mile]",fontsize=12)
ax2.legend(fontsize=12,loc="upper right")
ax2.grid(True,linestyle='--',alpha=.6)
# Subplot 3
gas_mass_kg = [res["Mass_kg"] for res in gas_emissions]
diesel_mass_kg = [res["Mass_kg"] for res in diesel_emissions]
ax3 = plt.subplot2grid((2, 2), (0, 1))
ax3.plot(gas_mpg_sweep, gas_mass_kg, label="Gasoline Fuel Mass", color="#E53E3E", linestyle="-", linewidth=3.5)
ax3.plot(diesel_mpg_sweep, diesel_mass_kg, label="Diesel Fuel Mass", color="#3182CE", linestyle="--", linewidth=3.5)
ax3.set_title(r"Total Fuel Mass Consumed vs. Fuel Economy (100-Mile Trip)", fontsize=15, fontweight='bold', pad=10)
ax3.set_xlabel("Fuel Economy [MPG]", fontsize=11)
ax3.set_ylabel("Total Fuel Mass Consumed [kg]", fontsize=11)
ax3.legend(fontsize=15, loc="upper right", frameon=True)
ax3.grid(True, linestyle='--', alpha=.6)
plt.suptitle("ME 401 Project: Thermodynamic Cycles & Emissions Comparitive Analysis",fontsize=20,fontweight='bold',y=1.03)
plt.tight_layout()
# Optional - Saves the figure as a .png
"""
output_filename = "Engine_Thermodyanmic_Emissions_Comparison.png"
plt.savefig(output_filename,dpi=300,bbox_inches="tight")
print(f"\n[Success] Analysis plots generated and saved successfully as '{output_filename}'.")
plt.show()
"""