import calendar
from taqdir.ذرائع.ذریعہ import ذریعہ
import os
import re
import numpy as np
import csv
import pandas as pd
import datetime as ft


class دن_مشا(ذریعہ):

    def __init__(خود, archivo, c_fecha, cols_datos):
        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        خود.nombres_cols = cols_datos

        خود.اعداد = gen_bd(archivo)
        خود.دن = خود.اعداد.obt_días(col=c_fecha)
        خود.rango_potencial = (خود.دن[0], خود.دن[1][-1] + خود.دن[0])

    def _اعداد_پیدا_کرنا(خود, سے, تک, **kwargs):
        v_cols = [خود.nombres_cols[x] for x in خود.cols_día]

        اعداد = pd.DataFrame(خود.اعداد.obt_datos(cols=v_cols), columns=v_cols)

        return اعداد


class مہنہ_مشا(ذریعہ):

    def __init__(خود, archivo, cols_datos, c_meses, c_años):

        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        خود.nombres_cols = cols_datos

        خود.اعداد = gen_bd(archivo)
        خود.سال = خود.اعداد.obt_datos(cols=c_años, prec_dec=0)
        خود.مہینہ = خود.اعداد.obt_datos(cols=c_meses, prec_dec=0)
        año_mín = خود.سال.min()
        mes_mín = خود.مہینہ[np.where(خود.سال == año_mín)].min()
        año_máx = خود.سال.max()
        mes_máx = خود.مہینہ[np.where(خود.سال == año_máx)].max()
        fecha_mín = ft.date(year=año_mín, month=mes_mín, day=1)
        fecha_máx = ft.date(year=año_máx, month=mes_máx, day=calendar.monthrange(año_máx, mes_máx)[1])

        خود.rango_potencial = (fecha_mín, fecha_máx)

    def _اعداد_پیدا_کرنا(خود, سے, تک, **kwargs):
        v_cols = [x for x in خود.cols_día if x in خود.nombres_cols]
        v_cols_extrn = [خود.nombres_cols[x] for x in v_cols]

        اعداد_مہینہ = خود.اعداد.obt_datos(cols=v_cols_extrn)

        ش_دن = (خود.rango_potencial[1] - خود.rango_potencial[0]).days + 1

        اعداد_دن = pd.DataFrame(index=pd.date_range(*خود.rango_potencial), columns=v_cols)

        دن_مہینا_میں = [calendar.monthrange(سا, م)[1] for م, سا in zip(خود.مہینہ, خود.سال)]

        for i, c in enumerate(v_cols_extrn):
            if c in ['بارش']:
                اعداد_مہینہ[i, :] = اعداد_مہینہ[i] / دن_مہینا_میں

        تاریخ = خود.rango_potencial[0]
        سال_شروع = تاریخ.year
        for _ in range(ش_دن):
            n_mes = (تاریخ.year - سال_شروع) * 12 + تاریخ.month - 1
            اعداد_دن.loc[تاریخ] = اعداد_مہینہ[n_mes]
            تاریخ += ft.timedelta(days=1)

        return اعداد_دن


