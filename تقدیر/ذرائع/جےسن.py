import json

import pandas as pd
from chardet import UniversalDetector

from تقدیر.متغیرات import متغیرات
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

    def _کوائف_بنانا(خود, سے, تک, عرض, طول, بلندی, خاکے):

        ستون_تاریخ = خود._نام_عمودی_ستون('تاریخ')

        اعداد_جےسن = pd.DataFrame(
            data={س: خود.جےسن[خود._نام_عمودی_ستون(س)] for س in متغیرات if خود._نام_عمودی_ستون(س) in خود.جےسن},
            index=خود._اشاریہ_پانڈا_بنانا(خود.جےسن[ستون_تاریخ])
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
