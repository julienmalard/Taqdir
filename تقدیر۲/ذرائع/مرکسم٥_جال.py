import os
import shutil
import tempfile
import time
import zipfile

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from எண்ணிக்கை import எண்ணுக்கு

from تقدیر۲.ذریعہ import ذریعہ
from .مرکسم۵ import _خاکے_مرکسم


class مرکسم۵_جال(ذریعہ):

    def __init__(خود):

        خود.profile = webdriver.FirefoxProfile()
        خود.profile.set_preference('browser.download.folderList', 2)  # custom location
        خود.profile.set_preference('browser.download.manager.showWhenStarting', False)
        خود.tmp = tempfile.mkdtemp()
        خود.profile.set_preference('browser.download.dir', خود.tmp)
        خود.profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

    def آدادوشمار_پانا(خود, سے, تک, چوڑائی, طول, بلندی, خاکے='۸۔۵ََ'):

        خاکے = எண்ணுக்கு(خاکے)
        if خاکے not in _خاکے_مرکسم:
            return
        else:
            خاکے = 'rcp' + str(خاکے).replace('.', '')

        سالیں = range(سے.year, تک.year + 1)

        TQDR = 'TQDR'
        descarg = os.path.join(خود.tmp, '{}.zip'.format(TQDR))

        for سال in سالیں:

            driver = webdriver.Firefox(firefox_profile=خود.profile)
            driver.get("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3")
            assert "MarkSim" in driver.title

            driver.find_element_by_name('latitude').send_keys(str(طول))

            driver.find_element_by_name('longitude').send_keys(str(چوڑائی))

            driver.find_element_by_name('place').send_keys(TQDR)

            driver.find_element_by_link_text('Select All Models').click()

            driver.find_element_by_xpath('//input[@value="{}"]'.format(خاکے)).click()

            driver.find_element_by_name('yearsimulation').send_keys(str(سال))

            driver.find_element_by_name('numrep').send_keys(str(n_reps))

            driver.find_element_by_id('BtnRun').click()

            if os.path.isfile(descarg):
                os.remove(descarg)

            listo = False
            while not listo:
                try:
                    driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[1]/td[1]/form/div[2]/img')
                    listo = True
                except NoSuchElementException:
                    pass

            listo = False
            while not listo:
                try:
                    img = driver.find_element_by_xpath('//a[img/@src="images/zip-icon.jpg"]')
                    img.click()
                    listo = True
                except:
                    pass

            time.sleep(1)
            img.click()

            while not os.path.isfile(descarg):
                pass

            nombre_dir = 'TQDR_11111111111111111_{}_{}'.format(خاکے, سال)
            direc_final = os.path.join(خود.tmp, nombre_dir)
            if os.path.isdir(direc_final):
                shutil.rmtree(direc_final)

            os.makedirs(direc_final)

            with zipfile.ZipFile(descarg) as az:
                az.extractall(path=direc_final)

            os.remove(descarg)

            driver.close()
