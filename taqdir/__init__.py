import json
import os
from pkg_resources import resource_filename as وسائل_کا_نام
from warnings import warn as انتباہ


with open(وسائل_کا_نام('taqdir', 'تبدیل.txt'), 'r', encoding='utf8') as archivo_versión:
    __تبدیل__ = archivo_versión.read().strip()

__version__ = __تبدیل__


def جسون_پڑھنا(مسل):
    with open(مسل, 'r', encoding='utf8') as م:
        دستاویز = json.load(م)

    return دستاویز


def جسون_بچانا(مسل, راستہ):
    with open(راستہ, 'w', encoding='utf8') as ر:
        json.dump(مسل, ر, ensure_ascii=False, sort_keys=True, indent=2)  # Guardar todo


مسل_قابو = وسائل_کا_نام('taqdir', 'مسل_مرکسم.json')
لغت_قابو = جسون_پڑھنا(مسل_قابو)
مسل_مرکسم = لغت_قابو['مسل_مرکسم']

# پہلا دیکھیںگے کہ کیا مارکسم کا راستہ میں مسل ہے یا نہیں.
if os.path.isdir(مسل_مرکسم):
    # اگر نہیں ہے، تو اسے جوڑنا.
    مسل_مرکسم = os.path.join(مسل_مرکسم, 'MarkSim_Standalone_v2.exe')


# اگر اب تک مسل سہی نہیں ہے، تو تکلیف ہوتی ہے.
if not os.path.isfile(مسل_مرکسم):
    if مسل_مرکسم == "":
        انتباہ('مرکسم کا مسل نہیں ملی. اسے "taqdir.مرکسم_وضاحت_کریں()" سے وضاحت کیجئے.')
elif not os.path.isdir(مسل_مرکسم):
        انتباہ('مرکسم کا مسل کا راستہ سہی نہیں ہے. اسے "taqdir.مرکسم_وضاحت_کریں()" سے ٹھیک کر دیجئے.')


def مرکسم_وضاحت_کریں(راستہ):

    if not os.path.isfile(راستہ):
        if os.path.isdir(راستہ):
            راستہ = os.path.join(راستہ, 'MarkSim_Standalone_v2.exe')
        else:
            انتباہ('راستہ سہی نہیں.')

    لغت_قابو['مسل_مرکسم'] = راستہ
    جسون_بچانا(مسل=لغت_قابو, راستہ=مسل_قابو)
