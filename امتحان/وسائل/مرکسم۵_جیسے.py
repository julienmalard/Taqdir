#!/usr/bin/env python

import calendar
import os
import shutil
import sys

راستہ_بنیادی = os.path.split(__file__)[0]
مسل_۳۶۵ = os.path.join(راستہ_بنیادی, '۳۶۵دن.WTG')
مسل_۳۶۶ = os.path.join(راستہ_بنیادی, '۳۶۶دن.WTG')


def بنیادی(راستہ, سانچے, خاکے, سال, دہرائی):
    مسلیں = [مسل for مسل in os.listdir(راستہ) if os.path.splitext(مسل)[1].upper() == '.CLI']
    for مسل in مسلیں:
        جگہ = os.path.splitext(مسل)[0]
        راستہ_نتائیج = os.path.join(راستہ, '_'.join([جگہ, سانچے, خاکے, سال]))
        if not os.path.isdir(راستہ_نتائیج):
            os.mkdir(راستہ_نتائیج)
        for دہريا in range(1, int(دہرائی) + 1):
            if calendar.isleap(2000 + دہريا):
                مسل_سانچہ = مسل_۳۶۶
            else:
                مسل_سانچہ = مسل_۳۶۵
            نام_مسل = جگہ + str(دہريا).rjust(2, '0') + '01.WTG'
            shutil.copyfile(مسل_سانچہ, os.path.join(راستہ_نتائیج, نام_مسل))


if __name__ == '__main__':
    بنیادی(*sys.argv[2:7])
