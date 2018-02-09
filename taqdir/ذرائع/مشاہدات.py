import calendar
import csv
import datetime as ft
import os

import numpy as نمپی
import pandas as پاندس
from taqdir.ذرائع.ذریعہ import ذریعہ
from taqdir.شمار import متن_سے_شمار


class دن_مشا(ذریعہ):

    def __init__(خود, مسل, س_تاریخ, س_اعداد, تبادلوں):
        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        خود.نام_شتونیں = س_اعداد
        خود.تبادلوں = تبادلوں

        خود.اعداد = اعداد_و_شمار_بنانا(مسل)

        for ن in س_اعداد.values():
            if ن not in خود.اعداد.نام_ستونیں:
                raise ValueError('')

        خود.دن = خود.اعداد.تاریخیں_پانا(شتون=س_تاریخ)
        خود.ممکنہ_تاریخیں = (خود.دن[0], خود.دن[1][-1] + خود.دن[0])

    def _اعداد_پیدا_کرنا(خود, سے, تک, **kwargs):
        شتونیں = [خود.نام_شتونیں[x] for x in خود.دن_ستون]

        اعداد = پاندس.DataFrame(خود.اعداد.اعداد_پانا(شتونیں=شتونیں), columns=شتونیں)

        for م, ش in خود.تبادلوں.items():
            اعداد[م] = اعداد[م] * ش

        return اعداد  # para hacer: سے, تک,


class مہنہ_مشا(ذریعہ):

    def __init__(خود, مسل, س_اعداد, س_مہینہ, س_سال, تبادلوں, combin=None):

        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        خود.نام_ستونیں = س_اعداد
        خود.تبادلوں = تبادلوں
        خود.combin = combin

        خود.اعداد = اعداد_و_شمار_بنانا(مسل)
        for ن in س_اعداد.values():
            if ن not in خود.اعداد.نام_ستونیں:
                raise ValueError('')

        خود.سال = خود.اعداد.اعداد_پانا(شتونیں=س_سال, prec_dec=0)[0]
        خود.مہینہ = خود.اعداد.اعداد_پانا(شتونیں=س_مہینہ, prec_dec=0)[0]
        سال_کم = خود.سال.min()
        مہینہ_کم = خود.مہینہ[نمپی.where(خود.سال == سال_کم)].min()
        سال_زیادہ = خود.سال.max()
        مہینہ_زیادہ = خود.مہینہ[نمپی.where(خود.سال == سال_زیادہ)].max()
        تاریخ_کم = ft.date(year=سال_کم, month=مہینہ_کم, day=1)
        تاریخ_زیادہ = ft.date(year=سال_زیادہ, month=مہینہ_زیادہ, day=calendar.monthrange(سال_زیادہ, مہینہ_زیادہ)[1])

        خود.ممکنہ_تاریخیں = (تاریخ_کم, تاریخ_زیادہ)

    def _اعداد_پیدا_کرنا(خود, سے, تک, **kwargs):

        ف_سوتون = [x for x in خود.دن_ستون if x in خود.نام_ستونیں]

        ف_سوتون_باہر = [خود.نام_ستونیں[x] for x in ف_سوتون]

        اعداد_مہینہ = خود.اعداد.اعداد_پانا(شتونیں=ف_سوتون_باہر)

        ش_دن = (خود.ممکنہ_تاریخیں[1] - خود.ممکنہ_تاریخیں[0]).days + 1

        اعداد_دن = پاندس.DataFrame(index=پاندس.date_range(*خود.ممکنہ_تاریخیں), columns=ف_سوتون)

        دن_مہینا_میں = [calendar.monthrange(سال, م)[1] for م, سال in zip(خود.مہینہ, خود.سال)]

        for ش, س in enumerate(ف_سوتون_باہر):
            if س in ['بارش']:
                اعداد_مہینہ[ش, :] = اعداد_مہینہ[ش] / دن_مہینا_میں

        تاریخ = خود.ممکنہ_تاریخیں[0]
        سال_شروع = تاریخ.year
        مہینہ_سروع = تاریخ.month
        for _ in range(ش_دن):
            # اداد میں ھر دن کہ لئے۔۔۔
            ش_مہینہ = (تاریخ.year - سال_شروع) * 12 + (تاریخ.month - مہینہ_سروع)
            اعداد_دن.loc[تاریخ] = اعداد_مہینہ[:, ش_مہینہ]

            for م in اعداد_دن:
                if خود.تریقہ_جمع[م] == 'رقم':
                    اعداد_دن.loc[تاریخ][م] = اعداد_دن.loc[تاریخ][م] / calendar.monthrange(تاریخ.year, تاریخ.month)[1]

            تاریخ += ft.timedelta(days=1)

        for م, ش in خود.تبادلوں.items():
            اعداد_دن[م] = اعداد_دن[م] * ش

        return اعداد_دن  # para hacer: سے, تک,


