import os
import shutil
import time
import zipfile

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .مرکسم۵ import مرکسم۵


class مرکسم۵_جال(مرکسم۵):

    def __init__(خود):

        super().__init__()

        خود.اختیار_فایئرفاکس = webdriver.FirefoxProfile()
        خود.اختیار_فایئرفاکس.set_preference('browser.download.folderList', 2)
        خود.اختیار_فایئرفاکس.set_preference('browser.download.manager.showWhenStarting', False)
        خود.اختیار_فایئرفاکس.set_preference('browser.download.dir', خود.راستہ)
        خود.اختیار_فایئرفاکس.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

    def _کوائف_بنانا(خود, سلسلہ_سال, چوڑائی, طول, خاکے):

        نام = 'TQDR'
        راستہ_نتیجہ = os.path.join(خود.راستہ, '{}.zip'.format(نام))

        for سال in سلسلہ_سال:

            فایئرفاکس = webdriver.Firefox(firefox_profile=خود.اختیار_فایئرفاکس)
            فایئرفاکس.get("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3")
            assert "MarkSim" in فایئرفاکس.title

            فایئرفاکس.find_element_by_name('latitude').send_keys(str(طول))

            فایئرفاکس.find_element_by_name('longitude').send_keys(str(چوڑائی))

            فایئرفاکس.find_element_by_name('place').send_keys(نام)

            فایئرفاکس.find_element_by_link_text('Select All Models').click()

            فایئرفاکس.find_element_by_xpath('//input[@value="{}"]'.format(خاکے)).click()

            فایئرفاکس.find_element_by_name('yearsimulation').send_keys(str(سال))

            فایئرفاکس.find_element_by_name('numrep').send_keys(str(10))

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

            راستہ_کا_نام = os.path.join(خود.راستہ, 'TQDR_11111111111111111_{}_{}'.format(خاکے, سال))
            if os.path.isdir(راستہ_کا_نام):
                shutil.rmtree(راستہ_کا_نام)

            os.makedirs(راستہ_کا_نام)

            with zipfile.ZipFile(راستہ_نتیجہ) as az:
                az.extractall(path=راستہ_کا_نام)

            os.remove(راستہ_نتیجہ)

            فایئرفاکس.close()
