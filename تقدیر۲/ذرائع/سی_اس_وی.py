from chardet import UniversalDetector
from تقدیر۲.ذریعہ import ذریعہ


class سی_اس_وی(ذریعہ):

    def __init__(خود, مسل,  چوڑائی, طول, بلندی=None, خاکے=None):
        خود.مسل = مسل
        خود.چوڑائی = چوڑائی
        خود.طول = طول
        خود.بلندی = بلندی
        خود.خاکے = خاکے

    def کوائف_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):
        ضابطہ = _ضابطہ_بندی(خود.مسل)
        
        with open(خود.مسل, 'r', encoding=ضابطہ) as م:
            


def _ضابطہ_بندی(مسل):
    آلہ = UniversalDetector()
    with open(مسل, 'rb') as م:
        for لکیر in م.readlines():

            آلہ.feed(لکیر)

            if آلہ.done:
                break

    آلہ.close()

    return آلہ.result['encoding']