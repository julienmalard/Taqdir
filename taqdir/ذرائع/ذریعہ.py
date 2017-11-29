from datetime import timedelta
import pandas as پاندس
import numpy as نمپی
import calendar


class ذریعہ(object):

    rango_potencial = None

    def __init__(خود, چوڑائی, طول, بلندی):
        خود.چوڑائی = چوڑائی
        خود.طول = طول
        خود.بلندی = بلندی

        خود.rango_actual = None
        خود.اعداد_دن = None  # type: پاندس.DataFrame
        خود.اعداد_مہینہ = None  # type: پاندس.DataFrame
        خود.cols_día = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']
        خود.cols_mes = ['مہینہ', 'سال', 'فہرست_سال', 'درجہ_حرارت_زیادہ_م', 'درجہ_حرارت_کم_م',
                        'درجہ_حرارت_اوسط_م', 'شمسی_تابکاری_م', 'مہینہ_بارش']

    def اعداد_پانا(خود, سے, تک, rcp=None, n_rep=1, usar_caché=True, regenerar=False):

        if regenerar:
            خود.اعداد_پیدا_کرنا(سے=سے, تک=تک, ار_سی_پی=rcp, n_rep=n_rep, usar_caché=usar_caché)
        else:
            if خود.rango_actual is None or (سے < خود.rango_actual[0] or تک > خود.rango_actual[1]):
                خود.اعداد_پیدا_کرنا(سے=سے, تک=تک, ار_سی_پی=rcp, n_rep=n_rep, usar_caché=usar_caché)

        return خود.اعداد_دن[سے:تک]

    def اعداد_پیدا_کرنا(خود, سے, تک, ار_سی_پی, n_rep, usar_caché):

        if خود.rango_potencial is not None:
            if سے < خود.rango_potencial[0]:
                raise ValueError()
            if تک > خود.rango_potencial[1]:
                raise ValueError()

        تاریخیں = پاندس.date_range(سے, تک)

        خود.اعداد_دن = پاندس.DataFrame(index=تاریخیں, columns=خود.cols_día)

        اعداد = خود._اعداد_پیدا_کرنا(سے=سے, تک=تک, ار_سی_پی=ار_سی_پی, n_rep=n_rep, usar_caché=usar_caché)

        خود.اعداد_دن.update(اعداد)

        خود.rango_actual = (سے, تک)

    def _اعداد_پیدا_کرنا(خود, سے, تک, ار_سی_پی, n_rep, usar_caché):
        """

        :param سے:
        :type سے:
        :param تک:
        :type تک:
        :param usar_caché:
        :type usar_caché:
        :return:
        :rtype: نمپی.ndarray
        """
        raise NotImplementedError

    def gen_mensuales(خود):

        r = خود.rango_actual

        if r[0].day == 1:
            primer_mes = r[0].month
            پہلا_سال = r[0].year
        else:
            primer_mes = r[0].month + 1
            if primer_mes == 13:
                پہلا_سال = r[0].year
            else:
                primer_mes = 1
                پہلا_سال = r[0].year - 1

        if (r[1] + timedelta(1)).month == r[1].month:
            último_mes = r[1].month - 1
            if último_mes == 0:
                último_mes = 12
                آخرا_سال = r[1].year - 1
            else:
                آخرا_سال = r[1].year
        else:
            último_mes = r[1].month
            آخرا_سال = r[1].year

        ش_مہینہ = (آخرا_سال - پہلا_سال + 1) * 12 + (último_mes - primer_mes)

        اعداد_دن = خود.اعداد_دن
        اعداد_مہینہ = خود.اعداد_مہینہ = پاندس.DataFrame(index=range(ش_مہینہ), columns=خود.cols_mes)

        #
        for سال in range(پہلا_سال, آخرا_سال + 1):
            for م in range(12):
                مہینہ_لمبائی = calendar.monthrange(سال, month=م + 1)
                شروع = مہینہ_لمبائی[0] - 1
                اختتام = مہینہ_لمبائی[1] - 1

                مہینہ_شمار = م + (سال - پہلا_سال) * 12
                اعداد_مہینہ['مہینہ'][مہینہ_شمار] = م + 1
                اعداد_مہینہ['سال'][مہینہ_شمار] = سال
                اعداد_مہینہ['درجہ_حرارت_زیادہ_م'][مہینہ_شمار] = نمپی.mean(اعداد_دن['درجہ_حرارت_زیادہ'][شروع: اختتام])
                اعداد_مہینہ['درجہ_حرارت_کم_م'][مہینہ_شمار] = نمپی.mean(اعداد_دن['درجہ_حرارت_کم'][شروع: اختتام])
                اعداد_مہینہ['درجہ_حرارت_اوسط_م'][مہینہ_شمار] = نمپی.mean(اعداد_دن['درجہ_حرارت_اوسط'][شروع: اختتام])
                اعداد_مہینہ['شمسی_تابکاری_م'][مہینہ_شمار] = نمپی.mean(اعداد_دن['شمسی_تابکاری'][شروع: اختتام])

                # پر ہر مہینہ کا بارش جوڈکے دینا ہے (اور اوسط دینا نہیں).
                اعداد_مہینہ['مہینہ_بارش'][مہینہ_شمار] = نمپی.sum(اعداد_دن['بارش'][شروع: اختتام])
