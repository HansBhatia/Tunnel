from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import json
from datetime import datetime
 
## relative to the flight card         
class PointHoundConstants:
    ANCHOR_XPATH = '//div[contains(text(), "¢ per point")]'
    ANCHOR_TO_FLIGHT_CARD_XPATH = '../../../../../..'
    DATE_XPATH = '//div[2]/p[1]'
    DAY_XPATH = '//div[2]/p[2]'
    TIMING_XPATH = '//div[3]/h5'
    AIRLINE_NAME_XPATH = '//div[3]/p[1]'
    CLASS_XPATH = '//div[3]/p[2]'
    SEATS_LEFT_XPATH = '//div[3]/p[3]'
    DURATION_XPATH = '//div[4]/p'
    STOPS_XPATH = '//div[5]/p'
    FLIGHT_PATH_XPATH = '//div[4]/div/p[1]'
    POINTS_COST_XPATH = '//div[8]/h5'
    RETAIL_PRICE_XPATH = '//div[7]/div/p'
    FEES_XPATH = '//div[8]/span'

class FlightScraper:
    def __init__(self):
        # Set up Chrome options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Run in headless mode
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
    def setup_driver(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def scrape_flights(self, url):
        try:
            self.setup_driver()
            print("Starting scrape...")
            
            # Load the page
            self.driver.get(url)
            
            # Let the dynamic content load fully
            time.sleep(5)
            
            # Find all flight cards
            flight_cards = self.driver.find_elements(By.XPATH, PointHoundConstants.ANCHOR_XPATH)
            
            print(f"length: {len(flight_cards)}")
            flights_data = []
            
            for card in flight_cards:
                print(f"card: {card.text}")
                main_element = card.find_element(By.XPATH, PointHoundConstants.ANCHOR_TO_FLIGHT_CARD_XPATH)
                # print data
                try:
                    date  = main_element.find_element(By.XPATH, PointHoundConstants.DATE_XPATH).text
                    day = main_element.find_element(By.XPATH, PointHoundConstants.DAY_XPATH).text
                    timing = main_element.find_element(By.XPATH, PointHoundConstants.TIMING_XPATH).text
                    airline_name = main_element.find_element(By.XPATH, PointHoundConstants.AIRLINE_NAME_XPATH).text
                    class_ = main_element.find_element(By.XPATH, PointHoundConstants.CLASS_XPATH).text
                    seats_left = main_element.find_element(By.XPATH, PointHoundConstants.SEATS_LEFT_XPATH).text
                    duration = main_element.find_element(By.XPATH, PointHoundConstants.DURATION_XPATH).text
                    stops = main_element.find_element(By.XPATH, PointHoundConstants.STOPS_XPATH).text
                    flight_path = main_element.find_element(By.XPATH, PointHoundConstants.FLIGHT_PATH_XPATH).text
                    points_cost = main_element.find_element(By.XPATH, PointHoundConstants.POINTS_COST_XPATH).text
                    retail_price = main_element.find_element(By.XPATH, PointHoundConstants.RETAIL_PRICE_XPATH).text
                    fees = main_element.find_element(By.XPATH, PointHoundConstants.FEES_XPATH).text
                    
                    flights_data.append({
                        "date": date,
                        "day": day,
                        "timing": timing,
                        "airline_name": airline_name,
                        "class_": class_,
                        "seats_left": seats_left,
                        "duration": duration,
                        "stops": stops,
                        "flight_path": flight_path,
                        "points_cost": points_cost,
                        "retail_price": retail_price,
                        "fees": fees,
                    })
                except Exception as e:
                    print(main_element.get_attribute('innerHTML'))
                    print(f"Error parsing flight card: {str(e)}")
                    continue
            return flights_data
        except TimeoutException:
            print("Timeout waiting for flight results to load")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
        finally:
            self.driver.quit()
    
    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass

if __name__ == "__main__":
    url = "https://www.pointhound.com/flights?dateBuffer=false&flightClass=Business+%26+First+Class&originCode=JFK&originName=New+York&destinationCode=BOS&destinationName=Boston&passengerCount=1&departureDate=2024-11-23"
    
    scraper = FlightScraper()
    results = scraper.scrape_flights(url)
    
    if results:
        print(f"Successfully scraped {len(results)} flights")