class سال_مشا(ذریعہ):

    def __init__(خود, مسل, س_اعداد, س_سال, تبادلوں):

        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        خود.نام_شتونیں = س_اعداد
        خود.تبادلوں = تبادلوں

        خود.اعداد = اعداد_و_شمار_بنانا(مسل)
        for ن in س_اعداد.values():
            if ن not in خود.اعداد.نام_ستونیں:
                raise ValueError('')

        خود.سال = خود.اعداد.اعداد_پانا(شتونیں=س_سال)[0]

        خود.ممکنہ_تاریخیں = (ft.datetime(year=min(خود.سال), month=1, day=1),
                             ft.datetime(year=max(خود.سال), month=1, day=1))

    def _اعداد_پیدا_کرنا(خود, سے, تک, **kwargs):

        ف_ستون = [خود.نام_شتونیں[x] for x in خود.دن_ستون]

        اعداد_سال = خود.اعداد.اعداد_پانا(شتونیں=ف_ستون)

        ش_دن = (خود.ممکنہ_تاریخیں[1] - خود.ممکنہ_تاریخیں[0]).days

        اعداد_دن = پاندس.DataFrame(index=پاندس.date_range(*خود.ممکنہ_تاریخیں), columns=ف_ستون)
        تاریخ = خود.ممکنہ_تاریخیں[0]
        سال_شروع = خود.سال.min()

        سال_میں_دن_شمار = [366 if calendar.isleap(x) else 365 for x in خود.سال]

        for ش, س in enumerate(ف_ستون):
            if س in ['بارش']:
                اعداد_سال[ش, :] = اعداد_سال[ش] / سال_میں_دن_شمار

        for _ in range(ش_دن):
            ش_سال = تاریخ.year - سال_شروع
            اعداد_دن.loc[تاریخ] = اعداد_سال[:, ش_سال]

            for م in اعداد_دن:
                if خود.تریقہ_جمع[م] == 'رقم':
                    اعداد_دن.loc[تاریخ][م] = اعداد_دن.loc[تاریخ][م] / calendar.monthrange(تاریخ.year, تاریخ.month)[1]

            تاریخ += ft.timedelta(1)

        for م, ش in خود.تبادلوں.items():
            اعداد_دن[م] = اعداد_دن[م] * ش

        return اعداد_دن  # para hacer: سے, تک,


def اعداد_و_شمار_بنانا(مسل):
    """

    :param مسل:
    :type مسل: str
    :return:
    :rtype: اعداد_و_شمار
    """
    ext = os.path.splitext(مسل)[1]
    if ext == '.txt' or ext == '.csv':
        return BDtexto(مسل)
    elif ext == '.sql':
        return BDsql(مسل)
    else:
        raise ValueError


