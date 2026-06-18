hour = np.arange(0.0,8760.0, 1) # hours from 0 to 8760
day_number, hour_day = divmod(hour,24) 

month_hours = [744,1416,2160,2880,3624,4344,5088,5832,6552,7296,8016,8760]
month = np.zeros(8760)  # which month every hour of the year is in
count = 0
for idx in range(8760):
    if(idx<= month_hours[count]):
        month[idx]=count+1
    else:
        count=count+1
