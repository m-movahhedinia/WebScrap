from builtins import print
from selenium import webdriver
import time

"""
The source for the very first version of the web scrapper for Mr. Nanda Kumar's project.
No classes or functions. Just codes.
Part 1: This part gathers the links to all the pages of the companies. These pages are the ones
        containing the address, email, and other info.
"""
# This line reads the file containing all the links from the excel file and names it "file".
with open("Links_1.txt") as file:
    # The file is read line by line and produces a list out of them.
    content = file.readlines()
# The new line marker is removed from the end of each item from the list created above.
# "file" is closed now.
content = [line.strip() for line in content]

# The web driver which we want to use is determined here.
driver = webdriver.PhantomJS()
# The file which we are going to save our results in is created here and named "file".
with open('links_2.txt', 'w') as file:
    # For each link in the list created above a task is performed. In each iteration, the link is
    # saved in the variable "page".
    for page in content:
        # The variable "Flag" is used later on to mark the end of the while loop.
        Flag = 1
        # The web driver loads the "page".
        driver.get(page)
        # This while loop keeps running as long as nothing out of the ordinary happens. If anything
        # unexpected occurs the variable "Flag" is changed to 0 which signals the end of the while
        # loop.
        while Flag == 1:
            # In order to ovoid errors causing a crash in the app, the possible erroneous sections
            # are placed in a "try" and their exceptions in an "except".
            try:
                # In case and advertisement appears in the page, this section will find the close
                # button and click it. If there are no ads, it will raise an error which is
                # handled in the corresponding "except" section.
                driver.find_element_by_class_name("lcf-close").click()
                print("1 passed. Ad closed.")
            except:
                print("1 failed. No ads.")
            try:
                # The elements with class name "GAQ_C_BUSL" hold the links we require. This section
                # searches the page for these elements and saves them in a list called "element_1"
                element_1 = driver.find_elements_by_class_name("GAQ_C_BUSL")
                # For each element found, its "href" attribute is written to "file"
                for element in element_1:
                    file.write(element.get_attribute('href') + "\n")
                    file.flush()
                print("2 passed. Links extracted.")
            # If the page doesn't contain any links, an error is raised which is handled below.
            except:
                print("2 failed. No links to scrap.")
            try:
                # In case the links continue to another page, the line below finds the button
                # with the ID "nextPage" and clicks it. If there is no such button in the page,
                # an error is raised which is handled in the next "except" section.
                driver.find_element_by_id("nextPage").click()
                print("3 passed. Next page requested")
                # The apps runtime is delayed for five seconds so that the page has time to load
                # the new content.
                time.sleep(5)
            except:
                # Since there is no more information to scrap the end of the while loop is signaled
                # by changing the value of "Flag" to 0.
                Flag = 0
                print("3 failed. Process finished")
