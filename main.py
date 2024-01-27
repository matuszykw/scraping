from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

chromedriver_path = r"C:\Selenium_Drivers\chromedriver.exe"
chrome_service = ChromeService(chromedriver_path)
driver = webdriver.Chrome(service=chrome_service)
driver.get("https://www.google.com")