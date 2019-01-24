![taqdir](دستاویزات/source/_static/تسویر_چھوٹی.png)

# تقدیر

[![Build Status](https://travis-ci.org/julienmalard/Taqdir.svg?branch=master)](https://travis-ci.org/julienmalard/Taqdir)
[![Coverage Status](https://coveralls.io/repos/github/julienmalard/Taqdir/badge.svg?branch=master)](https://coveralls.io/github/julienmalard/Taqdir?branch=master)
[![Documentation Status](https://readthedocs.org/projects/taqdir/badge/?version=latest)](https://taqdir.readthedocs.io/ur/latest/?badge=latest)

[![CodeFactor](https://www.codefactor.io/repository/github/julienmalard/taqdir/badge)](https://www.codefactor.io/repository/github/julienmalard/taqdir)
[![Maintainability](https://api.codeclimate.com/v1/badges/d1e4113d31c354cb6f20/maintainability)](https://codeclimate.com/github/julienmalard/Taqdir/maintainability)

## تقدیر کیا ہیے؟
تقدیر آب وہوا میں تبدیلی کے کوائف پایتھون کو ديتا ھے۔

## اسکا نام تقدیر کیوں ہے ؟
تکہ ہم بھول نہ جائں کہ آبوہوا میں تبدیلی کی بات میں کوئی تقدیر نہیں ہیے،
شاید انسانیت کی خود کی بیوکوف کے علاوہ۔

## استعمال کیسا کرنا؟
پہلہ ایک مقام بنانا جینکے کوائف ہمہیں چاییئے۔ بعاد میں اسّے کوائف ماں گنی۔ بس۔

```python
from تقدیر.مقام import مقام

میرا_مقام = مقام(عرض=11.02, طول=76.96, بلندی=1)

کو = میرا_مقام.کوائف_پانا(سے='۲۰۱۸۰۱۰۱', تک='۲۰۱۷۰۱۰۱')

کو.لاپتہ()  # لاپتہ دنوں کے نام پانا
کو.روزانہ()  # روزانہ کوائف، پاندس میں

# ماہانہ اور سالانہ کوائف بھی میلیں کے۔
کو.ماہانہ()
کو.سالانہ()

# نتیجہ کو مسل کے تور پر بھی لیکھ سکتے ہیں۔
کو.لکھنا('/میرا/راستہ', '.csv')
```

اگر آپکے پاس مشاہدات کے کوائف ہیں تو یہ بھی جوڑی جا سکتی ہیں۔

```python
from تقدیر.مقام import مقام
from تقدیر.ذرائع import سی_اس_وی

میرا_مقام = مقام(عرض=11.02, طول=76.96, بلندی=1)
مشاہدات = سی_اس_وی('مشاہدات.csv', عرض=11.02, طول=76.96, بلندی=1)
کو = میرا_مقام.کوائف_پانا(سے='۲۰۱۸۰۱۰۱', تک='۲۰۱۷۰۱۰۱', ذرائع=مشاہدات)
```

مشاہدات دیسات اور جسان سے بھی پڑھی جا سکتی ہیں۔

## تقدیر کام کیسا کارتا ہیے؟
اگر آپنے تقدیر کو مشاہدات دیئے ہیں، تقدیر پہلہ سے ھی کوائف وہاں سے اٹھائگا۔
بعاد مرکسم (مستقبل کے لئے) اور ناسا (ماضی کے لئے) سے کوائف ڈھونڈے کی کوشیش کریگا۔

## مصنفین
[ژولیئں ملاغ](https://www.researchgate.net/profile/Julien_Malard)
julien.malard@mail.mcgill.ca


[محمّد انعام اظہر بیگ](https://www.researchgate.net/profile/Azhar_Baig)
muhammad.baig@mail.mcgill.ca
