from setuptools import setup, find_packages

from எண்ணிக்கை import உரைக்கு as உ

with open('تقدیر/تبدیل.txt', 'r', encoding='utf8') as تبدیل_کی_دستاویز:
    تبدیل = '.'.join(உ(ش, 'latin', 'فارسی') for ش in تبدیل_کی_دستاویز.read().strip().split('.'))

setup(
    name='taqdir',
    version=تبدیل,
    packages=find_packages(),
    url='https://taqdir.readthedocs.io',
    download_url='https://github.com/julienmalard/taqdir',
    license='GNU 3',
    author='ژولئیں ژاں ملاغ (Julien Jean Malard)',
    author_email='julien.malard@mail.mcgill.ca',
    description='',
    long_description='',
    install_requires=['numpy', 'pandas', 'ennikkai', 'selenium', 'pcse', 'chardet', 'tradssat', 'requests', 'scipy'],
    setup_requires=['ennikkai'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: Urdu'
    ],
    package_data={
        '': ['**/*.txt', '**/*.csv', '**/*.json', '**/*.MTH', '**/*.WTG', '**/*.WTH'],
        'تقدیر': ['*.txt', '*.csv', '*.json', '*.MTH', '*.WTG', '*.WTH']
    },
)
