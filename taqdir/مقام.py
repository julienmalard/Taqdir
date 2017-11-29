from warnings import warn as avisar

import pandas as pd

from taqdir.ذرائع.ذریعہ import ذریعہ
from taqdir.ذرائع.مشاہدات import دن_مشا, مہنہ_مشا, سال_مشا
from taqdir.ذرائع.مرکسم٥ import مرکسم٥
from taqdir.ذرائع.مرکسم٣ import مرکسم٣


class مقام(ذریعہ):

    def __init__(خود, چوڑائی, طول, بلندی):
        super().__init__(چوڑائی=چوڑائی, طول=طول, بلندی=بلندی)

        خود.مشاہدات = []

    def مشاہدہ_کرنا(خود, مشاہد):
        """

        :param مشاہد:
        :type مشاہد: ObsDiario | ObsMensuales | سال_مشا
        :return:
        :rtype:
        """

        خود.مشاہدات.append(مشاہد)

    def borrar_obs(خود):
        خود.مشاہدات.clear()

    def اعداد_تیاری(خود, پہلہ_تاریخ, آخرا_تاریخ, rcp, n_rep=1,
                    ترجیحات=None, lím_prefs=False, usar_caché=True, regenerar=True):

        خود.اعداد_دن = pd.DataFrame(index=pd.date_range(پہلہ_تاریخ, آخرا_تاریخ),
                                    columns=خود.cols_día)

        تاریخ_چاہئے = (پہلہ_تاریخ, آخرا_تاریخ)
        لاپتہ_تاریخ = [تاریخ_چاہئے]

        prefs_auto = [مرکسم٥, مرکسم٣]

        ل_ذریعہ = {
            'مرکسم٥': مرکسم٥,
            'مرکسم٣': مرکسم٣,
            'مشاہدات': خود.مشاہدات
        }

        if ترجیحات is None:
            ترجیحات = prefs_auto

        if not lím_prefs:
            for ت in prefs_auto:
                if ت not in ترجیحات:
                    ترجیحات.append(ت)

        for ب, ت in enumerate(ترجیحات):
            if isinstance(ت, str):
                ترجیحات[ب] = ل_ذریعہ[ت]

        for م in خود.مشاہدات:
            if م not in ترجیحات:
                ترجیحات.insert(0, م)

        for ذرع in ترجیحات:

            for تاریخ in لاپتہ_تاریخ.copy():
                fechas_f = intersec_rangos(تاریخ, ذرع.rango_potencial)
                لاپتہ_تاریخ = act_l_rangos(l_rangos=لاپتہ_تاریخ, rango_sust=fechas_f)

                اعداد = ذرع.اعداد_پانا(*fechas_f, rcp=rcp, n_rep=n_rep, usar_caché=usar_caché, regenerar=regenerar)

                خود._اعداد_جوڈنا(اعداد)

            if len(لاپتہ_تاریخ) == 0:
                break

        if len(لاپتہ_تاریخ):
            avisar('Faltan اعداد_دن para las fechas siguientes:\n\t{}'.format(لاپتہ_تاریخ))

        return خود.اعداد_دن

    def _اعداد_پیدا_کرنا(خود, سے, تک, usar_caché):
        pass

    def _اعداد_جوڈنا(خود, datos):
        خود.اعداد_دن.update(datos)

    def cargar_datos(خود, archivo, cols_datos, fecha, mes, año):
        خود.اعداد_دن = pd.read_csv(archivo, index_col='UID')

    def guardar_datos(خود, مسل=None):
        if مسل is None:
            raise ValueError

        خود.اعداد_دن.to_csv(مسل, sep='\t', encoding='utf-8')


def intersec_rangos(rango1, rango2):
    """

    :param rango1:
    :type rango1:
    :param rango2:
    :type rango2:
    :return:
    :rtype: tuple
    """
    mín = max(rango1[0], rango2[0])
    máx = min(rango1[1], rango2[1])
    if mín > máx:
        rango = None
    else:
        rango = (mín, máx)

    return rango


def dif_rangos(rango1, rango2):
    """
    Sustrae rango2 de rango1.

    :param rango1:
    :type rango1: tuple
    :param rango2:
    :type rango2: tuple
    :return:
    :rtype: tuple | list[tuple] | None
    """

    mín1, máx1 = rango1
    mín2, máx2 = rango2

    # Rango 2 debe ser contenido por rango 1
    if (máx1 < máx2) or (mín1 > mín2):
        raise ValueError

    if rango1 == rango2:
        return
    else:
        if mín1 == mín2:
            return máx2, máx1
        else:
            if máx1 == máx2:
                return mín1, mín2
            else:
                return [(mín1, mín2), (máx2, máx1)]


def act_l_rangos(l_rangos, rango_sust):
    """

    :param l_rangos:
    :type l_rangos:  list[tuple]
    :param rango_sust:
    :type rango_sust: tuple
    :return:
    :rtype:
    """

    l_final = []
    for i, r_i in enumerate(l_rangos.copy()):
        u = intersec_rangos(r_i, rango_sust)
        if u is None:
            l_final.append(u)
        else:

            r_nuevo = dif_rangos(r_i, u)

            if r_nuevo is None:
                pass
            elif isinstance(r_nuevo, tuple):
                l_final.append(r_nuevo)
            elif isinstance(r_nuevo, list):
                l_final += r_nuevo

    return l_final
