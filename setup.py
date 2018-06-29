import os
import platform
import shutil
import sys
import urllib.request
from subprocess import run
from warnings import warn as avisar

from setuptools import setup, find_packages

with open('تقدیر/تبدیل.txt', 'r', encoding='utf8') as archivo_versión:
    تبدیل = archivo_versión.read().strip()


setup(
    name='taqdir',
    version=تبدیل,
    packages=find_packages(),
    url='https://taqdir.readthedocs.io',
    download_url='https://github.com/julienmalard/taqdir',
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
