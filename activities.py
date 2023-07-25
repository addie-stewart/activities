import csv

original_file_name = 'activities.csv'

"""
Reads csv containing period in first column, names as other column headers, and activities as rows
Returns:
periods = {
    period: {
        activity: [campers in activity]
    }
}
"""
def read_csv(filename):
    periods = {'1': {}, '2': {}, '3': {}, '4': {}}

    with open(filename, 'r') as activities:
        reader = csv.reader(activities)

        for row in reader:
            if 'Period' in row[0]: # this is the header row with Period in first column and names in other columns, ex: {Period, Mary, John, ...}
                header = row
            elif row:
                if row[0] in periods: # this row contains a valid period, ex: {1, Extreme Combo, Horse Lovers, ...}
                    period = row[0]
                    camper_index = 0
                    for camper in header: # loop through names in header
                        if camper_index > 0 and camper: # do not include first column header (Period) or blanks
                            activity = row[camper_index]
                            period_str = str(period)
                            if activity in periods[period]:
                                periods[period_str][activity].append(camper)
                            else:
                                periods[period_str][activity] = [camper]
                        camper_index += 1
    return periods

"""
Returns: Camper in list of campers by index. If camper at that index does not exist, returns empty string
"""
def safe_get_camper(campers, index):
    try:
        return campers[index]
    except IndexError:
            return ''

"""
Creates a new csv file with activities as column headers and rows containing campers in those activities
Inputs: name of new file to be created, dictionary of activities and campers of structure {activity: [list of campers in activiity]}
"""
def write_csv(filename, activities):
    file = open(filename, 'w')
    writer = csv.writer(file)
    writer.writerow(activities.keys())

    # get max campers for a single activity so we know how many rows csv must contain
    max_campers = 0 
    for activity in activities:
        if len(activities[activity]) > max_campers:
            max_campers = len(activities[activity])
    
    # create new row with campers corresponding to activity in header row
    row_index = 0
    while row_index < max_campers:
        new_row = []
        for activity in activities:
            campers_in_activity = activities[activity]
            new_row.append(safe_get_camper(campers_in_activity, row_index))
        row_index += 1
        writer.writerow(new_row)

    file.close()

"""
Main script
Creates new file for each period
"""
periods = read_csv(original_file_name)
for period in periods:
    write_csv('period_' + str(period) + '_activities.csv', periods[period])
