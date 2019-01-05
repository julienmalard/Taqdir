.. _نئے_ذرائع:

نئے ذرائع
=========
اگر آپکہ کیسی وضع کے کوائف کا استعمال کرنا ہیے جو تقدیر میں اب تک دستیاب نہیں ہیے، آپ اسکے لئے ایک نئا ذریعہ کے قسم بنا
سکتے ہیں۔


نئا قسم میں آپکو ایک ھی نئے فعل کو لیکھنا پڑھیگا، :meth:`~تقدیر.ذریعہ._کوائف_بنانا`.

نمونے کے تور پر ناسا نام کا ذریعہ کا _کوائف_بنانا() نام کا فعل نیچے دیئا جاتا ہیے۔

.. code-block:: python

   try:
       ذریعہ_ناسا = NASAPowerWeatherDataProvider(latitude=چوڑائی, longitude=طول, force_update=False)
   except (requests.exceptions.ConnectionError, KeyError, JSONDecodeError):
       return

   سے = max(ذریعہ_ناسا.first_date, سے)
   تک = min(ذریعہ_ناسا.last_date, تک)

   اعداد_پاندس = pd.DataFrame(columns=list(متاغیرات), index=pd.period_range(سے, تک), dtype=float)

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
