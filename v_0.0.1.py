from urllib import request
from bs4 import BeautifulSoup
import re
from builtins import print
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

"""
The source for the very first version of the web scrapper app.
No classes or functions. Just codes.
"""
# Open the file which contains the links of the root pages and read it line by line.
with open("links2.txt") as file:
    content = file.readlines()
content = [line.strip() for line in content]

# Build a list to store the links for the next pages scrapped from the root pages.
Links_temp = []
# This for loop gets every link, and extracts the links of the next pages based on a criteria.
for l in content:
    page = request.urlopen(l)
    soup = BeautifulSoup(page, "html.parser")
    # The findall function from the regular expressions library finds every string from the
    # pages source code which follow a specific template written in regular expressions format.
    # These two variables are to be used later on for making the template dynamic.
    # spec_var = "property"
    # regular_expression = "/" + spec_var + "/.+\\\""
    links = re.findall("/property/.+\"", str(soup))
    # This for loop checks to see if there is a repeated link. It needs to be rewritten
    # and optimized in so many ways!
    for i in links:
        if links.index(i) < len(links)-1:
            if i == links[links.index(i) + 1]:
                del links[links.index(i) + 1]
        # Rebuilds the links which are handled by a script instead of a <a> tag and stores them
        # in a list to be retrieved later.
        Links_temp.append("http://www.landsoftexas.com" + i.strip("\""))

# The with open line creates the file which is supposed to store the results of the scrapping
with open('result', 'w') as file:
    # The for loop below reads the links from the list.
    for page in Links_temp:
        # Set the web driver as Chrome. This requires the chrome drive to be in the path
        # variable. Need to find a way to automate this.
        driver = webdriver.Chrome()
        # Selenium's get module opens the browser and loads the link given to it, here 'page'.
        driver.get(page)
        # This is the location of the first element in the web page.
        XPATH_1 = '//*[@id="memberBox"]/div/div/div[2]/div[3]/button'
        # Selects the element in the given location.
        element_1 = driver.find_element_by_xpath(XPATH_1)
        # Executes the script which is supposed to show the hidden content of the web page.
        element_2 = driver.execute_script("var propid = $('.inventory-item').attr('data-propid');"
                                          " return recordPropertyPhone(461662, propid);", element_1)
        # This is an incomplete error handling. It was meant to avoid application crash
        # if element_3 could not be found.
        # element_3 = "none"
        # try:
        #     element_3 = driver.find_element_by_xpath(XPATH_2)
        #     element_3.click()
        # except:
        # XPATH_2 = 'driver.find_element_by_xpath(XPATH_1)'
        # The send keys module simulates pressing of the given keys. In this case it is
        # there to stop the page from redirecting by stopping loading. Not even sure it works!
        element_1.send_keys(Keys.CONTROL + Keys.ESCAPE)
        # A little delay in case there is latency in retrieving the hidden content from the
        # server. There was a similar delay before the sending the keys above but it cuased
        # error. It seems that the elements 1 and 2 are lost when there is a delay.
        time.sleep(1)
        # Expecting the source of the page to be updated with the new content, this line
        # reads the source html code.
        source0 = driver.page_source
        # Closes the browser window.
        driver.quit()

        # Finds the position of the given string in the pages source code. This string has
        # happened only once in the source.
        data_position = source0.find('seller-info')
        # Since I knew how much after the position above the data I wanted to scrap was
        # located, this line gives the location of the beginning of my data. Also, this
        # line trims off the code before this position.
        source = source0[data_position + 71:]
        # Same as above, this time for the ending of the data.
        data_position = source.find('agentPhone') + 24
        # Trim the data after the ending position off.
        source = source[:data_position]
        # Cleaning the data. The last three lines do the same by using regular expressions.
        # The line which replaces comma with pipe is there to avoid splitting when opening
        # the file in Excel as a csv file.
        source = source.replace("	", " ")
        source = source.replace("\n", " ")
        source = source.replace("  ", "")
        source = source.replace(" <", "<")
        source = source.replace("> ", ">")
        source = source.replace("&amp;", "&")
        source = source.replace(",", "|")
        source = source.replace("</p>", ",")
        source = re.sub("<.*?>", "", source)
        source = re.sub(".*?>", "", source)
        source = re.sub("<.*?", "", source)
        # prints the final outcome and each one's link so that I can see what the app is
        # doing.
        print(source + "," + page)
        # Writes the outcome to the file. Actially, keeps in buffer then flushes to file.
        file.write(source + "," + page + "\n")
        file.flush()
    # Closes the file but not required.
    # file.close()
