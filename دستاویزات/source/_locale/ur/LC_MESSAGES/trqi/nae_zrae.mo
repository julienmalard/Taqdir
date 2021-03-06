��          �               �   �  �   �  �     Z	  �   l	  �   [
  �   8        �     �   �     �  (  �  $  �  }  �  �  o  �  I     �  �   �  �   �  �   �     �  �   �  �   Y        (  %   $  N"   class جےسن(ذریعہ_نکتہ):

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
     return اعداد_جےسن class ناسا(ذریعہ):

    def _کوائف_بنانا(خود, سے, تک, عرض, طول, بلندی, خاکے):
        try:
            ذریعہ_ناسا = NASAPowerWeatherDataProvider(latitude=عرض, longitude=طول, force_update=False)
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

        return اعداد_پاندس اعم ذرائع اگر آپکو ايسی وضع کے کوائف استعمال کرنے ہیں جو ابھی تک تقدیر میں دستیاب نہیں ہیں، تو آپ اسکے لئے ایک نئے ذریعہ کی قسم بنا سکتے ہیں۔ تقدیر میں دو قسم کے ‍‌ذرائع ہیں، اعم ذرائع (:class:`~تقدیر.ذریعہ.ذریعہ`) اور نکتہ کے ذرائع (:class:`~تقدیر.ذریعہ_نکتہ.ذریعہ_نکتہ`)۔ نئی قسم کے ليے، اعم ذریع ہو یا نکتہ کا بھی، آپکو ایک نيا فعل لکھنا پڑے گا: :meth:`~تقدیر.ذریعہ.ذریعہ._کوائف_بنانا`۔ نئے ذرائع نمونے کے طور پر جےسن نام کے ذریعے کا :meth:`~تقدیر.ذریعہ_نکتہ.ذریعہ_نکتہ._کوائف_بنانا` نام کا فعل نیچے دیا گيا ہے۔ نمونے کے طور پر ناسا نام کے ذریعے کا :meth:`~تقدیر.ذریعہ.ذریعہ._کوائف_بنانا` نام کا فعل نیچے دیا گيا ہے۔ نکتہ کا ذرائع نکتہ کا ذرائع کو بناتے پر ھی بتانے پڑھتا ہیے کے کہاں کا ہیے اور کس خاکے سے۔ اسی لیے آپکا :meth:`~تقدیر.ذریعہ_نکتہ.ذریعہ_نکتہ._کوائف_بنانا` نام کا فعل میں تاریخ، عرض، طول، بلندی، یا خاکے کے بارے میں فکر کرنے کی ظرورت نہیں، ‎‎سرف دستیاب کوائف پاندس میں واپس دینا۔ تقدیر آپکے لیے تاریخ، جگہ اور خاکے کا جانچ کریگا۔ نکتہ کے ذرائع وہ ‌ذرائع ہیں جنکو بناتے پر ھی پتا ھو جاتا ہیے کے انکے کوائف نکشہ پر کس نکتے سے ایں گے۔ نکتہ کے ذرائے کا ایک نمونہ ہیے دیسات کے مسل کا ذریع، کیوں کے مسل میں ایک ہی جگہ کے کوائف رہتے ہیں۔ اعم ذرائع میں مختلف جگے کے کوائف دستیاب ہیں، جیسے کے مرکسم کا ذریع، جسے پوری دنیا کے کوائف ملی جا سکتے ہیں۔ Project-Id-Version: تقدیر 1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-07-03 13:56+0000
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ur
Language-Team: ur <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 class جےسن(ذریعہ_نکتہ):

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
     return اعداد_جےسن class ناسا(ذریعہ):

    def _کوائف_بنانا(خود, سے, تک, عرض, طول, بلندی, خاکے):
        try:
            ذریعہ_ناسا = NASAPowerWeatherDataProvider(latitude=عرض, longitude=طول, force_update=False)
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

        return اعداد_پاندس اعم ذرائع اگر آپکو ايسی وضع کے کوائف استعمال کرنے ہیں جو ابھی تک تقدیر میں دستیاب نہیں ہیں، تو آپ اسکے لئے ایک نئے ذریعہ کی قسم بنا سکتے ہیں۔ تقدیر میں دو قسم کے ‍‌ذرائع ہیں، اعم ذرائع (:class:`~تقدیر.ذریعہ.ذریعہ`) اور نکتہ کے ذرائع (:class:`~تقدیر.ذریعہ_نکتہ.ذریعہ_نکتہ`)۔ نئی قسم کے ليے، اعم ذریع ہو یا نکتہ کا بھی، آپکو ایک نيا فعل لکھنا پڑے گا: :meth:`~تقدیر.ذریعہ.ذریعہ._کوائف_بنانا`۔ نئے ذرائع نمونے کے طور پر جےسن نام کے ذریعے کا :meth:`~تقدیر.ذریعہ_نکتہ.ذریعہ_نکتہ._کوائف_بنانا` نام کا فعل نیچے دیا گيا ہے۔ نمونے کے طور پر ناسا نام کے ذریعے کا :meth:`~تقدیر.ذریعہ.ذریعہ._کوائف_بنانا` نام کا فعل نیچے دیا گيا ہے۔ نکتہ کا ذرائع نکتہ کا ذرائع کو بناتے پر ھی بتانے پڑھتا ہیے کے کہاں کا ہیے اور کس خاکے سے۔ اسی لیے آپکا :meth:`~تقدیر.ذریعہ_نکتہ.ذریعہ_نکتہ._کوائف_بنانا` نام کا فعل میں تاریخ، عرض، طول، بلندی، یا خاکے کے بارے میں فکر کرنے کی ظرورت نہیں، ‎‎سرف دستیاب کوائف پاندس میں واپس دینا۔ تقدیر آپکے لیے تاریخ، جگہ اور خاکے کا جانچ کریگا۔ نکتہ کے ذرائع وہ ‌ذرائع ہیں جنکو بناتے پر ھی پتا ھو جاتا ہیے کے انکے کوائف نکشہ پر کس نکتے سے ایں گے۔ نکتہ کے ذرائے کا ایک نمونہ ہیے دیسات کے مسل کا ذریع، کیوں کے مسل میں ایک ہی جگہ کے کوائف رہتے ہیں۔ اعم ذرائع میں مختلف جگے کے کوائف دستیاب ہیں، جیسے کے مرکسم کا ذریع، جسے پوری دنیا کے کوائف ملی جا سکتے ہیں۔ 