from taqdir.Fuentes.ذریعہ import ذریعہ
import os
import numpy as np
import csv
import pandas as pd
import datetime as ft

class ObsDiario(ذریعہ):

    def __init__(símismo, archivo, c_fecha, cols_datos):

        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        símismo.nombres_cols = cols_datos

        símismo.اعداد = gen_bd(archivo)
        símismo.دن = símismo.اعداد.obt_días(col=c_fecha)
        símismo.rango_potencial = (símismo.دن[0], símismo.دن[1][-1] + símismo.دن[0])

    def _اعداد_پیدا_کرنا(símismo, سے, تک, **kwargs):

        v_cols = [símismo.nombres_cols[x] for x in símismo.cols_día]

        اعداد = pd.DataFrame(símismo.اعداد.obt_datos(cols=v_cols), columns=v_cols)

        return اعداد


class ObsMensuales(ذریعہ):

    def __init__(símismo, archivo, cols_datos, c_meses, c_años):

        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        símismo.nombres_cols = cols_datos

        símismo.اعداد = gen_bd(archivo)
        سال = símismo.اعداد.obt_datos(cols=c_años)
        مہینہ = símismo.اعداد.obt_datos(cols=c_meses)
        fecha_mín =
        fecha_máx =

        símismo.rango_potencial = (fecha_mín, fecha_máx)

    def _اعداد_پیدا_کرنا(símismo, سے, تک, **kwargs):
        v_cols = [símismo.nombres_cols[x] for x in símismo.cols_día]

        اعداد_مہینہ = símismo.اعداد.obt_datos(cols=v_cols)

        ش_دن = (símismo.rango_potencial[1] - símismo.rango_potencial[0]).days

        datos_diarios = np.zeros(len(v_cols), ش_دن)

        تاریخ = símismo.rango_potencial[0]
        سال_شروع = تاریخ.year
        for د in range(ش_دن):
            n_mes = (تاریخ.year - سال_شروع) * 12 + تاریخ.month - 1
            datos_diarios[:, د] = اعداد_مہینہ[n_mes]
            د += 1

        اعداد_دن = pd.DataFrame(datos_diarios, columns=v_cols)

        return اعداد_دن


class ObsAnuales(ذریعہ):

    def __init__(símismo, archivo, cols_datos, c_años):

        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        símismo.nombres_cols = cols_datos

        símismo.اعداد = gen_bd(archivo)
        símismo.سال = símismo.اعداد.obt_datos(cols=c_años)

        símismo.rango_potencial = (ft.datetime(year=min(símismo.سال), month=1, day=1),
                                   ft.datetime(year=max(símismo.سال), month=1, day=1))

    def _اعداد_پیدا_کرنا(símismo, سے, تک, **kwargs):

        v_cols = [símismo.nombres_cols[x] for x in símismo.cols_día]

        اعداد_سال = símismo.اعداد.obt_datos(cols=v_cols)

        ش_دن = (símismo.rango_potencial[1] - símismo.rango_potencial[0]).days
        
        datos_diarios = np.zeros(len(v_cols), ش_دن)
        تاریخ = símismo.rango_potencial[0]
        سال_شروع = símismo.سال.min()
        for د in range(ش_دن):
            n_mes = (تاریخ.year - سال_شروع) * 12 + تاریخ.month - 1
            datos_diarios[:, د] = اعداد_مہینہ[n_mes]
            د += 1
        
        اعداد_دن = pd.DataFrame(datos_diarios, columns=v_cols)

        return اعداد_دن


def gen_bd(archivo):
    """

    :param archivo:
    :type archivo: str
    :return:
    :rtype: BD
    """
    ext = os.path.splitext(archivo)[1]
    if ext == '.txt' or ext == '.csv':
        return BDtexto(archivo)
    elif ext == '.sql':
        return BDsql(archivo)
    else:
        raise ValueError


