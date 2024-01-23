import time
import PIL
from PIL import ImageDraw

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions, Chrome



def create_image(prompt, username="defualt_username", password_real="defualt_password", path="defualt/path/to/image.jpg"): # has to be a jpg
    # URL for the login page
    login_url = "https://playgroundai.com/create"

    # Configure the Selenium WebDriver (here we're using Chrome)


    # Configure undetected Chrome WebDriver options
    options = ChromeOptions()

    options.add_argument("--disable-automation")

    link = None

    # Create undetected Chrome WebDriver
    driver = Chrome(options=options, driver_executable_path='driver/exectuable/path')

    def log_in(driver):
        button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[2]/div/button")
        button.click()

        wait = WebDriverWait(driver, 15)
        textbox = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")))
        textbox.send_keys(username)
        textbox.send_keys(Keys.RETURN)

        password = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")))
        password.send_keys(password_real)
        password.send_keys(Keys.RETURN)

        success_element = wait.until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))
        return success_element

    try:
        # Open the login URL
        driver.get(login_url)

        success_element = log_in(driver)
        success_element.send_keys(prompt)
        success_element.send_keys(Keys.LEFT_CONTROL, Keys.RETURN)
        success_element.send_keys(Keys.LEFT_CONTROL, 'a')
        success_element.send_keys(Keys.DELETE)
        # Check if the login was successful by looking for a specific element
        wait = WebDriverWait(driver, 15)

        img = driver.find_elements(By.XPATH, '//img')
        i = 0
        while True:
            img = driver.find_elements(By.XPATH, '//img')
            if 'data:image/jpg' in img[i].get_attribute('src'):
                break

            if i >= len(img):
                i = 0

            i += 1
            if i == len(img):
                time.sleep(2)  # Wait for elements to potentially load
                i = 0
            else:
                time.sleep(0.2)

            sleeps += 1
            print(sleeps)
        #img = wait.until(EC.element_to_be_clickable((By.XPATH, '//img')))


        """
        try:
            skip = driver.find_element(By.CLASS_NAME, 'RateImageModal_TopBarButton_nyGvA')
            skip.click()
        except NoSuchElementException:
            pass
            """




        src = []
        for image in img:
            if ('data:image/jpg' in image.get_attribute('src')):
                src.append(image.get_attribute('src'))

        link = src[0]
        #link = img.get_attribute('src')







    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

    if not(link == None):
        #return str(link)
        import urllib
        urllib.request.urlretrieve(str(link), path)
        return path
    else:
        return "An Error Occured, Please try again"
