import os
from subprocess import run as چلو
import numpy as نمپی
import calendar
from pkg_resources import resource_filename as وسائل_کا_نام
from PyMarkSim import لغت_قابو

مسل_مرکسم = لغت_قابو['مسل_مرکسم']  #
path_gcm_data = ''  # Path to the GMC data files


"""
Do not edit anything below this line!
"""

راستہ_سانچے = وسائل_کا_نام('PyMarkSim', 'سانچے.CLI')


class مقام(object):
    def __init__(خود, چوڑائی, طول, بلندی):
        خود.چوڑائی = چوڑائی
        خود.طول = طول
        خود.بلندی = بلندی

    def پیشنگوئی_کرنا(خود, پہلا_سال, آخرا_سال, ار_سی_پی):
        # 'rcp26', 'rcp45', 'rcp60' or 'rcp85'

        #
        if آخرا_سال < پہلا_سال:
            raise ValueError('پہلا سال اکر سال کے پہلہ ینا ہے.')
        if آخرا_سال > 2099 or پہلا_سال < 2013:
            raise ValueError('سال ٢٠١٢ اور ٢٠٩٩ کے بچ میں ہونے پڑتے ہیں.')

        with open(راستہ_سانچے) as م:
            سانچے = م.readlines()

        #
        for س, قطار in enumerate(سانچے):
            سانچے[س] = قطار.format(LAT=خود.چوڑائی, LONG=خود.طول, ELEV=خود.بلندی)

        #
        راستہ_موجودہ = os.path.dirname(os.path.realpath(__file__))

        #
        with open(os.path.join(راستہ_موجودہ, 'PYTH.CLI'), 'w') as d:
            d.write(''.join(سانچے))

        #
        ش_مہینہ = (آخرا_سال - پہلا_سال + 1) * 12
        فہرست_مہینہ = نمپی.empty(ش_مہینہ)
        فہرست_سال = نمپی.empty(ش_مہینہ)
        temp_max_monthly = نمپی.empty(ش_مہینہ, dtype=float)
        temp_min_monthly = نمپی.empty(ش_مہینہ, dtype=float)
        temp_avg_monthly = نمپی.empty(ش_مہینہ, dtype=float)
        solar_rad_monthly = نمپی.empty(ش_مہینہ, dtype=float)
        precip_monthly = نمپی.empty(ش_مہینہ, dtype=float)

        # ہر سال کے لئے...
        for سال in range(پہلا_سال, آخرا_سال + 1):

            #
            args = dict(
                مسل_مرکسم=مسل_مرکسم,
                راستہ_١=path_gcm_data,
                راستہ_٢=راستہ_موجودہ,
                سانچے='11111111111111111',
                ار_سی_پی=ار_سی_پی,
                سال=سال,
                تکرار=1,
                بھیج=1313
            )

            #
            فرمان= '{مسل_مرکسم} {راستہ_١} {راستہ_٢} {سانچے} {ار_سی_پی} {سال} {تکرار} {بھیج}'.format(**args)

            #
            چلو(فرمان)

            #
            mks_output_file_name = 'PYTH{0}01.WTG'.format(str(سال)[-2:])
            mks_output_file = os.path.join(current_dir, 'PYTH', '11111111111111111', ار_سی_پی, str(سال),
                                           mks_output_file_name)

            #
            with open(mks_output_file, 'r') as م:
                #
                عنوان = ''
                while '@DATE' not in عنوان:
                    عنوان = م.readline()

                col_names = عنوان.split()
                #
                output = d.readlines()

            #
            day = [x[col_names.index('@DATE')] for x in output]
            solar_rad = نمپی.array([float(x.split()[col_names.index('SRAD')]) for x in output if x != '\n'])
            temp_max = نمپی.array([float(x.split()[col_names.index('TMAX')]) for x in output if x != '\n'])
            temp_min = نمپی.array([float(x.split()[col_names.index('TMIN')]) for x in output if x != '\n'])
            precip = نمپی.array([float(x.split()[col_names.index('RAIN')]) for x in output if x != '\n'])

            # Calculate average temperature
            temp_avg = نمپی.add(temp_max, temp_min) / 2

            # Calculate monthly data
            for m in range(12):
                month_range = calendar.monthrange(year, month=m + 1)
                start = month_range[0] - 1
                end = month_range[1] - 1

                data_pt = m + (year - year_start) * 12
                list_month[data_pt] = m + 1
                list_year[data_pt] = year
                temp_max_monthly[data_pt] = نمپی.mean(temp_max[start: end])
                temp_min_monthly[data_pt] = نمپی.mean(temp_min[start: end])
                temp_avg_monthly[data_pt] = نمپی.mean(temp_avg[start: end])
                solar_rad_monthly[data_pt] = نمپی.mean(solar_rad[start: end])
                # Only precipitation is given as a monthly total (instead of a monthly average)
                precip_monthly[data_pt] = نمپی.sum(precip[start: end])


    def بچانا(خود):
        # Save the data in csv format
        csv_headers = ','.join(['Year', 'Month', 'Tmax', 'Tmin', 'Tavg', 'SolarRad'])

        csv_data = [csv_headers]

        list_data = [list_year, list_month, temp_max_monthly, temp_min_monthly, temp_avg_monthly, solar_rad_monthly]

        for m in range((year_end - year_start + 1) * 12):  # For every month, in every year...
            data_month = [x[m] for x in list_data]
            csv_data.append(','.join(data_month))

        with open(output_file, 'w') as d:
            d.write(''.join(csv_data))
