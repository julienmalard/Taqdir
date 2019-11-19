import numpy as np
from تقدیر import ذریعہ
from تقدیر.کام import بلندی_پانا


class ذریعہ_نکتہ(ذریعہ):
    """
    نکتہ کے ذرائع اعم ذرائع کے جیسے ہیں، پر انہیں بناتے پر ھی بتانے پڈتا ہیے کہ کیس جگہ کے ہیں۔
    """

    def __init__(خود, عرض, طول, بلندی, خاکے=None, تبدیل_عمودی_ستون=None):
        خود.عرض = عرض
        خود.طول = طول
        خود.بلندی = بلندی if بلندی is not None else بلندی_پانا(عرض, طول)
        خود.خاکے = خاکے
        خود.تبدیل_عمودی_ستون = تبدیل_عمودی_ستون or {}

    def کوائف_پانا(خود, سے, تک, عرض, طول, بلندی, خاکے='۸.۵'):
        if خود.عرض != عرض or خود.طول != طول or (بلندی is not None and np.isfinite(بلندی) and بلندی != خود.بلندی):
            return
        if خود.خاکے is not None and خاکے is not None and خود.خاکے != خاکے:
            return

        return super().کوائف_پانا(سے, تک, عرض, طول, بلندی, خاکے='۸.۵')

    @property
    def متغیرات(خود):
        raise NotImplementedError

    def _نام_عمودی_ستون(خود, ستون):
        try:
            return خود.تبدیل_عمودی_ستون[ستون]
        except KeyError:
            return ستون

    def _کوائف_بنانا(خود, سے, تک, عرض, طول, بلندی, خاکے):
        raise NotImplementedError
