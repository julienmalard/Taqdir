import datetime

from تقدیر۲.ذریعہ import ذریعہ

from tradssat import WTHFile


class دیسات(ذریعہ):

    def __init__(خود, مسل, خاکے=None):
        خود.مسل = مسل
        خود.کوائف_دیسات = WTHFile(خود.مسل)

        خود.چوڑائی = خود.کوائف_دیسات.get_value('LAT')
        خود.طول = خود.کوائف_دیسات.get_value('LONG')
        خود.بلندی = خود.کوائف_دیسات.get_value('ELEV')
        خود.خاکے = خاکے

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        اعداد_پاندس = خود._پاندس_بنانا(سے, تک)
       
        if خود.چوڑائی != چوڑائی or خود.طول != طول or (بلندی is not None and بلندی != خود.بلندی):
            return
        if خود.خاکے is not None and خود.خاکے != خاکے:
            return

        دیسات_سے_بھرنا(خود.کوائف_دیسات, اعداد_پاندس, سال=None)

        return اعداد_پاندس


def دیسات_سے_بھرنا(مسل, اعداد_پاندس, سال):
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