class سال_مشا(ذریعہ):

    def __init__(خود, archivo, cols_datos, c_años):

        super().__init__(چوڑائی=None, طول=None, بلندی=None)

        خود.nombres_cols = cols_datos

        خود.اعداد = gen_bd(archivo)
        خود.سال = خود.اعداد.obt_datos(cols=c_años)

        خود.rango_potencial = (ft.datetime(year=min(خود.سال), month=1, day=1),
                               ft.datetime(year=max(خود.سال), month=1, day=1))

    def _اعداد_پیدا_کرنا(خود, سے, تک, **kwargs):

        v_cols = [خود.nombres_cols[x] for x in خود.cols_día]

        اعداد_سال = خود.اعداد.obt_datos(cols=v_cols)

        ش_دن = (خود.rango_potencial[1] - خود.rango_potencial[0]).days

        اعداد_دن = pd.DataFrame(index=pd.date_range(*خود.rango_potencial), columns=v_cols)
        تاریخ = خود.rango_potencial[0]
        سال_شروع = خود.سال.min()

        días_en_año = [366 if calendar.isleap(x) else 365 for x in خود.سال]

        for i, c in enumerate(v_cols):
            if c in ['بارش']:
                اعداد_سال[i, :] = اعداد_سال[i] / días_en_año

        for د in range(ش_دن):
            n_año = تاریخ.year - سال_شروع
            اعداد_دن.loc[د] = اعداد_سال[n_año]
            د += 1

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

    def __init__(خود, archivo):
        خود.archivo = archivo

        if not os.path.isfile(archivo):
            raise FileNotFoundError

        خود.n_obs = خود.calc_n_obs()

    def sacar_cols(خود):
        """

        :return:
        :rtype: list[str]
        """
        raise NotImplementedError

    def obt_datos(خود, cols, prec_dec=None):
        """

        :param cols:
        :type cols: list[str] | str
        :param prec_dec:
        :type prec_dec: int
        :return:
        :rtype: np.ndarray
        """
        raise NotImplementedError

    def obt_datos_tx(خود, cols):
        """

        :param cols:
        :type cols: list[str] | str
        :return:
        :rtype: list
        """
        raise NotImplementedError

    def obt_días(خود, col):
        """

        :param col:
        :type col: str
        :return:
        :rtype: (ft.date, np.ndarray)
        """

        # Sacar la lista de fechas en formato texto
        fechas_tx = خود.obt_datos_tx(cols=col)

        # Procesar la lista de fechas
        fch_inic_datos, v_núm = خود.leer_fechas(lista_fechas=fechas_tx)

        # Devolver información importante
        return fch_inic_datos, v_núm

    def calc_n_obs(خود):
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
                raise ValueError(
                    'No puedo leer los اعداد_دن de fechas. ¿Mejor le eches un vistazo a tu base de اعداد_دن?')

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

    def calc_n_obs(خود):
        """

        :rtype: int
        """
        with open(خود.archivo, encoding='UTF8') as d:
            n_filas = sum(1 for f in d if len(f)) - 1  # Sustrayemos la primera fila

        return n_filas

    def obt_datos(خود, cols, prec_dec=None):
        """

        :param cols:
        :type cols: str | list[str]
        :param prec_dec:
        :type prec_dec: int
        :return:
        :rtype: np.ndarray
        """
        if not isinstance(cols, list):
            cols = [cols]

        m_datos = np.empty((len(cols), خود.n_obs))

        with open(خود.archivo, encoding='UTF8') as d:
            lector = csv.DictReader(d)
            for n_f, f in enumerate(lector):
                m_datos[:, n_f] = [tx_a_núm(f[c]) if f[c] != '' else np.nan for c in cols]

        if len(cols) == 1:
            m_datos = m_datos[0]

        if prec_dec is not None:
            if prec_dec == 0:
                m_datos = m_datos.astype(int)
            else:
                m_datos.round(prec_dec, out=m_datos)

        return m_datos

    def obt_datos_tx(خود, cols):
        """

        :param cols:
        :type cols: list[str] | str
        :return:
        :rtype: list
        """
        if not isinstance(cols, list):
            cols = [cols]

        l_datos = [[''] * خود.n_obs] * len(cols)

        with open(خود.archivo, encoding='UTF8') as d:
            lector = csv.DictReader(d)
            for n_f, f in enumerate(lector):
                for i_c, c in enumerate(cols):
                    l_datos[i_c][n_f] = f[c]

        if len(cols) == 1:
            l_datos = l_datos[0]

        return l_datos

    def sacar_cols(خود):
        """

        :return:
        :rtype: list[str]
        """

        with open(خود.archivo, encoding='UTF8') as d:
            lector = csv.reader(d)

            nombres_cols = next(lector)

        return nombres_cols


class BDsql(BD):
    """
    Una clase para leer bases de اعداد_دن en formato SQL.
    """

    def calc_n_obs(خود):
        """

        :return:
        :rtype:
        """
        pass

    def obt_datos(خود, cols, prec_dec):
        """

        :param cols:
        :type cols:
        :param prec_dec:
        :type prec_dec:
        :return:
        :rtype:
        """
        pass

    def obt_datos_tx(خود, cols):
        """

        :param cols:
        :type cols:
        :return:
        :rtype:
        """
        pass

    def sacar_cols(خود):
        """

        :return:
        :rtype:
        """
        pass


dic_trads = {'Latino': {'núms': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'),
                        'sep_dec': ['.', ',']},
             'हिंदी': {'núms': ('०', '१', '२', '३', '४', '५', '६', '७', '८', '९'),
                       'sep_dec': ['.', ',']},
             'ਪੰਜਾਬੀ': {'núms': ('੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯'),
                        'sep_dec': ['.', ',']},
             'ગુજરાતી': {'núms': ('૦', '૧', '૨', '૩', '૪', '૫', '૬', '૭', '૮', '૯'),
                         'sep_dec': ['.', ',']},
             'മലയാളം': {'núms': ('൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯'),
                        'sep_dec': ['.', ',']},
             'தமிழ்': {'núms': ('൦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯'),
                       'sep_dec': ['.', ','],
                       'bases': [(10, '௰'), (100, '௱'), (1000, '௲')]},
             'اردو': {'núms': ('٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'),
                      'sep_dec': ['.', ',']},
             'العربية': {'núms': ('٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩',),
                         'sep_dec': ['.', ',']},
             'فارسی': {'núms': ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'),
                       'sep_dec': ['.', ',']},
             'ଓରିୟା': {'núms': ('୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯'),
                       'sep_dec': ['.', ',']},
             'ಕನ್ನಡ': {'núms': ('೦', '೧', '೨', '೩', '೪', '೫', '೬', '೭', '೮', '೯'),
                       'sep_dec': ['.', ',']},
             'తెలుగు': {'núms': ('౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯'),
                        'sep_dec': ['.', ',']},
             '汉语': {'núms': ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'),
                    'sep_dec': ['.', ',']},
             '日本語': {'núms': ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'),
                     'sep_dec': ['.', ',']},
             }


