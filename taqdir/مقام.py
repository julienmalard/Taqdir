from warnings import warn as avisar

import pandas as pd

from taqdir.Fuentes.Fuente import Fuente
from taqdir.Fuentes.مشاہدات import ObsDiario
from taqdir.Fuentes.مرکسم٥ import مرکسم٥
from taqdir.Fuentes.مرکسم٣ import مرکسم٣


class مقام(Fuente):
    def __init__(símismo, چوڑائی, طول, بلندی):
        super().__init__(چوڑائی=چوڑائی, طول=طول, بلندی=بلندی)

        símismo.مشاہدات = []

    def مشاہدہ_کرنا(símismo, مشاہد):
        """

        :param مشاہد:
        :type مشاہد: ObsDiario
        :return:
        :rtype:
        """

        símismo.مشاہدات.append(مشاہد)

    def borrar_obs(símismo):
        símismo.مشاہدات.clear()

    def prep_datos(símismo, fecha_inic, fecha_final, rcp, n_rep=1,
                   prefs=None, lím_prefs=False, usar_caché=True, regenerar=True):

        símismo.datos = pd.DataFrame(index=pd.date_range(fecha_inic, fecha_final),
                                     columns=símismo.cols_día)

        fechas_interés = (fecha_inic, fecha_final)
        fechas_faltan = [fechas_interés]

        prefs_auto = [مرکسم٥, مرکسم٣]

        d_fuentes = {
            'مرکسم٥': مرکسم٥,
            'مرکسم٣': مرکسم٣,
            'مشاہدات': símismo.مشاہدات
        }

        if prefs is None:
            prefs = prefs_auto

        if not lím_prefs:
            for p in prefs_auto:
                if p not in prefs:
                    prefs.append(p)

        for i, p in enumerate(prefs):
            if isinstance(p, str):
                prefs[i] = d_fuentes[p]

        for o in símismo.مشاہدات:
            if o not in prefs:
                prefs.insert(0, o)

        for fuente in prefs:

            for fchs in fechas_faltan.copy():
                fechas_f = intersec_rangos(fchs, fuente.rango_potencial)
                fechas_faltan = act_l_rangos(l_rangos=fechas_faltan, rango_sust=fechas_f)

                datos = fuente.obt_datos(*fechas_f, rcp=rcp, n_rep=n_rep, usar_caché=usar_caché, regenerar=regenerar)

                símismo._agregar_datos(datos)

            if len(fechas_faltan) == 0:
                break

        if len(fechas_faltan):
            avisar('Faltan datos para las fechas siguientes:\n\t{}'.format(fechas_faltan))

        return símismo.datos

    def _agregar_datos(símismo, datos):
        símismo.datos.update(datos)

    def cargar_datos(símismo, archivo, cols_datos, fecha, mes, año):
        símismo.datos = pd.read_csv(archivo, index_col='UID')

    def guardar_datos(símismo, archivo=None):
        if archivo is None:
            raise ValueError

        símismo.datos.to_csv(archivo, sep='\t', encoding='utf-8')


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
