# This code snip calculates the rates and cost for electricity usage fees
# and monthly fees.
# It assumes two inputs from other code: The arrays of PV_unused and load_unmet
# which are what goes to and comes from the grid respectivley.

# ***********************************************************************
# Generate arrays with month, day, hour of the day and hour of the year *
# ***********************************************************************

hour = np.arange(0.0,8760.0, 1) # hours of the year from 0 to 8760
hour_day = np.tile((np.arange(1,25)),365) # Generate an array with the hours 1 to 24 repeated 365 times
day_number = np.repeat((np.arange(1,366)),24)

# Month array consists of 8760 data points and has the month number for every hour of the year.
# Month array has a zero right at the transition from one month to another
# This makes it easy to see the months when variables are plotted for every hour of the year 
# The zero makes little difference in other calculations since its at night for only 12 hours of the year
month_hours = [744,1416,2160,2880,3624,4344,5088,5832,6552,7296,8016,8760]
month = np.zeros(8760)  # which month every hour of the year is in
count = 0
for idx in range(8760):
    if(idx<=month_hours[count]):
        month[idx]=1.0*count+1
    else:
        count=count+1
# Plots the Month array
if 0:  # 1 = plot the data, 0 = turn plot off
    plt.title('Month')
    plt.plot(month)
    plt.xlabel('hour of the year')
    plt.ylabel('rates')
    plt.show()

# Assuming the year starts on Monday, weekend is an array to determine which days are weekdays
# weekend has a zero if it is a weekday and 1 if it is a weekend
# Need this for electricity rate calculations and also for load calculations (depending on your load).
weekend_days = [0.0,0,0,0,0,1.0,1.0]
weekend = np.tile(np.repeat(weekend_days,24),52)
extra_day= np.repeat(0,24) # 24 extra hours to give an extra day since year is 365 not 364 (7*52) days
weekend = np.append(weekend, extra_day)


# ************************************************************
# Electricity rate calculations                              *
# ************************************************************

# Determine which season (winter = 1, spring = 2, or summer =3) and if on peak or off peak
# Season array gives which season each of the 12 months is. This depends on the rate structure, and the uesr needs to enter it.
season_1 = [1,2,3,4,11,12]
season_2 = [5,6,9,10]
season_3 = [7,8]

# define the times for peak electricity rates in all seasons.
# Season 1 is winter, season 2 is shoulder, seasone 3 is summer
peak_time_1 = [5,6,7,8,17,18,19,20]
peak_time_2 = [14,15,16,17,18,19]
peak_time_3 = [14,15,16,17,18,19]

# define the rates in all seasons
# Season 1 is winter, season 2 is shoulder, seasone 3 is summer
# First number is off-peak rate, second in on-peak rate.
rates_1 = [6.91,9.51]
rates_2 = [7.27,20.94]
rates_3 = [7.3,24.09]

# Note: could do this more compactly using 2D array
 
rate=np.zeros(len(month))
for idx, month_check in enumerate(month):
    if month_check in season_1:
        #print('month {:.0f} is in season 1' .format(month_check))
        if hour_day[idx] in peak_time_1:
            rate[idx] = rates_1[1]
            #print('rate is on peak for hour of day {:.0f} in season 1' .format(hour_day[idx]))
        else:
            rate[idx] = rates_1[0]
            #print('rate is off peak for hour of day {:.0f} in season 1' .format(hour_day[idx]))
    if month_check in season_2:
        if hour_day[idx] in peak_time_2 and weekend[idx]==0:
            rate[idx] = rates_2[1]
            #print('rate is on peak for hour of day {:.0f} in season 2' .format(hour_day[idx]))
        else:
            rate[idx] = rates_2[0]
            #print('rate is off peak for hour of day {:.0f} in season 2' .format(hour_day[idx]))
    if month_check in season_3:
        if hour_day[idx] in peak_time_3 and weekend[idx]==0:
             rate[idx] = rates_3[1]
            #rate[idx] = np.maximum(rates_3[0],rates_3[1]*weekend[idx])
        else:
            rate[idx] = rates_3[0]

# This plots rates for every hour of the year
if 0:  # 1 = plot the data, 0 = turn plot off
    plt.title('Electricity Usage Rates in Cents/kWh')
    plt.plot(rate)
    plt.xlabel('hour of the year')
    plt.ylabel('Electricity Usage Rates in Cents/kWh')
    plt.show()

# Plot the ELectricity Rates in heat map
if 0:  # 1 - plot the data, 0 - turn plot off
    plt.figure('Rates in cents/kWh')
    plt.title('Rates in cents/kWh \n ' +details4plot)
    rate_2D = rate.reshape(-1,24)
    plt.xlabel('hour')
    plt.ylabel('day number')
    plt.imshow(rate_2D, cmap='jet', aspect='auto')
    plt.colorbar()
    plt.show()

# Electricity Yearly Charges

# Calculate Monthly Fee
monthly_fee = 32.44 # SRP Monthly Fee
cost_monthly_fee = monthly_fee*12

# Calculate Electricity Usage Charges
#First determine if net metering or not
net_metering = 0 # If set to 0, no net metering, 1 means there is net metering
buy_back=np.zeros(8760)
buy_back=rate  # Default is net metering, where utility buy-back and sell rates are the same
if net_metering == 0:
    net_metering = 2.81  # SRP Buy-back rate

cost_electricity_usage_hourly= 1e-2*(rate*load_unmet - buy_back*PV_unused)
cost_electricity_usage=sum(cost_electricity_usage_hourly)

# Plot the Cost per hour in cents
if 1:  # 1 - plot the data, 0 - turn plot off
    plt.figure('Electricity Usage cost per hour')
    plt.title('Electricity Usage cost per hour in $/hour\n ' +details4plot)
    cost_electricity_usage_2D = cost_electricity_usage_hourly.reshape(-1,24)
    plt.xlabel('hour')
    plt.ylabel('day number')
    plt.imshow(cost_electricity_usage_2D, cmap='jet', aspect='auto')
    plt.colorbar()
    plt.show()
    
print('\t Monthly Charge  = ${:.2f} ' .format(cost_monthly_fee).replace('$-','-$'))
print('\t Electricity Usage = ${:.2f}' .format(cost_electricity_usage))
print('\t Total cost = ${:.2f}' .format(cost_monthly_fee + cost_electricity_usage ).replace('$-','-$'))
print('\t LCOE component from Electrical Grid only = ${:.4f} kWh'. format((cost_monthly_fee + cost_electricity_usage)/sum(Load)))

