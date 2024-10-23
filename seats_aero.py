from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import json
from datetime import datetime
from bs4 import BeautifulSoup
        
## relative to the flight card         
class PointYeahConstants:
    ANCHOR_XPATH = '//span[contains(text(), "View Detail")]'
    ANCHOR_TO_FLIGHT_CARD_XPATH = '../../../../../..'
    DATE_XPATH = '//div[1]/div/div[1]/div/div[1]/div[2]/span[1]'
    DAY_XPATH = '//div[1]/div/div[1]/div/div[1]/div[2]/span[2]'
    TIMING_XPATH = '//div[1]/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div'
    AIRLINE_NAME_XPATH = '//div[1]/div/div[1]/div/div[1]/div[3]/div[1]/div[2]'
    CLASS_XPATH = '//div[1]/div/div[1]/div/div[1]/div[3]/div[1]/div[3]/div'
    SEATS_LEFT_XPATH = '//div[1]/div/div[1]/div/div[1]/div[3]/div[1]/div[4]'
    DURATION_XPATH = '//div[1]/div/div[1]/div/div[1]/div[3]/div[2]/div[1]'
    STOPS_XPATH = '//div[1]/div/div[1]/div/div[1]/div[3]/div[2]/div[1]'
    FLIGHT_PATH_XPATH = '//div[1]/div/div[1]/div/div[1]/div[3]/div[2]/div[2]'
    POINTS_COST_XPATH = '//div[2]/div/div[1]/div[2]/div/div/div[2]/div[1]'

    
class FlightScraper:
    URL = 'https://www.pointsyeah.com/'
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        
    def authenticate(self):
        self.driver.get(self.URL)
        time.sleep(1)
        requires_auth = self.driver.find_element(By.XPATH, '//*[contains(text(), "Login/Sign up")]')
        if not requires_auth.is_displayed():
            return

        requires_auth.click()
        # self.driver.find_element(By.XPATH, '//*[contains(text(), "Log in")]').click()
        popup = self.driver.find_element(By.CLASS_NAME, 'popup-authenticator')
        print(popup)
        # login with email and password
        self.driver.find_element(By.NAME, 'username').send_keys('bboygraffity2002@gmail.com')
        self.driver.find_element(By.NAME, 'password').send_keys('PointsYeah@2024')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(5)
        
    def scrape_flights(self):
        print("scraping flights time")
        url = "https://www.pointsyeah.com/search?cabins=Economy%2CPremium+Economy%2CBusiness%2CFirst&cabin=Economy&banks=Amex%2CBilt%2CCapital+One%2CChase%2CCiti%2CWF&airlineProgram=AR%2CAM%2CAC%2CKL%2CAS%2CAA%2CAV%2CDL%2CEK%2CEY%2CF9%2CIB%2CB6%2CQF%2CSK%2CNK%2CTP%2CTK%2CUA%2CVS%2CVA&tripType=1&adults=1&children=0&departure=JFK&arrival=MHT&departDate=2024-10-25&departDateSec=2024-10-25&multiday=false&bankpromotion=false&pointpromotion=false"
        self.driver.get(url)
    
        time.sleep(10)
        # print page source
        main_element_1 = self.driver.find_element(By.CSS_SELECTOR, f'div[data-index="0"]')
        print(main_element_1.get_attribute('innerHTML'))
        
        # main_element_2 = self.driver.find_element(By.CSS_SELECTOR, f'div[data-index="1"]')
        # print(main_element_2.text)
        return []
    
        flight_cards = self.driver.find_elements(By.XPATH, PointYeahConstants.ANCHOR_XPATH)
        print(f"length: {len(flight_cards)}")
        
        flights_data = []
        
        for card in flight_cards:
            print(f"card: {card.text}")
            main_element = card.find_element(By.XPATH, PointYeahConstants.ANCHOR_TO_FLIGHT_CARD_XPATH)
            # print data
            try:
                date  = main_element.find_element(By.XPATH, PointYeahConstants.DATE_XPATH).text
                day = main_element.find_element(By.XPATH, PointYeahConstants.DAY_XPATH).text
                timing = main_element.find_element(By.XPATH, PointYeahConstants.TIMING_XPATH).text
                airline_name = main_element.find_element(By.XPATH, PointYeahConstants.AIRLINE_NAME_XPATH).text
                class_ = main_element.find_element(By.XPATH, PointYeahConstants.CLASS_XPATH).text
                seats_left = main_element.find_element(By.XPATH, PointYeahConstants.SEATS_LEFT_XPATH).text
                duration = main_element.find_element(By.XPATH, PointYeahConstants.DURATION_XPATH).text
                stops = main_element.find_element(By.XPATH, PointYeahConstants.STOPS_XPATH).text
                flight_path = main_element.find_element(By.XPATH, PointYeahConstants.FLIGHT_PATH_XPATH).text
                points_cost = main_element.find_element(By.XPATH, PointYeahConstants.POINTS_COST_XPATH).text

                flights_data.append({
                    'date': date,
                    'day': day,
                    'timing': timing,
                    'airline_name': airline_name,
                    'class_': class_,
                    'seats_left': seats_left,
                    'duration': duration,
                    'stops': stops,
                    'flight_path': flight_path,
                    'points_cost': points_cost
                })
            except Exception as e:
                print(f"Error: {e}")
                return []
        
        time.sleep(10)
        return flights_data
        
    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = FlightScraper()
    scraper.authenticate()
    scraper.scrape_flights()
    scraper.close()