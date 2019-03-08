import os

from எண்ணிக்கை import உரைக்கு as உ

from .ذریعہ import ذریعہ
from .کام import متغیرات, اختیارہ_پانا, اختیارہ_رکھنا
from .مقام import مقام

with open(os.path.join(os.path.split(__file__)[0], 'تبدیل.txt'), 'r', encoding='utf8') as تبدیل_کی_دستاویز:
    __تبدیل__ = உ(تبدیل_کی_دستاویز.read().strip(), 'latin', 'ار')
