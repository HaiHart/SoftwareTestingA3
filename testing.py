import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select as Sel
import os
from datetime import datetime
from excelDriver import Excel 

PATH=".\chromedriver.exe"
USER="jackson@gmail.com"
PASSWORD="donQuiote3"
ADDRESS="688 Main.st Saint Rows NJ USA"
LOGIN="https://magento.softwaretestingboard.com/customer/account/login"

class Selen:
  def __init__(self):
    self.driver = None
    self.options = Options()
    self.options.add_experimental_option("detach", True)
    self.options.add_argument('headless')
    self.options.add_argument('--ignore-certificate-errors')
    self.options.add_argument('--ignore-ssl-errors')
    self.options.add_argument('--window-size=1920,1080')
     
    self.service = Service(PATH)
    
  def setup(self):
    self.driver = webdriver.Chrome(service=self.service, chrome_options=self.options)
    
  def passwordStrengthDTT(self, id, i, o, result):
    self.setup()
    self.driver.get("https://magento.softwaretestingboard.com/customer/account/create/")
    passwordInput = self.driver.find_element(By.ID, "password")
    try:
      time.sleep(2)
      passwordStrength = self.driver.find_element(By.ID, 'password-strength-meter-label') 
      passwordInput.clear()
      passwordInput.send_keys(i)
      print(passwordStrength.text == o)
      result.append([id, o, passwordStrength.text, passwordStrength.text == o])
    except TimeoutException:
      print("Loading took too much time!")
    self.driver.quit()
  
  def nonFunctional(self, eta_time, result):
    self.setup()
    self.driver.get(LOGIN)
    self.driver.find_element("id","email").send_keys(USER)
    self.driver.find_element("id","pass").send_keys(PASSWORD)
    self.driver.find_element("id","send2").click()
    try:
      time.sleep(1)
      self.driver.get("https://magento.softwaretestingboard.com/radiant-tee.html")
      # print('check_1')
      time.sleep(2)
      self.driver.find_element(By.ID,"option-label-size-143-item-166").click()
      self.driver.find_element(By.ID,"option-label-color-93-item-57").click()
      self.driver.find_element(By.ID,"product-addtocart-button").click()
      time.sleep(5)
      self.driver.find_element(By.CLASS_NAME,"minicart-wrapper").click()
      # print('check_2')
      time.sleep(2)
      self.driver.find_element(By.ID,"top-cart-btn-checkout").click()
      # print('check_3')
      
      time.sleep(5)
      if self.driver.find_elements(By.CLASS_NAME, "new-address-popup"):
        print(True)
        # self.driver.find_element(By.CLASS_NAME, "action action-show-popup").click()
      else:
        self.driver.find_element(By.NAME,"street[0]").send_keys(ADDRESS)
        # print('check_4')
        self.driver.find_element(By.NAME,"city").send_keys("New Jersey")
        # print('check_5')
        State = Sel(self.driver.find_element(By.NAME,"region_id"))
        # print('check_6')
        State.select_by_visible_text("New Jersey")
        # print('check_7')
        self.driver.find_element(By.NAME,"postcode").send_keys("02222222222")
        # print('check_8')
        self.driver.find_element(By.NAME,"telephone").send_keys("02222222222")
        # print('check_9')
      self.driver.find_element(By.NAME,"ko_unique_2").click()
      # print('check_10')      
      # self.driver.find_element(By.ID,"shipping-method-buttons-container").click()
      self.driver.find_element(By.CSS_SELECTOR,".button.action.continue.primary").click()
      # print('check_11')
      
      time.sleep(5)
      
      # self.driver.find_element(By.XPATH,"/html/body/div[3]/main/div[2]/div/div[2]/div[4]/ol/li[3]/div/form/fieldset/div[1]/div/div/div[2]/div[2]/div[4]/div/button").click()
      # if self.driver.find_elements(By.CLASS_NAME, "payment-method-content"):
      #   print("YES")
      # else:
      #   with open("page.html","w") as f:
      #     f.write(self.driver.find_element(By.TAG_NAME,"html").get_attribute("innerHTML"))
      start=datetime.now()
      self.driver.find_element(By.CLASS_NAME,"checkout").click()
      # self.driver.find_element(By.XPATH,"//button[@title='Place Order']").click()
      element_present = EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Thank you for your purchase!')]"))
      WebDriverWait(self.driver, eta_time).until(element_present)
      res = (datetime.now()-start)
      res = res.seconds
      if (res>eta_time ):
        result.append(["Slower", res, res-eta_time])
      else:
        result.append(["Faster", res, res-eta_time])

    except TimeoutException:
      print("connection timedout")
    except Exception as e:
      print("error occrured:",e)
    self.driver.quit()
      

class RunTest:
  def __init__(self):
    pass
  
  def runDTT(self):
    if os.path.exists('Output/DTT.xlsx'):
      os.remove('Output/DTT.xlsx')

    result = [['Testcase', 'Expected', 'Got', 'Result']]
    instance = Selen()
    excel = Excel("Input/DTT.xlsx")
    DTTdata = excel.readData("Input")

    for testcase in DTTdata:
      instance.passwordStrengthDTT(testcase[0], testcase[1], testcase[2], result)
  
    excel.writeData(result, "DTT")
  def runNonFunc(self):
    if os.path.exists('Output/NF.xlsx'):
      os.remove('Output/NF.xlsx')
    result = [['Eval', 'Backend', 'Diff']]
    instance = Selen()
    excel = Excel("Input/NF.xlsx")
    NFdata = excel.readData("Input")
    print(NFdata)
    for testcase in NFdata:
      instance.nonFunctional(5, result)
    excel.writeData(result, "NF")
    
   
if __name__=="__main__": 
  instance = RunTest()
  instance.runNonFunc()