class BD(object):
    """
    Una superclase para lectores de bases de اعداد_دن.
    """

    def __init__(símismo, archivo):
        símismo.archivo = archivo

        if not os.path.isfile(archivo):
            raise FileNotFoundError

        símismo.n_obs = símismo.calc_n_obs()

    def sacar_cols(símismo):
        """

        :return:
        :rtype: list[str]
        """
        raise NotImplementedError

    def obt_datos(símismo, cols):
        """

        :param cols:
        :type cols: list[str] | str
        :return:
        :rtype: np.ndarray
        """
        raise NotImplementedError

    def obt_datos_tx(símismo, cols):
        """

        :param cols:
        :type cols: list[str] | str
        :return:
        :rtype: list
        """
        raise NotImplementedError

    def obt_días(símismo, col):
        """

        :param col:
        :type col: str
        :return:
        :rtype: (ft.date, np.ndarray)
        """

        # Sacar la lista de fechas en formato texto
        fechas_tx = símismo.obt_datos_tx(cols=col)

        # Procesar la lista de fechas
        fch_inic_datos, v_núm = símismo.leer_fechas(lista_fechas=fechas_tx)

        # Devolver información importante
        return fch_inic_datos, v_núm

    def calc_n_obs(símismo):
        """

        :return:
        :rtype: int
        """
        raise NotImplementedError

    @staticmethod
    def leer_fechas(lista_fechas):
        """
        Esta función toma una lista de اعداد_دن de fecha en formato de texto y detecta 1) la primera fecha de la lista,
        y 2) la posición relativa de cada fecha a esta.

        :param lista_fechas: Una lista con las fechas en formato de texto
        :type lista_fechas: list

        :return: Un tuple de la primera fecha y del vector numpy de la posición de cada fecha relativa a la primera.
        :rtype: (ft.date, np.ndarray)

        """

        # Una lista de lso formatos de fecha posibles. Esta función intentará de leer los اعداد_دن de fechas con cada
        # formato en esta lista y, si encuentra un que funciona, parará allí.
        separadores = ['-', '/', ' ', '.']

        f = ['%d{0}%m{0}%y', '%m{0}%d{0}%y', '%d{0}%m{0}%Y', '%m{0}%d{0}%Y',
             '%d{0}%b{0}%y', '%m{0}%b{0}%y', '%d{0}%b{0}%Y', '%b{0}%d{0}%Y',
             '%d{0}%B{0}%y', '%m{0}%B{0}%y', '%d{0}%B{0}%Y', '%m{0}%B{0}%Y',
             '%y{0}%m{0}%d', '%y{0}%d{0}%m', '%Y{0}%m{0}%d', '%Y{0}%d{0}%m',
             '%y{0}%b{0}%d', '%y{0}%d{0}%b', '%Y{0}%b{0}%d', '%Y{0}%d{0}%b',
             '%y{0}%B{0}%d', '%y{0}%d{0}%B', '%Y{0}%B{0}%d', '%Y{0}%d{0}%B']

        formatos_posibles = [x.format(s) for s in separadores for x in f]

        # Primero, si los اعداد_دن de fechas están en formato simplemente numérico...
        if all([x.isdigit() for x in lista_fechas]):

            # Entonces, no conocemos la fecha inicial
            fecha_inic_datos = None

            # Convertir a vector Numpy
            vec_fch_núm = np.array(lista_fechas, dtype=int)

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
                raise ValueError('No puedo leer los اعداد_دن de fechas. ¿Mejor le eches un vistazo a tu base de اعداد_دن?')

            else:
                # Pero si está bien, ya tenemos que encontrar la primera fecha y calcular la posición relativa de las
                # otras con referencia en esta.

                # La primera fecha de la base de اعداد_دن. Este paso se queda un poco lento, así que para largas bases de
                # اعداد_دن podría ser útil suponer que la primera fila también contiene la primera fecha.
                fecha_inic_datos = min(fechas)

                # Si tenemos prisa, mejor lo hagamos así:
                # fecha_inic_datos = min(fechas[0], fechas[-1])

                # La posición relativa de todas las fechas a esta
                lista_fechas = [(x - fecha_inic_datos).days for x in fechas]

                # Convertir a vector Numpy
                vec_fch_núm = np.array(lista_fechas, dtype=int)

        return fecha_inic_datos, vec_fch_núm


class BDtexto(BD):
    """
    Una clase para leer bases de اعداد_دن en formato texto delimitado por comas (.csv).
    """

    def calc_n_obs(símismo):
        """

        :rtype: int
        """
        with open(símismo.archivo, encoding='UTF8') as d:
            n_filas = sum(1 for f in d if len(f)) - 1  # Sustrayemos la primera fila

        return n_filas

    def obt_datos(símismo, cols):
        """

        :param cols:
        :type cols: str | list[str]
        :return:
        :rtype: np.ndarray
        """
        if not isinstance(cols, list):
            cols = [cols]

        m_datos = np.empty((len(cols), símismo.n_obs))

        with open(símismo.archivo, encoding='UTF8') as d:
            lector = csv.DictReader(d)
            for n_f, f in enumerate(lector):
                m_datos[:, n_f] = [float(f[c]) if f[c] != '' else np.nan for c in cols]

        if len(cols) == 1:
            m_datos = m_datos[0]

        return m_datos

    def obt_datos_tx(símismo, cols):
        """

        :param cols:
        :type cols: list[str] | str
        :return:
        :rtype: list
        """
        if not isinstance(cols, list):
            cols = [cols]

        l_datos = [['']*símismo.n_obs]*len(cols)

        with open(símismo.archivo, encoding='UTF8') as d:
            lector = csv.DictReader(d)
            for n_f, f in enumerate(lector):
                for i_c, c in enumerate(cols):
                    l_datos[i_c][n_f] = f[c]

        if len(cols) == 1:
            l_datos = l_datos[0]

        return l_datos

    def sacar_cols(símismo):
        """

        :return:
        :rtype: list[str]
        """

        with open(símismo.archivo, encoding='UTF8') as d:
            lector = csv.reader(d)

            nombres_cols = next(lector)

        return nombres_cols


class BDsql(BD):
    """
    Una clase para leer bases de اعداد_دن en formato SQL.
    """

    def calc_n_obs(símismo):
        """

        :return:
        :rtype:
        """
        pass

    def obt_datos(símismo, cols):
        """

        :param cols:
        :type cols:
        :return:
        :rtype:
        """
        pass

    def obt_datos_tx(símismo, cols):
        """

        :param cols:
        :type cols:
        :return:
        :rtype:
        """
        pass

    def sacar_cols(símismo):
        """

        :return:
        :rtype:
        """
        pass
