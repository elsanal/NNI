from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from find_cities import get_neighbourhood_towns
import re
import pandas as pd

def login_facebook(email, pwd):
    driver = webdriver.Chrome()

    # Navigate to Facebook login page
    driver.get("https://www.facebook.com")

    # Find email and password fields, and login button
    email_input = driver.find_element("id","email")
    password_input = driver.find_element("id","pass")
    login_button = driver.find_element("name","login")

    # Enter your email and password here
    email_input.send_keys(email)
    password_input.send_keys(pwd)

    # Click on the login button
    login_button.click()
    
    #return the driver with facebook
    return driver

    
def find_facebook_groups(email, pwd, town, radius):
    driver = login_facebook(email, pwd)
    locations = get_neighbourhood_towns(town,  radius)
    locations.append(town)
    time.sleep(50)  # import time
    # Visit the desired URL directly
    driver.get(f"https://www.facebook.com/search/groups/?q={town}&filters=community%20OR%20town")

    # Define the JavaScript code for scrolling the page
    scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
    final_groups = []
    # Scroll the page multiple times (e.g., 5 times)
    for _ in range(20):
         # Execute the JavaScript code to scroll the page
        driver.execute_script(scroll_script) 
        time.sleep(5)
        # get list of groups 
    time.sleep(5)  # import time
    groups = driver.find_elements(By.CLASS_NAME, 'x1yztbdb')
    #  Print out the group names
    #print(element_groups)
    for idx, group in enumerate(groups):
        full_text = group.text
        full_text = full_text.split('\n')
        if "Private" in str(full_text[1]) and all(keyword not in str(full_text[0]).lower() for keyword in ['sell', 'buy', 'business', 'trader', 'trade', 'sale']): 
            try:
                url = group.find_element(By.CSS_SELECTOR, "a")
                url = url.get_attribute("href")
                final_groups.append({
                    'name': full_text[0],
                    'privacy': "Private",
                    "Number": str(full_text[1])[10:],
                    'url': url,
                    'radius': radius  
                })
                print(url.get_attribute("href"))
            except:
                pass    
       
          
    output = []    
    for element in final_groups:
        #if 'groups' in link:
        driver.get(element['url'])
        about = driver.find_element(By.CLASS_NAME, "x1yztbdb")
        time.sleep(3)
        pres = about.text
        matching_location = find_matching_location(pres, locations)
        if matching_location:
            element['location'] = matching_location
            output.append(element)
    return output        


def find_matching_location(text, locations):
    # Regular expression pattern to match city or town name
    pattern = r'[A-Z][a-z]+(?: [A-Z][a-z]+)*(?=, [A-Z][a-z]+)'
    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    # Check if any match is in the list of locations
    for match in matches:
        if match in locations:
            return match
    # If no matches are found in the list of locations
    return None


email = "YOUR_FACEBOOK_EMAIL"
pwd = "YOUR_PASSWORD"
result = find_facebook_groups(email=email, pwd=pwd, town="Franklin", radius=300)    
print(result)
data = pd.DataFrame(result) 
data.to_csv('result.csv')
# # Close the browser window
k = input("Yes we can : ")
# driver.quit()





