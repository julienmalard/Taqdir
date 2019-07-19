import calendar
import os
import time
import zipfile

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from tradssat import WTHFile
from .مرکسم۵ import مرکسم۵_سانچہ


class مرکسم۵_جال(مرکسم۵_سانچہ):
    """
    یہ ذریعہ مرکسم ۵ کے `جلبینی صفحہ <http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3>`_
    سے آوہوا تبدیلی کے کوائف پاتا ہیے۔
    """

    def _مسل_کوائف_بنانا(خود, سلسلہ_سال, چوڑائی, طول, بلندی, خاکے, سانچے_نمونہ):  # پراگما: مت دکھنا

        جگہ = 'TQDR'
        راستہ_نتیجہ = خود.راستے.راستے_پانا(چوڑائی, طول, بلندی)
        راستہ_مسل = os.path.join(راستہ_نتیجہ, '{}.zip'.format(جگہ))

        for سال in سلسلہ_سال:
            try:
                اختیار_فایئرفاکس = webdriver.FirefoxProfile()
            except WebDriverException:
                return
            اختیار_فایئرفاکس.set_preference('browser.download.folderList', 2)
            اختیار_فایئرفاکس.set_preference('browser.download.manager.showWhenStarting', False)
            اختیار_فایئرفاکس.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

            اختیار_فایئرفاکس.set_preference('browser.download.dir', راستہ_نتیجہ)
            try:
                with webdriver.Firefox(firefox_profile=اختیار_فایئرفاکس) as فایئرفاکس:
                    فایئرفاکس.get("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3")

                    راستہ_کا_نام = خود._راستہ_نتیجہ(چوڑائی, طول, بلندی, سال=سال, خاکے=خاکے, نمونے=خود.نمونے)
                    if خود._راستہ_بھری_ہیے(راستہ_کا_نام):
                        continue
                    os.makedirs(راستہ_کا_نام)

                    فایئرفاکس.find_element_by_name('latitude').send_keys(str(چوڑائی))

                    فایئرفاکس.find_element_by_name('longitude').send_keys(str(طول))

                    فایئرفاکس.find_element_by_name('place').send_keys(جگہ)

                    if سانچے_نمونہ == '۰۰۰۰۰۰۰۰۰۰۰۰۰۰۰۰۰':
                        فایئرفاکس.find_element_by_link_text('None').click()
                    else:
                        if سانچے_نمونہ == '۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱':
                            فایئرفاکس.find_element_by_link_text('Select All Models').click()
                        else:
                            ف_نمونہ = [
                                'bcc1', 'bcc2', 'CSIR', 'FIOE', 'GFD1', 'GFD2', 'GFD3', 'GIS1', 'GIS2', 'HadG', 'IPS1',
                                'IPS2',
                                'MIR2', 'MIR3', 'MIR1', 'MRIC', 'NorE'
                            ]
                            for ن, نام in zip(سانچے_نمونہ, ف_نمونہ):
                                if int(ن):
                                    فایئرفاکس.find_element_by_id('chkbx_' + نام).click()

                        فایئرفاکس.find_element_by_xpath('//input[@value="{}"]'.format(خاکے)).click()

                        فایئرفاکس.find_element_by_name('yearsimulation').send_keys(str(سال if سال >= 2010 else 2010))

                    فایئرفاکس.find_element_by_name('numrep').send_keys(str(12 if not calendar.isleap(سال) else 40))

                    فایئرفاکس.find_element_by_id('BtnRun').click()

                    if os.path.isfile(راستہ_مسل):
                        os.remove(راستہ_مسل)

                    while فایئرفاکس.find_element_by_id('td_results').get_attribute('style') == 'display: none;':
                        time.sleep(1)

                    while not فایئرفاکس.find_element_by_xpath('//a[img/@src="images/zip-icon.jpg"]') \
                            .find_element_by_xpath('.').get_attribute('href'):
                        time.sleep(1)

                    time.sleep(1)
                    فایئرفاکس.find_element_by_xpath('//a[img/@src="images/zip-icon.jpg"]').click()

                    while not os.path.isfile(راستہ_مسل):
                        pass

                    فایئرفاکس.close()

            except WebDriverException:
                return

            with zipfile.ZipFile(راستہ_مسل) as زیپ:
                زیپ.extractall(path=راستہ_کا_نام)

            os.remove(راستہ_مسل)

            for م in os.listdir(راستہ_کا_نام):
                نام, توسیع = os.path.splitext(م)
                if WTHFile.matches_file(م) and calendar.isleap(2000 + int(نام[-4:-2])) != calendar.isleap(سال):
                    os.remove(os.path.join(راستہ_کا_نام, م))
