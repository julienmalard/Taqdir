import os
from subprocess import run
import numpy as np
import calendar

lat, long = (3.500, -76.300)  # The lat and long coordinates (decimal format) for your region
elev = 965

# The starting and ending years of interest

year_start = 2013
year_end = 2099

# Can take values of 'rcp26', 'rcp45', 'rcp60' or 'rcp85' for RCP scenarios 2.6, 4.5, 6.0, or 8.5, respectively.
rcp = 'rcp85'

path_marksim_exe = ''  # Path to the MarkSim standalone
path_gcm_data = ''  # Path to the GMC data files

output_file = ''  # Where you would like the output to be stored

"""
Do not edit anything below this line!
"""

path_cli = ''  # Path to the CLI file


# Make sure that the start and end years are valid:
if year_end > 2099 or year_start < 2013:
    raise ValueError('Year must be between 2013 and 2099')

if year_end < year_start:
    raise ValueError('End year must be larger than start year!')

# Prepare the CLI file
current_dir = os.path.dirname(os.path.realpath(__file__))

# Read the template CLI file
with open(os.path.join(current_dir, 'TEMP.CLI')) as d:
    template = d.readlines()


dic_coords = dict(LAT=lat, LONG=long, ELEV=elev)

# Fill in our lat, long and elev data
for n, line in enumerate(template):
    template[n] = line.format(**dic_coords)

# And save the input file
with open(os.path.join(current_dir, 'PYTH.CLI'), 'w') as d:
    d.write(''.join(template))


# Create empty Numpy matrices to hold the eventual data
n_months = (year_end - year_start + 1) * 12

list_month = np.empty(n_months)
list_year = np.empty(n_months)
temp_max_monthly = np.empty(n_months, dtype=float)
temp_min_monthly = np.empty(n_months, dtype=float)
temp_avg_monthly = np.empty(n_months, dtype=float)
solar_rad_monthly = np.empty(n_months, dtype=float)
precip_monthly = np.empty(n_months, dtype=float)

# For every year of interest...
for year in range(year_start, year_end+1):

    # Set the appropriate arguments for the Marksim command line call. See Marksim V2 documentation online for details.
    args = dict(
        MarkSim_standalone=path_marksim_exe,
        path1=path_gcm_data,
        path2=path_cli,
        template='11111111111111111',
        RCP=rcp,
        year=year,
        nreps=1,
        seed=1313
    )

    # Prepare the command
    command = '{MarkSim_standalone} {path1} {path2} {template} {RCP} {year} {nreps} {seed}'.format(**args)

    # Run the command prompt command
    run(command)

    # Get the output file location
    mks_output_file_name = 'PYTH{0}01.WTG'.format(str(year)[-2:])
    mks_output_file = os.path.join(current_dir, 'PYTH', '11111111111111111', rcp, str(year), mks_output_file_name)

    # Read data from the output file
    with open(mks_output_file, 'r') as d:
        # Skip header lines
        h = ''
        while '@DATE' not in h:
            h = d.readline()

        col_names = h.split()
        # Save only the data
        output = d.readlines()

    # Read the output data into Numpy array format
    day = [x[col_names.index('@DATE')] for x in output]
    solar_rad = np.array([float(x.split()[col_names.index('SRAD')]) for x in output if x != '\n'])
    temp_max = np.array([float(x.split()[col_names.index('TMAX')]) for x in output if x != '\n'])
    temp_min = np.array([float(x.split()[col_names.index('TMIN')]) for x in output if x != '\n'])
    precip = np.array([float(x.split()[col_names.index('RAIN')]) for x in output if x != '\n'])

    # Calculate average temperature
    temp_avg = np.add(temp_max, temp_min) / 2

    # Calculate monthly data
    for m in range(12):
        month_range = calendar.monthrange(year, month=m + 1)
        start = month_range[0] - 1
        end = month_range[1] - 1

        data_pt = m + (year - year_start) * 12
        list_month[data_pt] = m + 1
        list_year[data_pt] = year
        temp_max_monthly[data_pt] = np.mean(temp_max[start: end])
        temp_min_monthly[data_pt] = np.mean(temp_min[start: end])
        temp_avg_monthly[data_pt] = np.mean(temp_avg[start: end])
        solar_rad_monthly[data_pt] = np.mean(solar_rad[start: end])
        # Only precipitation is given as a monthly total (instead of a monthly average)
        precip_monthly[data_pt] = np.sum(precip[start: end])


# Save the data in csv format
csv_headers = ','.join(['Year', 'Month', 'Tmax', 'Tmin', 'Tavg', 'SolarRad'])

csv_data = [csv_headers]

list_data = [list_year, list_month, temp_max_monthly, temp_min_monthly, temp_avg_monthly, solar_rad_monthly]

for m in range((year_end - year_start + 1) * 12):  # For every month, in every year...
    data_month = [x[m] for x in list_data]
    csv_data.append(','.join(data_month))


with open(output_file, 'w') as d:
    d.write(''.join(csv_data))