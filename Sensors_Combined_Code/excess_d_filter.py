def excess_d_filter(data, to_check, size, ratio):
    #data should be a list of at least length size, where size is an integer >1
    rel_list = data[-size:]
    #d_avg = 0
    d_avg_abs = 0
    #calc average difference between 2 data points
    for n in range(len(rel_list)-1):
        to_add = (rel_list[n] - rel_list[n+1])/(size - 1)
        #d_avg += to_add
        d_avg_abs += abs(to_add)
    if (rel_list[-1]-to_check) <= d_avg_abs*ratio:
        #check that the difference is within limits
        return True
    return False
