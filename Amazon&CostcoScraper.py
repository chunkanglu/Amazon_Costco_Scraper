from selenium import webdriver
from bs4 import BeautifulSoup as soup
import requests
import time
import csv
import datetime
import smtplib
from email.message import EmailMessage

DRIVER_PATH = '' # Put Chrome Webdriver path here
driver = webdriver.Chrome(DRIVER_PATH)

def getCostcoData(link):
    driver.get(link)
    try:
        driver.find_element_by_class_name('modal-buttons').click()
    except:
        pass
    time.sleep(18)
    page_html = driver.page_source

    page_soup = soup(page_html, "html.parser")
    try:
        name = page_soup.find("h1", itemprop="name").text
        price = page_soup.find("div", id="pull-right-price").text
        price = price.strip()
        price = price[:-1]
    except:
        name = "Product Error"
        price = "None"

    result = (name, price)
    return result

def getAmazonData(link):
    driver.get(link)
    time.sleep(2)

    name = driver.find_element_by_id("productTitle").text
    
    try:
        price = driver.find_element_by_id("priceblock_ourprice").text
        price = price[5:]
    except:
        price = "Possibly out of stock";

    result = (name, price)
    return result


# Costco Data
costco_records = [] 

costco_links = [] # Insert all Costco links here, each in its own string

for item in costco_links:
    costco_records.append(getCostcoData(item))

# Amazon Data
amazon_records = []

amazon_links = [] # Insert all Amazon links here, each in its own string

for item in amazon_links:
    amazon_records.append(getAmazonData(item))

driver.quit()

# Create csv file
for item in costco_records:
    print(f"Name: {item[0]} || Price: {item[1]}")

time = datetime.datetime.now()
with open("PriceData.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Date:", time])
    writer.writerow("\n")

    writer.writerow(["Costco"])
    writer.writerow(['Name', 'Price'])
    writer.writerows(costco_records)

    writer.writerow("\n")

    writer.writerow(["Amazon"])
    writer.writerow(['Name', 'Price'])
    writer.writerows(amazon_records)


# OPTIONAL: Automatically send email (if using Gmail)

FROM_EMAIL = "" # Modify variables to set the 
SUBJECT = ""
TO_EMAIL = ""
BODY = ""

msg = EmailMessage()
msg["From"] = FROM_EMAIL
msg["Subject"] = SUBJECT
msg["To"] = TO_EMAIL
msg.set_content(BODY)
msg.add_attachment(open("PriceData.csv", "r").read(), filename="PriceData.csv")

EMAIL_PASSWORD = ""

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(FROM_EMAIL, EMAIL_PASS)

server.send_message(msg)