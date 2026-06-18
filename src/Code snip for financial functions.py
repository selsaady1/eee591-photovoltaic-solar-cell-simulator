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
