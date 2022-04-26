from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import NoSuchElementException
from sys import exit
import time
import pickle


def UpdateChromeDriver():
    chromeVersion = SessionNotCreated[SessionNotCreated.find('Current browser version is'):SessionNotCreated.find('with binary')]
    chromeVersion = chromeVersion[len('Current browser version is '):len(chromeVersion)-1]
    chromeUrl = f'https://chromedriver.storage.googleapis.com/{chromeVersion}/chromedriver_win32.zip'
    print('Please follow this link and unzip chromedriver.exe into your application folder:')
    print(chromeUrl)

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

def autoActivateOrderFunction():
        driver.find_element_by_css_selector('.tc-item.warning').click()
        if not driver.find_element_by_xpath(f"/html[1]/body[1]/div[2]/div[1]/div[1]/div[2]/form[1]/div[6]/div[1]/label[1]/i[1]").is_selected():
            driver.find_element_by_xpath(f"/html[1]/body[1]/div[2]/div[1]/div[1]/div[2]/form[1]/div[6]/div[1]/label[1]/i[1]").click()
        driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[1]/div[1]/div[2]/form[1]/div[7]/button[1]").click()
        print('[FPA] Активировал лот')
        time.sleep(0.25)

def firstStart(array):
    time.sleep(0.1)
    array.append(driver.current_url)
    return array
    
    
def raiseOrder(flag):
    if check_exist_by_css('.tc-item.warning') and flag:
        print('вошли')
        autoActivateOrderFunction()
    driver.find_element_by_xpath("//button[contains(text(),'Поднять предложения')]").click()
    #{!} не рассмотрен случай когда нажимается кнопка только на 1 товар(без списка то есть)
    if not check_exist_by_xpath("//div[@class='ajax-alert ajax-alert-danger']"):
        rid = 0
        while True:
            rid += 1
            try:
                if not driver.find_element_by_xpath(f"/html/body/div[2]/div/div/div[2]/div/div[{rid}]/label/input").is_selected():
                    driver.find_element_by_xpath(f"/html/body/div[2]/div/div/div[2]/div/div[{rid}]/label").click()
            except Exception:
                break
        driver.find_element_by_xpath(f"//button[@class='btn btn-primary btn-block js-lot-raise-ex']").click()
    return 0
    
def main():
    print('FunPay Assistant by MRossa')
    #delay = int(input('[FPA] Введите вашу задержку (в минутах)')) # отголоски интерфейса
    delay = 10 * 60 # стандарт 10 минут
    autoActivateOrder = True
    FirtsStartFlag = True
    links = []
    driver.implicitly_wait(2)
    try:  
        driver.get('https://funpay.ru/account/login')
        for cookie in pickle.load(open('cookie', 'rb')):
            driver.add_cookie(cookie)
        driver.refresh()
        print('[FPA] Вошёл в аккаунт')
        driver.get('https://funpay.ru/users/3302780/')      # тут ссылка на свой аккаунт
        timer_min = 0
        timer_hour = 0
        timer_string = '0 часов 0 минут'
        while True:
            if FirtsStartFlag:
                i = 1
                print('[FPA] Начинаю проход по лотам')
                while True:
                    i += 1
                    try:
                        driver.find_element_by_xpath(f"(//i[@class='fa fa-pen'])[{i}]").click()
                        firstStart(links)
                        driver.get('https://funpay.ru/users/3302780/')
                    except NoSuchElementException:
                        break
                print(links,' ', len(links))
                FirtsStartFlag = False
            for url in links:
                driver.get(url)
                raiseOrder(autoActivateOrder)
            pickle.dump(driver.get_cookies(), open('cookie', 'wb')) # сохранение куки
            print(f'[FPA] Жду {delay//60} минут (Всего работаю: {timer_string})')
            time.sleep(delay)
            timer_min += delay // 60
            if timer_min % 60 == 0:
                timer_min = 0
                timer_hour += 1
            timer_string = f'{timer_hour} часов, {timer_min} минут'
            
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


###########START WEB DRIVER###########
try:
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

    driver = webdriver.Chrome(options = options)
    
except SessionNotCreatedException as SessionNotCreated:
        SessionNotCreated = str(SessionNotCreated)
        if SessionNotCreated.find('This version of ChromeDriver only supports'):
            print('Your version chromedriver is out of date.')
            UpdateChromeDriver()
            exit()
            

########################################

if __name__ == '__main__':
    main()
    
