# flight_test.py
# Headless Selenium test for BlazeDemo (works in Gitpod)
import shutil
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://blazedemo.com/"

def get_chrome_and_driver():
    chrome_binary = shutil.which("chromium") or shutil.which("google-chrome") or shutil.which("chrome")
    driver_path  = shutil.which("chromedriver")
    if not chrome_binary:
        raise RuntimeError("Chromium not found in environment.")
    if not driver_path:
        raise RuntimeError("chromedriver not found in environment.")
    return chrome_binary, driver_path

def run_test(from_city="Boston", to_city="Rome"):
    chrome_binary, driver_path = get_chrome_and_driver()

    options = Options()
    options.binary_location = chrome_binary
    # use --headless on some images if --headless=new fails
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(BASE_URL)

        Select(driver.find_element(By.NAME, "fromPort")).select_by_visible_text(from_city)
        Select(driver.find_element(By.NAME, "toPort")).select_by_visible_text(to_city)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        assert len(rows) > 0, "No flights found in results."
        driver.find_elements(By.CSS_SELECTOR, "table tbody tr td input[type='submit']")[0].click()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        driver.find_element(By.ID, "inputName").send_keys("Test User")
        driver.find_element(By.ID, "address").send_keys("123 Test Street")
        driver.find_element(By.ID, "city").send_keys("Test City")
        driver.find_element(By.ID, "state").send_keys("TS")
        driver.find_element(By.ID, "zipCode").send_keys("000000")
        driver.find_element(By.ID, "creditCardNumber").send_keys("4111111111111111")
        m = driver.find_element(By.ID, "creditCardMonth"); m.clear(); m.send_keys("12")
        y = driver.find_element(By.ID, "creditCardYear");  y.clear(); y.send_keys("2028")
        driver.find_element(By.ID, "nameOnCard").send_keys("Test User")

        cb = driver.find_element(By.ID, "rememberMe")
        if not cb.is_selected():
            cb.click()

        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        title = driver.find_element(By.TAG_NAME, "h1").text
        assert "Thank you for your purchase" in title, "Confirmation title not found."

        purchase_id = driver.find_element(By.CSS_SELECTOR, "table tbody tr td:nth-child(2)").text.strip()
        assert purchase_id != "", "Purchase ID missing."
        print("✅ Test passed! Purchase ID:", purchase_id)
        return 0
    except Exception as e:
        print("❌ Test failed:", e)
        return 1
    finally:
        driver.quit()

if __name__ == "__main__":
    f = sys.argv[1] if len(sys.argv) > 1 else "Boston"
    t = sys.argv[2] if len(sys.argv) > 2 else "Rome"
    code = run_test(f, t)
    sys.exit(code)
