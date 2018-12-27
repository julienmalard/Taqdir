from pcse.db import NASAPowerWeatherDataProvider

from تقدیر۲.ذریعہ import ذریعہ


class ناسا(ذریعہ):
    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        ذریعہ_ناسا = NASAPowerWeatherDataProvider(latitude=چوڑائی, longitude=طول, force_update=False)

        سے = max(ذریعہ_ناسا.first_date, سے)
        تک = min(ذریعہ_ناسا.last_date, تک)

        اعداد_پاندس = خود._پاندس_بنانا(سے, تک)

        ستون = {
            'بارش': 'RAIN',
            'شمسی_تابکاری': 'IRRAD',
            'درجہ_حرارت_زیادہ': 'TMAX',
            'درجہ_حرارت_کم': 'TMIN',
            'درجہ_حرارت_اوسط': 'TEMP'
        }

        for تاریخ in اعداد_پاندس.index:
            for س, س_ناسا in ستون.items():
                اعداد_پاندس.loc[تاریخ][س] = getattr(ذریعہ_ناسا(سے), س_ناسا)

        اعداد_پاندس.شمسی_تابکاری *= 1e-6

        return اعداد_پاندس
