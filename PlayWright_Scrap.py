
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
# A new person object is created. Its __init__ method is called, which is auto-generated by the dataclass decorator.
import pandas as pd
import argparse

#__init__ use karva vagar 
@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    # viv_name: str = None

@dataclass
class BusinessList:
    business_list : list[Business] = field(default_factory=list)
    
    def dataframe(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")
    
    def create_file(self, filename):
     
        self.dataframe().to_excel(f'{filename}.xlsx')
        self.dataframe().to_csv(f'{filename}.csv')
    
def main():
    
    with sync_playwright() as p:
        
        #Browser Open 
        # browser = p.chromium.launch(headless=False)

        #without Browser open
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto('https://www.google.com/maps', timeout=60000)
       
        page.wait_for_timeout(5000)
        
        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)
        
        page.keyboard.press('Enter') # click event fire on search click uper
        page.wait_for_timeout(5000)
        
        # scrolling 
        page.hover('(//div[@role="article"])[1]')#div tag no child link tag par mouse lai java mate 

      
        
        business_obj = BusinessList()
        
        # scraping
        for listing in page.locator('//div[@role="article"]').all()[:total]:
        
            listing.click()
            page.wait_for_timeout(5000)
            
            # name_xpath = '//h1[contains(@class, "fontHeadlineLarge")]'
            name_xpath = '//h1[contains(@class,"fontHeadlineLarge")]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_span_xpath = '//span[@role="img"]'
            # viv_name = '//button[@data-review-id="ChZDSUhNMG9nS0VJQ0FnSURnZzZXSkJnEAE"]//div[contains(@class, "d4r55")]'
            business = Business()
            
            if page.locator(name_xpath).count() > 0:
                business.name = page.locator(name_xpath).inner_text()
            else:
                business.name = '' #na hoy to blank 
            if page.locator(address_xpath).count() > 0:
                business.address = page.locator(address_xpath).inner_text()
            else:
                business.address = ''
            if page.locator(website_xpath).count() > 0:
                business.website = page.locator(website_xpath).inner_text()
            else:
                business.website = ''
            if page.locator(phone_number_xpath).count() > 0:
                business.phone_number = page.locator(phone_number_xpath).inner_text()
                # business.viv_name=page.locator(viv_name).inner_text()
            else:
                business.phone_number = ''
            if listing.locator(reviews_span_xpath).count() > 0:
                business.reviews_average = float(listing.locator(reviews_span_xpath).get_attribute('aria-label').split()[0].replace(',','.').strip())
                business.reviews_count = int(listing.locator(reviews_span_xpath).get_attribute('aria-label').split()[2].strip())
            else:
                business.reviews_average = ''
                business.reviews_count = ''
                
            business_obj.business_list.append(business) # The business_list attribute is initialized with the provided list of Business objects
       
        business_obj.create_file('GVP_DATA')
        
        browser.close()
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    
    if args.search:
        search_for = args.search
    else:
        search_for = 'Ahemdabad,EmergingFive'
    
    # total number of products to scrape. Default is 10
    if args.total:
        total = args.total
    else:
        total = 10
        
    main()
