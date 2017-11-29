import os
import shutil
import time
import zipfile

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

lat = 32.178207
long = 73.217391
lugar = 'Prueba'
n_reps = 10
sem = 1234
l_rcp = [2.6, 4.5, 6.0, 8.5]
l_años = range(2015, 2100)

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/tmp')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

for año in l_años:
    print(año)
    for rcp in l_rcp:

        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get("http://gisweb.ciat.cgiar.org/MarkSimGCM/#tabs-3")
        assert "MarkSim" in driver.title

        tx_rcp = 'rcp' + str(rcp).replace('.', '')
        print(tx_rcp)

        ingr_lat = driver.find_element_by_name('latitude')
        ingr_lat.send_keys(str(lat))

        ingr_long = driver.find_element_by_name('longitude')
        ingr_long.send_keys(str(long))

        ingr_lat = driver.find_element_by_name('place')
        ingr_lat.send_keys(str(lugar))

        todos_mods = driver.find_element_by_link_text('Select All Models')
        todos_mods.click()

        bt_rcp = driver.find_element_by_css_selector("input[type='radio'][value='{}']".format(tx_rcp))
        bt_rcp.click()

        ingr_años = driver.find_element_by_name('yearsimulation')
        ingr_años.send_keys(str(año))

        ingr_reps = driver.find_element_by_name('numrep')
        ingr_reps.send_keys(str(n_reps))

        bt_correr = driver.find_element_by_id('BtnRun')
        bt_correr.click()

        descarg = 'C:\\Users\\jmalar1\\Downloads\\{}.zip'.format(lugar)

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

        nombre_dir = 'TQDR_11111111111111111_{}_{}'.format(tx_rcp, año)
        direc_final = os.path.join('C:\\Users\\jmalar1\\Marksim\\CLI', nombre_dir)
        if os.path.isdir(direc_final):
            shutil.rmtree(direc_final)

        os.makedirs(direc_final)

        with zipfile.ZipFile(descarg) as az:
            az.extractall(path=direc_final)

        os.remove(descarg)

        driver.close()
