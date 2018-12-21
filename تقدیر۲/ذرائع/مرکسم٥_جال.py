import calendar
import os
import time
import zipfile

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from .مرکسم۵ import مرکسم۵


class مرکسم۵_جال(مرکسم۵):

    def __init__(خود, نمونہ='11111111111111111'):

        super().__init__(نمونہ)

        خود.اختیار_فایئرفاکس = webdriver.FirefoxProfile()
        خود.اختیار_فایئرفاکس.set_preference('browser.download.folderList', 2)
        خود.اختیار_فایئرفاکس.set_preference('browser.download.manager.showWhenStarting', False)
        خود.اختیار_فایئرفاکس.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

    def _کوائف_بنانا(خود, سلسلہ_سال, چوڑائی, طول, بلندی, خاکے):

        نام = 'TQDR'
        راستہ_نتیجہ = os.path.join(خود.راستے, '{}.zip'.format(نام))

        خود.اختیار_فایئرفاکس.set_preference('browser.download.dir', خود.راستے.راستے_پانا(چوڑائی, طول, بلندی))

        for سال in سلسلہ_سال:

            راستہ_کا_نام = خود._راستہ_نتیجہ(چوڑائی, طول, بلندی, سال=سال, خاکے=خاکے)
            if خود._rasta_bhari_hai(راستہ_کا_نام):
                return
            os.makedirs(راستہ_کا_نام)

            فایئرفاکس = webdriver.Firefox(firefox_profile=خود.اختیار_فایئرفاکس)
            try:
                فایئرفاکس.get("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3")
            except WebDriverException:
                return

            فایئرفاکس.find_element_by_name('latitude').send_keys(str(طول))

            فایئرفاکس.find_element_by_name('longitude').send_keys(str(چوڑائی))

            فایئرفاکس.find_element_by_name('place').send_keys(نام)

            if خود.نمونے == '11111111111111111':
                فایئرفاکس.find_element_by_link_text('Select All Models').click()
            else:
                ف_نمونہ = [
                    'bcc1', 'bcc2', 'CSIR', 'FIOE', 'GFD1', 'GFD2', 'GFD3', 'GIS1', 'GIS2', 'HadG', 'IPS1', 'IPS2',
                    'MIR2', 'MIR3', 'MIR1', 'MRIC', 'NorE'
                ]
                for ن, نام in zip(خود.نمونے, ف_نمونہ):
                    if int(ن):
                        فایئرفاکس.find_element_by_id('chkbx_' + نام).click()

            فایئرفاکس.find_element_by_xpath('//input[@value="{}"]'.format(خاکے)).click()

            فایئرفاکس.find_element_by_name('yearsimulation').send_keys(str(سال if سال >= 2010 else 2010))

            فایئرفاکس.find_element_by_name('numrep').send_keys(str(12 if calendar.isleap(سال) else 40))

            فایئرفاکس.find_element_by_id('BtnRun').click()

            if os.path.isfile(راستہ_نتیجہ):
                os.remove(راستہ_نتیجہ)

            تئیار = False
            while not تئیار:
                try:
                    فایئرفاکس.find_element_by_xpath('/html/body/table[2]/tbody/tr[1]/td[1]/form/div[2]/img')
                    تئیار = True
                except NoSuchElementException:
                    pass

            تسویر = None
            while not تسویر:
                try:
                    تسویر = فایئرفاکس.find_element_by_xpath('//a[img/@src="images/zip-icon.jpg"]')
                    تسویر.click()
                except NoSuchElementException:
                    pass

            time.sleep(1)
            تسویر.click()

            while not os.path.isfile(راستہ_نتیجہ):
                pass

            with zipfile.ZipFile(راستہ_نتیجہ) as زیپ:
                زیپ.extractall(path=راستہ_کا_نام)

            os.remove(راستہ_نتیجہ)

            فایئرفاکس.close()

            for م in os.listdir(راستہ_کا_نام):
                نام = os.path.splitext(م)[0]
                if calendar.isleap(2000 + int(نام[-4:-2])) != calendar.isleap(سال):
                    os.remove(م)
