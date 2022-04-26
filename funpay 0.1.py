from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pickle

def check_exist_by_xpath(xpath):
    try:
        elem = driver.find_element_by_xpath(xpath)
        return True
    except NoSuchElementException:
        return False

def check_exist_by_css(css):
    try:
        elem = driver.find_element_by_css_selector(css)
        return True
    except NoSuchElementException:
        return False
    
def activating_order():
    driver.find_element_by_css_selector('.tc-item.warning').click()
    driver.find_element_by_xpath("//label[contains(text(),'Активное')]").click()
    driver.find_element_by_xpath("//button[contains(text(),'Сохранить')]").click()
    driver.refresh()
    time.sleep(1)
    print('Активировали товар')



#options
options = webdriver.ChromeOptions()

#change user-agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

#headless mode
#options.add_argument("--headless")

#disable webdriver mode
options.add_argument("--disable-blink-features=AutomationControlled")

#disable automation flag
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options =options)
driver.implicitly_wait(2)

try:  
    driver.get("https://funpay.ru/account/login")
    print('Перешли на страницу логина')
    #for cookie in pickle.load(open("fp cookies", "rb")):
        #driver.add_cookie(cookie)  
    #driver.refresh()
    #print('Залогинились')
    
    input('сохраняем?')
    pickle.dump(driver.get_cookies(), open("fp_cookies_new", "wb"))
    print('сохранили куки')
    time.sleep(100000)
    '''
    timer_min = 0
    timer_hour = 0
    timer_string = '0 часов 0 минут'
    while True:
        print('Проверяем Crossout')
        driver.get("https://funpay.ru/lots/214/trade")
        if check_exist_by_css('.tc-item.warning'):
            activating_order()
        driver.find_element_by_xpath('//*[text()="Поднять предложения"]').click()
        if not check_exist_by_xpath("//div[@class='ajax-alert ajax-alert-danger']"):
            if check_exist_by_xpath("//div[@class='modal-dialog modal-sm']"):
                driver.find_element_by_xpath("//label[contains(text(),'Предметы')]").click()
                driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block js-lot-raise-ex']").click()
            print('Crossout: Успешно поднят!')
        driver.get("https://funpay.ru/lots/244/trade")
        print('Проверяем War Thunder')
        if check_exist_by_css('.tc-item.warning'):
            activating_order()
        driver.find_element_by_xpath('//*[text()="Поднять предложения"]').click()
        if not check_exist_by_xpath("//div[@class='ajax-alert ajax-alert-danger']"):
            if check_exist_by_xpath("//div[@class='modal-dialog modal-sm']"):
                driver.find_element_by_xpath("//label[contains(text(),'Бонус-коды')]").click()
                time.sleep(2)
                driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block js-lot-raise-ex']").click()
        if not check_exist_by_xpath("//div[@class='ajax-alert ajax-alert-danger']"):
            print('War Thunder: Успешно поднят!')
        driver.get("https://funpay.ru/lots/423/trade")
        print('Проверяем Star Conflict')
        if check_exist_by_css('.tc-item.warning'):
            activating_order()
        driver.find_element_by_xpath('//*[text()="Поднять предложения"]').click()
        if not check_exist_by_xpath("//div[@class='ajax-alert ajax-alert-danger']"):
            print('Star Conflict: Успешно поднят!')
        print(f'Ждём 10 минут (Всего работаем: {timer_string})')    
        time.sleep(600)
        timer_min += 10
        if timer_min % 60 == 0:
            timer_min = 0
            timer_hour += 1
        timer_string = f'{timer_hour} часов, {timer_min} минут'
     '''

    
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


