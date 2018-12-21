import datetime

from tradssat import WTHFile
from تقدیر۲.ذریعہ import ذریعہ


class دیسات(ذریعہ):

    def __init__(خود, مسل):
        خود.مسل = مسل

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        اعداد_پاندس = خود._پاندس_بنانا(سے, تک)
        کوائف_دیسات = WTHFile(خود.مسل)

        چوڑائی_دیسات = کوائف_دیسات.get_value('LAT')
        طول_دیسات = کوائف_دیسات.get_value('LONG')
        بلندی_دیسات = کوائف_دیسات.get_value('ELEV')
        if چوڑائی_دیسات != چوڑائی or طول_دیسات != طول or (بلندی is not None and بلندی != بلندی_دیسات):
            return

        دیسات_سے_بھرنا(کوائف_دیسات, اعداد_پاندس, سال=None)

        return اعداد_پاندس


def دیسات_سے_بھرنا(مسل, اعداد_پاندس, سال):
    'SRAD  TMAX  TMIN  RAIN'

    ستون = {
        'بارش': 'RAIN',
        'شمسی_تابکاری': 'SRAD',
        'درجہ_حرارت_زیادہ': 'TMAX',
        'درجہ_حرارت_کم': 'TMIN',
    }

    for ش, تاریخ in enumerate(مسل.get_value('DATE')):
        if سال is None:
            raise NotImplementedError
        else:
            اسلی_تاریخ = datetime.date(سال, 1, 1) + datetime.timedelta(days=int(تاریخ[-3:]) - 1)

        if اسلی_تاریخ in اعداد_پاندس.index:
            for مت, مت_دیسات in ستون.items():
                اعداد_پاندس.loc[اسلی_تاریخ][مت] = مسل.get_value(مت_دیسات)[ش]

    # درجہ_حرارت_اوسط = نمپی.add(درجہ_حرارت_زیادہ, درجہ_حرارت_کم) / 2
