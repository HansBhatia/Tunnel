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
    # flight_scraper = FlightScraper()
    
    eg_html_content = '''<div class="px-[10px]"><div class="mb-6"><div class="flex flex-row items-stretch self-stretch"><div class="mr-[1px] flex flex-1 cursor-pointer self-stretch bg-white shadow-md rounded-l-2xl rounded-r-3xl"><div class="flex w-full flex-col items-center justify-end  gap-4 self-stretch  px-6 py-4 "><div class="flex w-full flex-1 flex-row items-center justify-start "><div class="flex w-full flex-row justify-between self-stretch"><div class="flex  flex-1  items-center gap-8 self-stretch"><div class="size-[3.125rem]"><img class="size-full object-contain" src="https://d1eehocm4fsl24.cloudfront.net/airlines/aa.png" alt=""></div><div class="flex  flex-col items-center  justify-center text-xs leading-[normal] text-black"><span> 10/25</span><span>Fri</span></div><div class="flex items-start gap-8"><div class="flex flex-col items-start gap-0.5"><div class="flex items-start gap-0.5"><div class="  text-sm font-semibold leading-[1.375rem] text-black">7:50 AM - 2:26 PM</div></div><div class=" self-stretch   text-xs leading-[normal] text-black">American Airlines<span> - AA4538</span></div><div class=" self-stretch   text-xs leading-[normal] text-black"><div>Economy</div></div><div class=" self-stretch  text-xs leading-[normal] text-black">Seats Left: 6</div></div><div class="flex flex-col items-start gap-0.5"><div class="  text-sm font-semibold leading-[1.375rem] text-black">6h 36m - 1 stop</div><div class="flex  items-center justify-between text-xs leading-[normal] text-black">JFK - DCA - MHT</div></div></div></div><div class="flex items-center justify-center transition-all duration-300"><svg width="37" height="37" viewBox="0 0 37 37" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M24.7812 15.0797C24.3907 14.6891 23.7575 14.6891 23.367 15.0797L18.4326 20.0141L13.4982 15.0797C13.1077 14.6891 12.4745 14.6891 12.084 15.0797L11.6397 15.524C11.2492 15.9145 11.2492 16.5476 11.6397 16.9382L18.4326 23.7311L25.2255 16.9382C25.616 16.5476 25.616 15.9145 25.2255 15.524L24.7812 15.0797Z" fill="#262626"></path></svg></div></div></div><div class="flex w-full flex-col items-start gap-2 self-stretch border-x-0 border-b-0 border-t border-solid border-t-[#e1e1e1] px-0 pt-2"><div class="flex items-start gap-0.5 self-stretch  p-0 "><div class="flex size-4 max-h-4 max-w-4 shrink-0 grow-0 items-center justify-center"><svg width="16" height="17" viewBox="0 0 16 17" fill="none" class="size-full" xmlns="http://www.w3.org/2000/svg"><path d="M6.77312 12.5142L3.09509 8.76269C2.85836 8.52124 2.86213 8.13362 3.1035 7.89681C3.34501 7.65987 3.7329 7.66366 3.96973 7.90528L6.78169 10.7741L12.0345 5.52127C12.2736 5.28219 12.6612 5.28219 12.9003 5.52127C13.1394 5.76034 13.1394 6.14796 12.9003 6.38704L6.77312 12.5142Z" fill="#686563"></path></svg></div><div class="flex items-center self-stretch text-[14px] font-normal text-[#686563] max-md:text-sm"><div class="font-semibold">Free Cancellation</div></div></div><div class="flex items-start gap-0.5 self-stretch  p-0 "><div class="flex size-4 max-h-4 max-w-4 shrink-0 grow-0 items-center justify-center"><svg width="12" height="11" viewBox="0 0 12 11" fill="none" class="size-full" xmlns="http://www.w3.org/2000/svg"><path d="M0.666504 9.15899C0.666945 9.63355 0.855658 10.0885 1.19122 10.4241C1.52679 10.7597 1.98178 10.9484 2.45634 10.9488H9.54235C9.85596 10.949 10.1641 10.8668 10.4359 10.7104C10.7078 10.554 10.9337 10.3289 11.0912 10.0577C11.2487 9.78645 11.3321 9.47861 11.3332 9.165C11.3342 8.85139 11.2528 8.54301 11.0972 8.27074L7.36589 1.74301C7.22803 1.50234 7.02906 1.30235 6.7891 1.16326C6.54914 1.02418 6.2767 0.950928 5.99934 0.950928C5.72199 0.950928 5.44955 1.02418 5.20959 1.16326C4.96963 1.30235 4.77066 1.50234 4.6328 1.74301L0.903149 8.27074C0.748427 8.54123 0.666865 8.84738 0.666504 9.15899ZM1.76974 8.76736L5.49939 2.23963C5.54957 2.15127 5.62228 2.07778 5.7101 2.02666C5.79792 1.97553 5.89773 1.9486 5.99934 1.9486C6.10096 1.9486 6.20077 1.97553 6.28859 2.02666C6.37641 2.07778 6.44912 2.15127 6.4993 2.23963L10.229 8.76736C10.2976 8.88754 10.3334 9.02364 10.3329 9.16202C10.3323 9.30041 10.2955 9.43622 10.2259 9.55587C10.1564 9.67553 10.0567 9.77481 9.93669 9.84379C9.81672 9.91277 9.68074 9.94902 9.54235 9.94892H2.45634C2.31795 9.94902 2.18197 9.91277 2.062 9.84379C1.94203 9.77481 1.84229 9.67553 1.77276 9.55587C1.70323 9.43622 1.66636 9.30041 1.66582 9.16202C1.66529 9.02364 1.70113 8.88754 1.76974 8.76736Z" fill="#dc2626"></path><path d="M6.49942 4.44946H5.49951V7.11588H6.49942V4.44946Z" fill="#dc2626"></path><path d="M5.99947 8.94913C6.27558 8.94913 6.49942 8.72529 6.49942 8.44917C6.49942 8.17306 6.27558 7.94922 5.99947 7.94922C5.72335 7.94922 5.49951 8.17306 5.49951 8.44917C5.49951 8.72529 5.72335 8.94913 5.99947 8.94913Z" fill="#dc2626"></path></svg></div><div class="flex items-center self-stretch text-[14px] font-normal text-[#686563] max-md:text-sm"><div class=""><span class="font-semibold text-red-600">Warning:</span>&nbsp; Alaska Airlines is undergoing a major website and system upgrade in preparation for a merger and currently has two interfaces running simultaneously. You may randomly encounter either one, especially on mobile. If you don’t see flights through our link, try running a search directly on their site again and our result is accurate</div></div></div></div></div></div><div class="flex min-h-[9.625rem] w-[28.75rem] min-w-[28.75rem] rounded-l-3xl rounded-r-2xl bg-white shadow-md"><div class="flex w-full cursor-pointer  flex-col items-center justify-center self-stretch"><div class="flex items-center justify-between gap-[3.75rem] self-stretch border-x-0 border-b border-t-0 border-solid border-[#e1e1e1] p-4"><div class="flex flex-col items-start gap-2"><div class="relative flex h-[2.0625rem] w-[5.1875rem] items-center justify-center"><img src="https://d1eehocm4fsl24.cloudfront.net/bank/Bilt.png" alt="Bilt" class="aspect-video h-full w-[90%] object-contain"></div></div><div class="flex flex-1 flex-col items-start gap-4"><div class="flex items-center justify-between self-stretch"><div class="flex flex-col items-start justify-center text-xs font-medium text-neutral-800"><div class="text-xs">From </div><div class="flex items-center gap-1"><div class="text-[1.125rem] font-bold leading-[2.125rem]">7,500</div><div class="flex items-center"><div class="">pts</div><div class="">/</div><svg width="11" height="11" viewBox="0 0 11 11" fill="#686563" xmlns="http://www.w3.org/2000/svg"><g id="Group"><path id="Vector" d="M6.78873 5.54871H3.50413C1.65306 5.54871 0.146484 7.05528 0.146484 8.90635V10.3381C0.146484 10.4338 0.224771 10.5121 0.320457 10.5121H9.97251C10.0682 10.5121 10.1465 10.4338 10.1465 10.3381V8.90635C10.1465 7.05528 8.6398 5.54871 6.78873 5.54871Z" fill="currentColor"></path><path id="Vector_2" d="M7.61671 2.5442C7.61671 1.18203 6.50851 0.0737305 5.14625 0.0737305C3.78398 0.0737305 2.67578 1.18193 2.67578 2.5442C2.67578 3.90646 3.78398 5.01466 5.14625 5.01466C6.50851 5.01466 7.61671 3.90646 7.61671 2.5442Z" fill="currentColor"></path></g></svg></div></div></div><button type="button" class="ant-btn css-12kn5qh ant-btn-default ant-btn-color-default ant-btn-variant-outlined btn-grad-orange rounded-full px-3 py-2 font-semibold leading-[1.375rem]"><span>View Detail</span></button></div></div></div><div class="flex flex-col items-start justify-center gap-2 self-stretch p-4 max-md:px-0"><div class="flex flex-col items-start gap-4 self-stretch"><div class="flex flex-row items-center self-stretch gap-9"><div class="flex items-center"><svg width="24" height="47" viewBox="0 0 24 47" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 4.63281C1 6.84195 2.79086 8.63281 5 8.63281C7.20914 8.63281 9 6.84195 9 4.63281C9 2.42367 7.20914 0.632812 5 0.632812C2.79086 0.632812 1 2.42367 1 4.63281ZM5 36.6328H4.25V37.3828H5V36.6328ZM19.5303 37.1631C19.8232 36.8703 19.8232 36.3954 19.5303 36.1025L14.7574 31.3295C14.4645 31.0366 13.9896 31.0366 13.6967 31.3295C13.4038 31.6224 13.4038 32.0973 13.6967 32.3902L17.9393 36.6328L13.6967 40.8755C13.4038 41.1683 13.4038 41.6432 13.6967 41.9361C13.9896 42.229 14.4645 42.229 14.7574 41.9361L19.5303 37.1631ZM4.25 4.63281V36.6328H5.75V4.63281H4.25ZM5 37.3828H19V35.8828H5V37.3828Z" fill="#A1A09F"></path></svg><div class="h-[1.9375rem] w-[5.1875rem] shrink-0 grow-0 cursor-pointer flex-col items-start gap-2"><img src="https://d1eehocm4fsl24.cloudfront.net/programs/as.png" alt="" class="aspect-video size-full object-contain"></div></div><div class="flex flex-1 flex-row items-center justify-between self-stretch max-md:justify-end"><div class="flex items-center gap-1 text-[#262626]"><div class="flex items-center"><div class="font-semibold"><span class="text-[1.125rem] font-bold max-md:text-lg">7,500</span><span class="text-xs font-medium max-md:!text-[17px]"> pts</span></div><div class="text-base">&nbsp;+</div></div><div class="flex items-center font-bold"><span class="text-[1.125rem] font-bold max-md:text-lg">$18.1</span><span class="text-xs font-medium max-md:!text-[17px]">&nbsp;tax</span><span class="text-xs font-medium max-md:!text-[17px]">&nbsp;/&nbsp;</span><svg width="11" height="11" viewBox="0 0 11 11" fill="#686563" xmlns="http://www.w3.org/2000/svg"><g id="Group"><path id="Vector" d="M6.78873 5.54871H3.50413C1.65306 5.54871 0.146484 7.05528 0.146484 8.90635V10.3381C0.146484 10.4338 0.224771 10.5121 0.320457 10.5121H9.97251C10.0682 10.5121 10.1465 10.4338 10.1465 10.3381V8.90635C10.1465 7.05528 8.6398 5.54871 6.78873 5.54871Z" fill="currentColor"></path><path id="Vector_2" d="M7.61671 2.5442C7.61671 1.18203 6.50851 0.0737305 5.14625 0.0737305C3.78398 0.0737305 2.67578 1.18193 2.67578 2.5442C2.67578 3.90646 3.78398 5.01466 5.14625 5.01466C6.50851 5.01466 7.61671 3.90646 7.61671 2.5442Z" fill="currentColor"></path></g></svg></div></div><div class="inline-flex size-8  cursor-pointer  items-center justify-center gap-2.5 rounded-full border border-solid border-orange hover:opacity-60"><svg width="24" height="25" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M15.8158 12.1689L13.5945 9.80342C13.4538 9.64972 13.375 9.44353 13.375 9.22885C13.375 9.01416 13.4538 8.80798 13.5945 8.65427C13.7369 8.50355 13.9295 8.41894 14.1303 8.41894C14.331 8.41894 14.5236 8.50355 14.666 8.65427L18.154 12.3688C18.2956 12.5204 18.375 12.7255 18.375 12.9393C18.375 13.1531 18.2956 13.3582 18.154 13.5098L14.666 17.2244C14.5206 17.3569 14.3336 17.4262 14.1424 17.4183C13.9511 17.4105 13.7697 17.326 13.6344 17.1819C13.499 17.0378 13.4197 16.8446 13.4124 16.6409C13.405 16.4372 13.47 16.2381 13.5945 16.0833L15.8617 13.6689L6.375 13.6689C5.96079 13.6689 5.625 13.3332 5.625 12.9189C5.625 12.5047 5.96079 12.1689 6.375 12.1689L15.8158 12.1689Z" fill="#FF7823"></path></svg></div></div></div><div class="flex flex-col items-start gap-2.5 self-stretch pl-[8.9375rem]"><div class="flex items-center gap-0.5 self-stretch rounded-sm bg-[#faf3ff] p-0"><div class="flex size-4 items-center justify-center p-0"><svg width="11" height="12" viewBox="0 0 11 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.20047 10.9191C4.94453 11.175 4.59705 11.3189 4.23454 11.3189C3.87249 11.3189 3.52502 11.175 3.26862 10.9191L0.469186 8.11962C0.213248 7.86369 0.0693359 7.51621 0.0693359 7.1537C0.0693359 6.79164 0.213248 6.44418 0.469186 6.18777L5.43126 1.2257C5.65987 0.997086 5.96272 0.856812 6.28515 0.830405L8.39871 0.656438C8.79856 0.623648 9.19294 0.768013 9.47666 1.05173L10.336 1.91109C10.6197 2.19481 10.7646 2.58873 10.7313 2.98904L10.5573 5.1026C10.5309 5.42503 10.3907 5.72742 10.1621 5.95649L5.19998 10.9186L5.20047 10.9191Z" fill="#AE24FE"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M3.09489 6.21322C2.9692 6.21322 2.86719 6.1112 2.86719 5.98551C2.86719 5.85982 2.9692 5.75781 3.09489 5.75781H7.73053C7.85622 5.75781 7.95823 5.85982 7.95823 5.98551C7.95823 6.1112 7.85622 6.21322 7.73053 6.21322H3.09489Z" fill="white"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M5.97475 3.90741C6.28489 4.21755 6.28489 4.72077 5.97475 5.0309C5.66461 5.34104 5.16138 5.34104 4.85126 5.0309C4.54112 4.72076 4.54112 4.21754 4.85126 3.90741C5.16139 3.59727 5.66462 3.59727 5.97475 3.90741ZM5.65278 4.22938C5.52025 4.09686 5.3053 4.09686 5.17323 4.22938C5.04071 4.3619 5.04071 4.57686 5.17323 4.70893C5.30575 4.84145 5.52071 4.84145 5.65278 4.70893C5.7853 4.57641 5.7853 4.36145 5.65278 4.22938Z" fill="white"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M5.97474 6.94012C6.28488 7.25026 6.28488 7.75349 5.97474 8.06361C5.6646 8.37374 5.16138 8.37375 4.85125 8.06361C4.54113 7.75348 4.54111 7.25025 4.85125 6.94012C5.16139 6.62998 5.66462 6.62998 5.97474 6.94012ZM5.65277 7.26209C5.52025 7.12957 5.30529 7.12957 5.17322 7.26209C5.0407 7.39462 5.0407 7.60958 5.17322 7.74164C5.30575 7.87416 5.5207 7.87416 5.65277 7.74164C5.78529 7.60912 5.78529 7.39416 5.65277 7.26209Z" fill="white"></path></svg></div><div class="h-[1.125rem] w-[16.4375rem] text-[12px] font-medium text-[#ae24fe] underline">Buy points up to 60% bonus at 1.85 cents per mile</div></div></div></div></div></div></div></div></div></div>'''
    print(f"len html content {len(eg_html_content)}")
    # Parse the HTML content
    soup = BeautifulSoup(eg_html_content, 'html.parser')

    # Find all SVG tags and remove them
    for svg_tag in soup.find_all('svg'):
        svg_tag.decompose()
        
    for tag in soup.find_all(class_=True):
        del tag['class']

    # Output the modified HTML
    print(soup.prettify())
    print(f"len html content pretty {len(soup.prettify())}")
    # print(flight_scraper.authenticate())
    # print(flight_scraper.scrape_flights())
    # scraper = FlightScraper()
    # results = scraper.scrape_flights(url)
    
    # if results:
    #     print(f"Successfully scraped {len(results)} flights")