class اعداد_و_شمار(object):
    """
    Una superclase para lectores de bases de datos.
    """

    def __init__(خود, مسل):
        خود.مسل = مسل

        if not os.path.isfile(مسل):
            raise FileNotFoundError

        خود.n_obs = خود.calc_n_obs()
        خود.نام_ستونیں = خود.نام_ستونیں_پانا()

    def نام_ستونیں_پانا(خود):
        """

        :return:
        :rtype: list[str]
        """
        raise NotImplementedError

    def اعداد_پانا(خود, شتونیں, prec_dec=None):
        """

        :param شتونیں:
        :type شتونیں: list[str] | str
        :param prec_dec:
        :type prec_dec: int
        :return:
        :rtype: np.ndarray
        """
        raise NotImplementedError

    def اعداد_متن_پانا(خود, شتونیں):
        """

        :param شتونیں:
        :type شتونیں: list[str] | str
        :return:
        :rtype: list
        """
        raise NotImplementedError

    def تاریخیں_پانا(خود, شتون):
        """

        :param شتون:
        :type شتون: str
        :return:
        :rtype: (ft.date, np.ndarray)
        """

        # Sacar la lista de fechas en formato texto
        fechas_tx = خود.اعداد_متن_پانا(شتونیں=شتون)

        # Procesar la lista de fechas
        fch_inic_datos, v_núm = خود.تاریخیں_پڑنا(lista_fechas=fechas_tx)

        # Devolver información importante
        return fch_inic_datos, v_núm

    def calc_n_obs(خود):
        """

        :return:
        :rtype: int
        """
        raise NotImplementedError

    @staticmethod
    def تاریخیں_پڑنا(lista_fechas):
        """
        Esta función toma una lista de datos de fecha en formato de texto y detecta 1) la primera fecha de la lista,
        y 2) la posición relativa de cada fecha a esta.

        :param lista_fechas: Una lista con las fechas en formato de texto
        :type lista_fechas: list

        :return: Un tuple de la primera fecha y del vector numpy de la posición de cada fecha relativa a la primera.
        :rtype: (ft.date, np.ndarray)

        """

        # Una lista de lso formatos de fecha posibles. Esta función intentará de leer los datos de fechas con cada
        # formato en esta lista y, si encuentra un que funciona, parará allí.
        separadores = ['-', '/', ' ', '.']

        f = ['%d{0}%m{0}%y', '%m{0}%d{0}%y', '%d{0}%m{0}%Y', '%m{0}%d{0}%Y',
             '%d{0}%b{0}%y', '%m{0}%b{0}%y', '%d{0}%b{0}%Y', '%b{0}%d{0}%Y',
             '%d{0}%B{0}%y', '%m{0}%B{0}%y', '%d{0}%B{0}%Y', '%m{0}%B{0}%Y',
             '%y{0}%m{0}%d', '%y{0}%d{0}%m', '%Y{0}%m{0}%d', '%Y{0}%d{0}%m',
             '%y{0}%b{0}%d', '%y{0}%d{0}%b', '%Y{0}%b{0}%d', '%Y{0}%d{0}%b',
             '%y{0}%B{0}%d', '%y{0}%d{0}%B', '%Y{0}%B{0}%d', '%Y{0}%d{0}%B']

        formatos_posibles = [x.format(s) for s in separadores for x in f]

        # Primero, si los datos de fechas están en formato simplemente numérico...
        if all([x.isdigit() for x in lista_fechas]):

            # Entonces, no conocemos la fecha inicial
            fecha_inic_datos = None

            # Convertir a vector Numpy
            vec_fch_núm = نمپی.array(lista_fechas, dtype=int)

        else:
            # Sino, intentar de leer el formato de fecha
            fechas = None

            # Intentar con cada formato en la lista de formatos posibles
            for formato in formatos_posibles:

                try:
                    # Intentar de convertir todas las fechas a objetos ft.datetime
                    fechas = [ft.datetime.strptime(x, formato).date() for x in lista_fechas]

                    # Si funcionó, parar aquí
                    break

                except ValueError:
                    # Si no funcionó, intentar el próximo formato
                    continue

            # Si todavía no lo hemos logrado, tenemos un problema.
            if fechas is None:
                raise ValueError(
                    'No puedo leer los datos de fechas. ¿Mejor le eches un vistazo a tu base de datos?')

            else:
                # Pero si está bien, ya tenemos que encontrar la primera fecha y calcular la posición relativa de las
                # otras con referencia en esta.

                # La primera fecha de la base de datos. Este paso se queda un poco lento, así que para largas bases de
                # datos podría ser útil suponer que la primera fila también contiene la primera fecha.
                fecha_inic_datos = min(fechas)

                # Si tenemos prisa, mejor lo hagamos así:
                # fecha_inic_datos = min(fechas[0], fechas[-1])

                # La posición relativa de todas las fechas a esta
                lista_fechas = [(x - fecha_inic_datos).days for x in fechas]

                # Convertir a vector Numpy
                vec_fch_núm = نمپی.array(lista_fechas, dtype=int)

        return fecha_inic_datos, vec_fch_núm


