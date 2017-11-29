from taqdir.Predictores.predictor import Predictor


class مرکسم٣(Predictor):
    def gen_datos(خود, de, hasta, ار_سی_پی, n_rep, recalc=True):

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
        with open(os.path.join(راستہ_موجودہ, 'TQDR.CLI'), 'w') as م:
            م.write(''.join(سانچے))

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
            فرمان = '{مسل_مرکسم} {راستہ_١} {راستہ_٢} {سانچے} {ار_سی_پی} {سال} {تکرار} {بھیج}'.format(**args)

            #
            چلو(فرمان)

            #
            mks_output_file_name = 'PYTH{0}01.WTG'.format(str(سال)[-2:])
            mks_output_file = os.path.join(راستہ_موجودہ, 'PYTH', '11111111111111111', ار_سی_پی, str(سال),
                                           mks_output_file_name)

            #
            with open(mks_output_file, 'r') as م:
                #
                عنوان = ''
                while '@DATE' not in عنوان:
                    عنوان = م.readline()

                ستون_کا_نام = عنوان.split()
                #
                پیداوار = م.readlines()

            #
            دن = [ب[ستون_کا_نام.index('@DATE')] for ب in پیداوار]
            شمسی_تابکاری = نمپی.array([float(ب.split()[ستون_کا_نام.index('SRAD')]) for ب in پیداوار if ب != '\n'])
            درجہ_حرارت_زیادہ = نمپی.array([float(ب.split()[ستون_کا_نام.index('TMAX')]) for ب in پیداوار if ب != '\n'])
            درجہ_حرارت_کم = نمپی.array([float(ب.split()[ستون_کا_نام.index('TMIN')]) for ب in پیداوار if ب != '\n'])
            بارش = نمپی.array([float(ب.split()[ستون_کا_نام.index('RAIN')]) for ب in پیداوار if ب != '\n'])

            #
            درجہ_حرارت_اوسط = نمپی.add(درجہ_حرارت_زیادہ, درجہ_حرارت_کم) / 2

            خود.اعداد = {
                'دن': {
                    'دن': دن,
                    'شمسی_تابکاری': شمسی_تابکاری,
                    'درجہ_حرارت_زیادہ': درجہ_حرارت_زیادہ,
                    'درجہ_حرارت_کم': درجہ_حرارت_کم,
                    'بارش': بارش,
                    'درجہ_حرارت_اوسط': درجہ_حرارت_اوسط
                },

            }