def tx_a_núm(texto):
    """
    Esta función toma texto de un número en cualquier idioma y lo cambia a un número Python.

    :param: El texto a convertir.
    :type texto: str

    :return: El número de Python correspondiendo
    :rtype: float

    """

    for lengua, d_l in dic_trads.items():
        # Intentar cada lengua disponible.

        l_sep_dec = d_l['sep_dec']  # El separador de decimales
        if not isinstance(l_sep_dec, list):
            l_sep_dec = [l_sep_dec]

        l_núms = list(d_l['núms'])  # Los números

        # Ver si hay posibilidad de un sistema de bases
        try:
            bases = d_l['bases']
        except KeyError:
            bases = None

        # Intentar traducir literalmente, número por número
        for sep_dec in l_sep_dec:
            try:
                núm = _trad_texto(texto=texto, núms=l_núms, sep_dec=sep_dec)
                # ¿Funcionó? ¡Perfecto!
                return núm
            except ValueError:
                pass  # ¿No funcionó? Qué pena. Ahora tenemos que trabajar.

        if bases is not None:
            # Intentar ver si puede ser un sistema de bases (unidades).

            try:

                # Ver si hay de separar decimales
                try:
                    entero, dec = texto.split(sep_dec)
                except ValueError:
                    entero = texto
                    dec = None

                # Expresiones RegEx para esta lengua
                regex_núm = r'[{}]'.format(''.join([n for n in l_núms]))
                regex_unid = r'[{}]'.format(''.join([b[1] for b in bases]))
                regex = r'((?P<núm>{})?(?P<unid>{}|$))'.format(regex_núm, regex_unid)

                # Intentar encontrar secuencias de unidades y de números en el texto.
                m = re.finditer(regex, entero)
                resultados = [x for x in list(m) if len(x.group())]

                if not len(resultados):
                    # Si no encontramos nada, seguir con la próxima lengua
                    continue

                # Grupos de números y de sus bases (unidades)
                grupos = resultados[:-1]

                # Dividir en números y en unidades
                núms = [_trad_texto(g.group('núm'), núms=l_núms, sep_dec=sep_dec) for g in grupos]
                unids = [_trad_texto(g.group('unid'), núms=[b[1] for b in bases], sep_dec=sep_dec)
                         for g in grupos]

                # Calcular el valor de cada número con su base.
                vals = [núms[i] * u for i, u in enumerate(unids)]

                # Agregar o multiplicar valores, como necesario.
                val_entero = vals[0]
                for i, v in enumerate(vals[1:]):
                    if unids[i + 1] > unids[i]:
                        val_entero *= v
                    else:
                        val_entero += v

                # Calcular el número traducido
                if dec is not None:
                    # Si había decima, convertir el texto decimal
                    val_dec = _trad_texto(texto=dec, núms=l_núms, sep_dec=sep_dec, txt=True)

                    # Calcular el número
                    núm = float(str(val_entero) + sep_dec + val_dec)

                else:
                    # ... si no había decimal, no hay nada más que hacer
                    núm = val_entero

                return núm  # Devolver el número

            except (KeyError, ValueError):
                # Si no funcionó, intentemos otra lengua
                pass

    # Si ninguna de las lenguas funcionó, hubo error.
    raise ValueError('No se pudo decifrar el número %s' % texto)


def _trad_texto(texto, núms, sep_dec, txt=False):
    """
    Esta función traduce un texto a un valor numérico o de texto (formato latino).

    :param texto: El texto para traducir.
    :type texto: str
    :param núms: La lista, en orden ascendente, de los carácteres que corresponden a los números 0, 1, 2, ... 9.
    :type núms: list[str]
    :param sep_dec: El separador de decimales
    :type sep_dec: str
    :param txt: Si hay que devolver en formato de texto
    :type txt: bool
    :return: El número convertido.
    :rtype: float | txt
    """

    if all([x in núms + [sep_dec] for x in texto]):
        # Si todos los carácteres en el texto están reconocidos...

        # Cambiar el separador de decimal a un punto.
        texto = texto.replace(sep_dec, '.')

        for n, d in enumerate(núms):
            # Reemplazar todos los números también.
            texto = texto.replace(d, str(n))

        # Devolver el resultado, o en texto, o en formato numeral.
        if txt:
            return texto
        else:
            return float(texto)

    else:
        # Si no se reconocieron todos los carácteres, no podemos hacer nada más.
        raise ValueError('Texto "{}" no reconocido.'.format(texto))
