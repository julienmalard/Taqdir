import json
import os
import shutil
import tempfile
import datetime
import pandas as pd
راستہ_اختیارے = os.path.join(os.path.split(__file__)[0], 'اختیارے.json')
try:
    with open(راستہ_اختیارے, 'r', encoding='utf8') as م:
        _اختیارے = json.load(م)
except (FileNotFoundError, json.JSONDecodeError, PermissionError):
    _اختیارے = {}


def اختیارہ_رکھنا(اختیارہ, قیمت):
    _اختیارے[اختیارہ] = قیمت
    مسل_رکھنا(json.dumps(_اختیارے, ensure_ascii=False, sort_keys=True, indent=2), راستہ_اختیارے)


def اختیارہ_پانا(اختیارہ):
    try:
        return _اختیارے[اختیارہ]
    except KeyError:
        return


def مسل_رکھنا(متن, مسل):
    with tempfile.NamedTemporaryFile('w', encoding='UTF-8', delete=False) as مسل_شروع:
        مسل_شروع.write(متن)

        راستہ = os.path.split(مسل)[0]
        if راستہ and not os.path.isdir(راستہ):  # pragma: sin cobertura
            os.makedirs(os.path.split(مسل)[0])

    if os.path.splitdrive(مسل_شروع.name)[0] == os.path.splitdrive(مسل)[0]:
        os.replace(مسل_شروع.name, مسل)
    else:
        shutil.move(مسل_شروع.name, مسل)


def تاریخ_بنانا(تاریخ):
    if isinstance(تاریخ, datetime.datetime):
        return تاریخ.date()
    elif isinstance(تاریخ, datetime.date):
        return تاریخ
    return pd.to_datetime(تاریخ).date()