class BDtexto(اعداد_و_شمار):
    """
    Una clase para leer bases de datos en formato texto delimitado por comas (.csv).
    """

    def calc_n_obs(خود):
        """

        :rtype: int
        """
        with open(خود.مسل, encoding='UTF8') as d:
            n_filas = sum(1 for f in d if len(f)) - 1  # Sustrayemos la primera fila

        return n_filas

    def اعداد_پانا(خود, شتونیں, prec_dec=None):
        """

        :param شتونیں:
        :type شتونیں: str | list[str]
        :param prec_dec:
        :type prec_dec: int
        :return:
        :rtype: np.ndarray
        """
        if not isinstance(شتونیں, list):
            شتونیں = [شتونیں]

        m_datos = نمپی.empty((len(شتونیں), خود.n_obs))

        with open(خود.مسل, encoding='UTF8') as d:
            lector = csv.DictReader(d)
            for n_f, f in enumerate(lector):
                m_datos[:, n_f] = [متن_سے_شمار(f[c]) if f[c] != '' else نمپی.nan for c in شتونیں]

        if prec_dec is not None:
            if prec_dec == 0:
                m_datos = m_datos.astype(int)
            else:
                m_datos.round(prec_dec, out=m_datos)

        return m_datos

    def اعداد_متن_پانا(خود, شتونیں):
        """

        :param شتونیں:
        :type شتونیں: list[str] | str
        :return:
        :rtype: list
        """
        if not isinstance(شتونیں, list):
            شتونیں = [شتونیں]

        l_datos = [[''] * خود.n_obs] * len(شتونیں)

        with open(خود.مسل, encoding='UTF8') as d:
            lector = csv.DictReader(d)
            for n_f, f in enumerate(lector):
                for i_c, c in enumerate(شتونیں):
                    l_datos[i_c][n_f] = f[c]

        if len(شتونیں) == 1:
            l_datos = l_datos[0]

        return l_datos

    def نام_ستونیں_پانا(خود):
        """

        :return:
        :rtype: list[str]
        """

        with open(خود.مسل, encoding='UTF8') as d:
            lector = csv.reader(d)

            nombres_cols = next(lector)

        return nombres_cols


class BDsql(اعداد_و_شمار):
    """
    Una clase para leer bases de datos en formato SQL.
    """

    def calc_n_obs(خود):
        """

        :return:
        :rtype:
        """
        pass

    def نام_ستونیں_پانا(خود):
        """

        :return:
        :rtype: list[str]
        """
        pass

    def اعداد_پانا(خود, شتونیں, prec_dec=None):
        """

        :param شتونیں:
        :type شتونیں:
        :param prec_dec:
        :type prec_dec:
        :return:
        :rtype:
        """
        pass

    def اعداد_متن_پانا(خود, شتونیں):
        """

        :param شتونیں:
        :type شتونیں:
        :return:
        :rtype:
        """
        pass
