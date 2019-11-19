import json

import pandas as pd
from chardet import UniversalDetector
from تقدیر.ذریعہ_نکتہ import ذریعہ_نکتہ


class جےسن(ذریعہ_نکتہ):
    """
    جےسن (``.json``) مسل سے کوائف پڑھتا ہیے۔
    """

    def __init__(خود, مسل, عرض, طول, بلندی=None, خاکے=None, تبديل_عمودی_ستون=None):
        super().__init__(عرض, طول, بلندی, خاکے, تبديل_عمودی_ستون)

        if isinstance(مسل, str):
            ضابطہ = _ضابطہ_بندی(مسل)
            with open(مسل, 'r', encoding=ضابطہ) as م:
                خود.جےسن = json.load(م)
        else:
            خود.جےسن = مسل

    @property
    def متغیرات(خود):
        return [ب for ب in [خود._نام_عمودی_ستون(س) for س in خود.جےسن] if ب != 'تاریخ']

    def _کوائف_بنانا(خود, سے, تک, عرض, طول, بلندی, خاکے):

        کو = {خود._نام_عمودی_ستون(س): قیمت for س, قیمت in خود.جےسن.items()}
        اعداد_جےسن = pd.DataFrame(
            data={م: ق for م, ق in کو.items() if م != 'تاریخ'},
            index=خود._اشاریہ_پانڈا_بنانا(کو['تاریخ'])
        )
        return اعداد_جےسن


def _ضابطہ_بندی(مسل):
    آلہ = UniversalDetector()
    with open(مسل, 'rb') as م:
        for لکیر in م.readlines():
            آلہ.feed(لکیر)
            if آلہ.done:
                break
    آلہ.close()

    return آلہ.result['encoding']
