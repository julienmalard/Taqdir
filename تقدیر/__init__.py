import os

from எண்ணிக்கை import உரைக்கு as உ
from .ذریعہ import ذریعہ
from .مقام import مقام
from .کام import اختیارہ_پانا, اختیارہ_رکھنا

with open(os.path.join(os.path.split(__file__)[0], 'تبدیل.txt'), 'r', encoding='utf8') as تبدیل_کی_دستاویز:
    __تبدیل__ = '.'.join(உ(ش, 'latin', 'فارسی') for ش in تبدیل_کی_دستاویز.read().strip().split('.'))
