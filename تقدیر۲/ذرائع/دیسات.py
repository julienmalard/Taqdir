from تقدیر۲.ذریعہ import ذریعہ
from tradssat import WTHFile

class ناسا(ذریعہ):
    
    def __init__(خود, مسل):
        خود.مسل = مسل
    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):

        اعداد_پاندس = خود._پاندس_بنانا(سے, تک)
        koaf_dssat = WTHFile(خود.مسل)

        lat_dssat = koaf_dssat.get_value('LAT')
        long_dssat = koaf_dssat.get_value('LONG')
        elev_dssat = koaf_dssat.get_value('ELEV')
        if lat_dssat != چوڑائی or long_dssat != طول or (بلندی is not None and بلندی != elev_dssat):
            return
        
        dssat_se_bharna(koaf_dssat, اعداد_پاندس)
        

        return اعداد_پاندس

def دیسات_پھڑھنا(مسل, اعداد_پاندس):
    'SRAD  TMAX  TMIN  RAIN'

    ستون = {
        'بارش': 'RAIN',
        'شمسی_تابکاری': 'SRAD',
        'درجہ_حرارت_زیادہ': 'TMAX',
        'درجہ_حرارت_کم': 'TMIN',
        'درجہ_حرارت_اوسط': 'TEMP'
    }

    for تاریخ in اعداد_پاندس.index:
        for س, س_ناسا in ستون.items():
            اعداد_پاندس.loc[تاریخ][س] =

    for mt, mt_DSSAT in mts_.items():
        pass

    درجہ_حرارت_اوسط = نمپی.add(درجہ_حرارت_زیادہ, درجہ_حرارت_کم) / 2