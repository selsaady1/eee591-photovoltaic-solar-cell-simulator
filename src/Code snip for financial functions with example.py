# For the financial functions I return two values, the NPV or Annualized value
# and the factor, I return the factor since it makes checking values
# comparing different terms sometimes easier.

def NPV_from_FV(FV, rate, time_period):
    """Return the NPV given future vale (FV), the interest rate (rate), 
    with the future value at a time = time_period in the future
    """
    factor = pow((1+rate),-1*time_period)
    NPV = factor*FV
    return NPV, factor

def A_from_NPV(NPV, rate, time_period):
    """Return the annualized value given Net Present Value (NPV), the interest rate (rate), 
    and the period over which the NPV is annualized
    """
    factor = rate*pow((1+rate),time_period)/(pow((1+rate),time_period)-1)
    A = factor*NPV
    return A, factor

def NPV_from_geo(geo, interest_rate, growth_rate, n):
    """Return the NPV given geometrically increasing initial value of geo.
    """
    if interest_rate == growth_rate:
        factor = n/(1 + interest_rate)        
    else:
        factor = (1/(interest_rate - growth_rate))* (1 - pow((1+ interest_rate),-1*n)*pow((1+ growth_rate),n))
    NPV = factor*geo
    return NPV, factor

# ************************************************************
# Calculate Cost of PV System                                *
# ************************************************************

# Example of how to use functions. It uses inputs from other parts of your code of the total system W (system_W),
# the battery capacity, and the system voltage (system_V)

dollars_per_watt = 2  # Dollars per watt installed of PV system without batteries
inverter_replace_cost = 500  # Not used in this particular example, assume inverter is with system cost
O_and_M_percentage =  0.005    # fraction of intial costs
battery_per_kWh = 300
battery_voltage = 48
n = 25
battery_replace_time = 7
inverter_replace_time = 7

interest_rate = 0.03
O_and_M_growth = 0.035

# Calculate Initial PV Cost
PV_Initial_cost = dollars_per_watt*system_W

# Calculate Battery Costs
Initial_battery_cost = 1e-3*battery_per_kWh*capacity*system_V
npv_battery_cost = Initial_battery_cost  
count = 1
while(count*battery_replace_time<= n):
    battery_NPV, factor= NPV_from_FV(Initial_battery_cost, interest_rate, battery_replace_time*count)
    npv_battery_cost = npv_battery_cost + battery_NPV
    # print(count, 'Battery replace cost = $', year_battery_cost, 'at year', count*battery_replace_time)
    count=count+1

# Calculate Operation and Maintenance Costs
Initial_OM_cost = O_and_M_percentage*PV_Initial_cost
NPV_OM, factor = NPV_from_geo(Initial_OM_cost,interest_rate, O_and_M_growth, n)

# Calculate total NPV
NPV_system = PV_Initial_cost + npv_battery_cost + NPV_OM

# Calculate Annualized Cost
A_battery_cost, factor = A_from_NPV(npv_battery_cost, interest_rate, n)
A_PV = PV_Initial_cost*factor
A_OM = NPV_OM*factor
A_system = A_battery_cost + A_PV + A_OM
