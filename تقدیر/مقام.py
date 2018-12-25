from datetime import date as تاریخ, timedelta
from warnings import warn as avisar

import pandas as pd
from تقدیر.ذرائع.ذریعہ import ذریعہ
from تقدیر.ذرائع.مرکسم٥ import مرکسم٥
from تقدیر.شمار import متن_سے_شمار


class مقام(ذریعہ):

    def __init__(خود, چوڑائی, طول, بلندی):
        super().__init__(چوڑائی=چوڑائی, طول=طول, بلندی=بلندی)

        خود.مشاہدات = []

    def مشاہدہ_کرنا(خود, مشاہد):
        """

        :param مشاہد:
        :type مشاہد: دن_مشا | مہنہ_مشا | سال_مشا
        :return:
        :rtype:
        """

        خود.مشاہدات.append(مشاہد)

    def مشاہدات_ھٹانا(خود):
        خود.مشاہدات.clear()

    def اعداد_تیاری(خود, پہلہ_تاریخ, آخرا_تاریخ, ر_ح_را, ش_ترکار=1,
                    ترجیحات=None, ترجیحات_محدود=False, پہلہ_ہونےولے_اشتمال=True, دوبارہ_پیدا=True):

        خود.اعداد_دن = pd.DataFrame(index=pd.date_range(پہلہ_تاریخ, آخرا_تاریخ),
                                    columns=خود.دن_ستون)
        if isinstance(پہلہ_تاریخ, str):
            پہلہ_تاریخ = متن_سے_شمار(پہلہ_تاریخ)
        if isinstance(آخرا_تاریخ, str):
            آخرا_تاریخ = متن_سے_شمار(آخرا_تاریخ)
        تاریخ_چاہئے = [پہلہ_تاریخ, آخرا_تاریخ]
        for ش, تا in enumerate(تاریخ_چاہئے):
            if isinstance(تا, int):
                تاریخ_چاہئے[ش] = تاریخ(year=تا, month=1, day=1)
        لاپتہ_تاریخ = [تاریخ_چاہئے]

        ترجیحات_خود = [مرکسم٥]

        ل_ذریعہ = {
            'مرکسم٥': مرکسم٥,
        }

        if ترجیحات is None:
            ترجیحات = ترجیحات_خود

        if not ترجیحات_محدود:
            for ت in ترجیحات_خود:
                if ت not in ترجیحات and ت not in [type(x) for x in ترجیحات]:
                    ترجیحات.append(ت)

        for ب, ت in enumerate(ترجیحات):
            if isinstance(ت, str):
                ترجیحات[ب] = ل_ذریعہ[ت]

        for ب, ت in enumerate(ترجیحات):
            if isinstance(ت, type):
                ترجیحات[ب] = ت(چوڑائی=خود.چوڑائی, طول=خود.طول, بلندی=خود.بلندی)

        for م in خود.مشاہدات:
            if م not in ترجیحات:
                ترجیحات.insert(0, م)

        for ذرع in ترجیحات:

            for تا in لاپتہ_تاریخ.copy():
                تاریخ_ذرائع = intersec_rangos(تا, ذرع.ممکنہ_تاریخیں)
                لاپتہ_تاریخ = act_l_rangos(l_rangos=لاپتہ_تاریخ, rango_sust=تاریخ_ذرائع)

                if (تاریخ_ذرائع[0] - تاریخ_ذرائع[1]).days != 0:
                    اعداد = ذرع.اعداد_پانا(*تاریخ_ذرائع, ر_ح_را=ر_ح_را, ش_ترکار=ش_ترکار, usar_caché=پہلہ_ہونےولے_اشتمال,
                                           دوبارہ_پیدا=دوبارہ_پیدا)

                    خود._اعداد_جوڈنا(اعداد)

            if len(لاپتہ_تاریخ) == 0:
                break

        if len(لاپتہ_تاریخ):
            avisar('ان سالوں کے لئے اعداد مای نہیں-:\n\t{}'.format(لاپتہ_تاریخ))

        return خود.اعداد_دن

    def _اعداد_پیدا_کرنا(خود, سے, تک, ر_ح_را, ش_ترکار, پہلہ_ہونےولے_اشتمال):
        pass

    def _اعداد_جوڈنا(خود, اعداد):
        خود.اعداد_دن.update(اعداد)

    def اعداد_پڑھنا(خود, مسل):
        خود.اعداد_دن = pd.read_csv(مسل, index_col='UID')

    def اعداد_رگھنا(خود, مسل=None):
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
            return máx2 + timedelta(days=1), máx1
        else:
            if máx1 == máx2:
                return mín1, mín2
            else:
                return [(mín1, mín2), (máx2 + timedelta(days=1), máx1)]


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

            r_nuevo = dif_rangos(tuple(r_i), u)

            if r_nuevo is None:
                pass
            elif isinstance(r_nuevo, tuple):
                l_final.append(r_nuevo)
            elif isinstance(r_nuevo, list):
                l_final += r_nuevo

    return l_final
