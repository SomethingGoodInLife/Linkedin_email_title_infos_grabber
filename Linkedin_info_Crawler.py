from selenium import webdriver
import csv
import time

browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe")  # load chromedriver

browser.get("https://www.linkedin.com/uas/login")  # jump to the login page
file = open("C:\password\config.txt")  # linkedin username and password in local path
lines = file.readlines()
username = lines[0]
password = lines[1]

elementID = browser.find_element_by_id("username")
elementID.send_keys(username)

elementID = browser.find_element_by_id("password")
elementID.send_keys(password)
elementID.submit()
time.sleep(1)
file.close()

base_link = "https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A0%22%5D&facetIndustry=%5B%2257" \
            "%22%5D&origin=FACETED_SEARCH&page="  # put the pre-search link in here


# jump to the linkedin search "people " page, with default filter "Oil & energy" "United States"


def get_info_all():
    global browser
    file_info = open('client_info.csv', 'w')  # creat a csv file_info
    info_writer = csv.writer(file_info)
    info_writer.writerow(["Name", "Title and Company", "E-mail", "Linkedin url"])  # write the rows

    for i in range(1, 11):
        browser.get(base_link + f'{i}')  # iterate the page from 1 to 10
        browser.implicitly_wait(10)
        for name in browser.find_elements_by_xpath("//span[@class = 'name actor-name']"):  # find the name
            client_name = name.text
            name.click()
            browser.implicitly_wait(10)
            get_title_company_name = browser.find_element_by_xpath(
                ".//p[@class = 'subline-level-1 t-14 t-black t-normal search-result__truncate']").text  # get the title and company name
            browser.find_element_by_link_text("Contact info").click()  # click the "Contact Info" to get a submenu
            browser.implicitly_wait(10)

            try:  # if there is a email address, get it
                get_linked_url = browser.find_element_by_class_name(
                    "pv-contact-info__contact-type ci-vanity-url").find_element_by_tag_name('a').text  #get the linkedin url
                print("find the url")
                get_email = browser.find_element_by_class_name(
                    "pv-contact-info__contact-type ci-email").find_element_by_tag_name('a').text # get the email address
            except Exception:
                get_email = "n/a"
                get_linked_url = "n/a"
            browser.implicitly_wait(10)
            info_writer.writerow([client_name, get_title_company_name, get_email,
                                  get_linked_url])  # write the info to csv file_info

            browser.get(base_link + f'{i}')   # back to the previous page to continue the iteration
            tbrowser.implicitly_wait(10)
    file_info.close()


get_info_all()  # call the function

