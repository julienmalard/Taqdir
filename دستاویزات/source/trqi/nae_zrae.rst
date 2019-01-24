.. _نئے_ذرائع:

نئے ذرائع
=========
اگر آپکو ايسی وضع کے کوائف استعمال کرنے ہیں جو ابھی تک تقدیر میں دستیاب نہیں ہیں،تو آپ اسکے لئے ایک نئے ذریعہ کی قسم بنا
سکتے ہیں۔


نئی قسم کے ليے آپکو ایک نيا فعل لکھنا پڑے گا، :meth:`~تقدیر.ذریعہ._کوائف_بنانا`.

نمونے کے طور پر ناسا نام کے ذریعے کا _کوائف_بنانا() نام کا فعل نیچے دیا گيا ہے۔

.. code-block:: python

   try:
       ذریعہ_ناسا = NASAPowerWeatherDataProvider(latitude=‏عرض, longitude=طول, force_update=False)
   except (requests.exceptions.ConnectionError, KeyError, JSONDecodeError):
       return

   سے = max(ذریعہ_ناسا.first_date, سے)
   تک = min(ذریعہ_ناسا.last_date, تک)

   اعداد_پاندس = pd.DataFrame(columns=list(متغیرات), index=pd.period_range(سے, تک), dtype=float)

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
