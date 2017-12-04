import os
import platform
import shutil
import sys
import urllib.request
from subprocess import run
from warnings import warn as avisar

from setuptools import setup, find_packages

"""

"""

so = platform.system()
bits = platform.architecture()[0][:2]

directorio = os.path.split(os.path.realpath(__file__))[0]
directorio_python = os.path.split(sys.executable)[0]
directorio_móds = os.path.join(directorio, 'Módulos')

versión_python = str(sys.version_info.major) + str(sys.version_info.minor)

try:
    import numpy as np
except ImportError:
    np = None

info_paquetes = {'numpy': {'versión': '1.13.1',
                           'formato_archivo': 'numpy-{versión}+mkl-cp{v_py}-cp{v_py}m-{sis}.whl',
                           '35': {
                               'Windows': {
                                   '32': {'id_dropbox': None
                                          },
                                   '64': {'id_dropbox': None
                                          }
                               }
                           },
                           '36': {
                               'Windows': {
                                   '32': {'id_dropbox': 'y66rav81q0i9gtu/numpy-1.11.3%2Bmkl-cp36-cp36m-win32.whl'
                                          },
                                   '64': {'id_dropbox': None
                                          }
                               }
                           }
                           }
                 }


def _actualizar_pip():
    print('Actualizando pip...')
    comanda_pip = '%s install --upgrade pip' % (os.path.join(directorio_python, 'Scripts', 'pip'))
    run(comanda_pip)


def _descargar_whl(nombre, v_py, sis, b):
    print('Descargando paquete "{}"...'.format(nombre))
    llave = url = None

    repositorios = {'id_google': 'https://drive.google.com/uc?export=download&id={}',
                    'id_dropbox': 'https://www.dropbox.com/s/{}?dl=1'}

    for r, u in repositorios.items():
        try:
            llave = info_paquetes[nombre][v_py][sis][b][r]  # type: str
        except KeyError:
            pass
        if llave is not None:
            url = u.format(llave)
            break

    if url is None:
        avisar('No existe descarga para paquete {} en {} bits.'.format(nombre, bits))
        return False

    nombre_archivo = info_paquetes[nombre]['formato_archivo']
    urllib.request.urlretrieve(url, os.path.join(directorio_móds, nombre_archivo))

    return True


def _instalar_whl(nombre):
    nombre_archivo = info_paquetes[nombre]['formato_archivo']

    if os.path.isfile(os.path.join(directorio_móds, nombre_archivo)):
        éxito = True
    else:
        éxito = _descargar_whl(nombre, v_py=versión_python, sis=so, b=bits)

    if éxito:
        print('Instalando paquete "{}"...'.format(nombre))

        comanda = '%s install %s' % (os.path.join(directorio_python, 'Scripts', 'pip'),
                                     os.path.join(directorio_móds, nombre_archivo))
        run(comanda)


def instalar_requísitos():
    print('Instalando paquetes requísitos...')

    lista_paquetes = []

    if np is None:
        lista_paquetes.append('numpy')

    if len(lista_paquetes):

        if not os.path.exists(directorio_móds):
            os.makedirs(directorio_móds)
            dir_creado = True
        else:
            dir_creado = False

        # Actualizar Pip
        _actualizar_pip()

        # Instalar cada paquete necesario
        for paq in lista_paquetes:
            _instalar_whl(paq)

        if dir_creado:
            shutil.rmtree('Módulos')

    # Verificar que todo esté bien:
    try:
        import numpy as _
    except ImportError:
        _ = None
        pass


if so == 'Windows':

    sistema = 'win' + bits

    for paquete, dic_paq in info_paquetes.items():
        v = dic_paq['versión']
        dic_paq['formato_archivo'] = dic_paq['formato_archivo'].format(versión=v, v_py=versión_python, sis=sistema)

    instalar_requísitos()

"""
Ahora cosas normales de instalación.
"""

with open('taqdir/تبدیل.txt', 'r', encoding='utf8') as archivo_versión:
    تبدیل = archivo_versión.read().strip()


setup(
    name='taqdir',
    version=تبدیل,
    packages=find_packages(),
    url='https://pymarksim.readthedocs.io',
    download_url='https://github.com/julienmalard/PyMarksim',
    license='GNU 3',
    author='ژولئیں ژاں ملار',
    author_email='julien.malard@mail.mcgill.ca',
    description='',
    long_description='',
    requires=['numpy', 'pandas'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    package_data={
        # Incluir estos documentos de los paquetes:
        '': ['*.CLI', 'تبدیل.txt', 'مسل_مرکسم.json'],
    },
)
