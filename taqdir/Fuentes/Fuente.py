from datetime import timedelta
import pandas as pd
import numpy as نمپی
import calendar
import numpy as np

class Fuente(object):

    rango_potencial = None

    def __init__(خود, چوڑائی, طول, بلندی):
        خود.چوڑائی = چوڑائی
        خود.طول = طول
        خود.بلندی = بلندی

        خود.rango_actual = None
        خود.datos = None  # type: pd.DataFrame
        خود.mensuales = None  # type: pd.DataFrame
        خود.cols_día = ['بارش', 'شمسی_تابکاری', 'درجہ_حرارت_زیادہ', 'درجہ_حرارت_کم', 'درجہ_حرارت_اوسط']
        خود.cols_mes = ['فہرست_مہینہ', 'فہرست_سال', 'درجہ_حرارت_زیادہ_م', 'درجہ_حرارت_کم_م',
                        'درجہ_حرارت_اوسط_م', 'شمسی_تابکاری_م', 'مہینہ_بارش']

    def obt_datos(símismo, de, hasta, rcp=None, n_rep=1, usar_caché=True, regenerar=False):

        if regenerar:
            símismo.gen_datos(de=de, hasta=hasta, rcp=rcp, n_rep=n_rep, usar_caché=usar_caché)
        else:
            if símismo.rango_actual is None or (de < símismo.rango_actual[0] or hasta > símismo.rango_actual[1]):
                símismo.gen_datos(de=de, hasta=hasta, rcp=rcp, n_rep=n_rep, usar_caché=usar_caché)

        return símismo.datos[de:hasta]

    def gen_datos(símismo, de, hasta, rcp, n_rep, usar_caché):

        if símismo.rango_potencial is not None:
            if de < símismo.rango_potencial[0]:
                raise ValueError()
            if hasta > símismo.rango_potencial[1]:
                raise ValueError()

        fechas = pd.date_range(de, hasta)

        símismo.datos = pd.DataFrame(index=fechas, columns=símismo.cols_día)

        datos = símismo._gen_datos(de=de, hasta=hasta, usar_caché=usar_caché)

        símismo.datos.update(datos)

        símismo.rango_actual = (de, hasta)

    def _gen_datos(símismo, de, hasta, usar_caché):
        """

        :param de:
        :type de:
        :param hasta:
        :type hasta:
        :param usar_caché:
        :type usar_caché:
        :return:
        :rtype: np.ndarray
        """
        raise NotImplementedError

    def gen_mensuales(símismo):

        r = símismo.rango_actual

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

        bd = símismo.datos
        bd_mens = símismo.mensuales = pd.DataFrame(index=range(ش_مہینہ), columns=símismo.cols_mes)

        #
        فہرست_مہینہ = نمپی.empty(ش_مہینہ)
        فہرست_سال = نمپی.empty(ش_مہینہ)
        درجہ_حرارت_زیادہ_م = نمپی.empty(ش_مہینہ, dtype=float)
        درجہ_حرارت_کم_م = نمپی.empty(ش_مہینہ, dtype=float)
        درجہ_حرارت_اوسط_م = نمپی.empty(ش_مہینہ, dtype=float)
        شمسی_تابکاری_م = نمپی.empty(ش_مہینہ, dtype=float)
        مہینہ_بارش = نمپی.empty(ش_مہینہ, dtype=float)

        #
        for سال in range(پہلا_سال, آخرا_سال + 1):
            for م in range(12):
                مہینہ_لمبائی = calendar.monthrange(سال, month=م + 1)
                شروع = مہینہ_لمبائی[0] - 1
                اختتام = مہینہ_لمبائی[1] - 1

                مہینہ_شمار = م + (سال - پہلا_سال) * 12
                فہرست_مہینہ[مہینہ_شمار] = م + 1
                فہرست_سال[مہینہ_شمار] = سال
                درجہ_حرارت_زیادہ_م[مہینہ_شمار] = نمپی.mean(bd['درجہ_حرارت_زیادہ'][شروع: اختتام])
                درجہ_حرارت_کم_م[مہینہ_شمار] = نمپی.mean(bd['درجہ_حرارت_کم'][شروع: اختتام])
                درجہ_حرارت_اوسط_م[مہینہ_شمار] = نمپی.mean(bd['درجہ_حرارت_اوسط'][شروع: اختتام])
                شمسی_تابکاری_م[مہینہ_شمار] = نمپی.mean(bd['شمسی_تابکاری'][شروع: اختتام])

                # پر ہر دن کا بارش جوڈکے دینا ہے (اور اوسط دینا نہیں).
                مہینہ_بارش[مہینہ_شمار] = نمپی.sum(bd['بارش'][شروع: اختتام])

        bd_mens[:] = NotImplemented
