#!/usr/bin/env python

import calendar
import os
import shutil
import sys

راستہ_بنیاد = os.path.split(__file__)[0]
مسل_۳۶۵ = os.path.join(راستہ_بنیاد, '۳۶۵دن.WTG')
مسل_۳۶۶ = os.path.join(راستہ_بنیاد, '۳۶۶دن.WTG')


def بنیادی(راستہ, سانچے, خاکے, سال, تکرار):
    مسلیں = [مسل for مسل in os.listdir(راستہ) if os.path.splitext(مسل)[1].upper() == '.CLI']
    for مسل in مسلیں:
        جگہ = os.path.splitext(مسل)[0]
        راستہ_نتیجہ = os.path.join(راستہ, '_'.join([جگہ, سانچے, خاکے, سال]))
        if not os.path.isdir(راستہ_نتیجہ):
            os.mkdir(راستہ_نتیجہ)
        for تکر in range(1, int(تکرار) + 1):
            if calendar.isleap(2000 + تکر):
                مسل_سانچہ = مسل_۳۶۶
            else:
                مسل_سانچہ = مسل_۳۶۵
            نام_مسل = جگہ + str(تکر).rjust(2, '0') + '01.WTG'
            shutil.copyfile(مسل_سانچہ, os.path.join(راستہ_نتیجہ, نام_مسل))


if __name__ == '__main__':
    بنیادی(*sys.argv[2:7])
