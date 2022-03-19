from builtins import print
from selenium import webdriver

"""
The source for the very first version of the web scrapper.
No classes or functions. Just codes.
Part 2: This part gathers the information from the links gathered in part 1.
"""

# The file which previous parts results were saved in is read here and named "file".
with open("links_2.txt") as file:
    # The file is read line by line and placed in a list called "content".
    content = file.readlines()
# The new line marker is removed from the end of each item from the list created above.
# "file" is closed now.
content = [line.strip() for line in content]

# The web driver which we want to use is determined here.
driver = webdriver.PhantomJS()
# The file in which the extracted information are to be saved is created here and named "file".
with open('results.csv', 'w') as file:
    # Since the "file" is a csv file, the first row is the name of the columns. Therefore,
    # the first row is created here.
    file.write("Name" + "," + "Phone Number" + "," + "Address" + "," + "Contact Person" + "," + "Working Hours" + "," +
               "Email" + "," + "Website" + "," + "Corresponding Page" + "," + "\n")
    file.flush()
    # For each link in the list created above a task is performed. In each iteration, the link is
    # saved in the variable "page".
    for page in content:
        # The web driver loads the "page".
        driver.get(page)
        # The sections which may raise an error are placed in the "try" sections and their
        # possible error is handled in each following "except".
        try:
            # The name of the company is extracted here. In order to avoid a mix up, the commas in
            # the name are replaced by pipe "|". If the name is missing from the page an error is
            # raised which is handled in the upcoming "except" section.
            Name = driver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div/div/h1").text
            Name = Name.replace(",", "|")
            print("1 passed. Name extracted.")
        except:
            Name = "Missing"
            print("1 failed. Name missing.")
        try:
            # The information this app is trying to extract is located in a list in the webpage.
            # Therefore, the lines below tend to find this list and read its contents and create a
            # list variable from them. This list variable is named "List_Items" and the source
            # list is called "Data_List".
            Data_List = driver.find_element_by_xpath("/html/body/div[1]/section/div[2]/div/div[1]/div[2]/ul")
            List_Items = Data_List.find_elements_by_tag_name("li")
            # A new list variable is created to hold each piece of information the app extracts
            # prior to writing it to "file". This list varialbe is called "Info_List". Obviously,
            # the first item of this list is name which was extracted earlier.
            Info_List = [Name]
            # For each item read from the source list an operation is performed.
            for item in List_Items:
                # This is the data cleaning section. In order to avoid a mix up, the commas are replaced
                # by pipe "|". Furthermore, any unwanted part of the scrapped data is ommited by replacing
                # it with nothing. Additionally, the new line marker is removed from the end of each item.
                Info_Raw = item.text.replace(",", "|").replace("ADDRESS", "").replace("CONTACT PERSON", "")\
                    .replace("WORKING HOURS", "").replace("EMAIL", "").replace("WEBSITE", "")\
                    .replace("SOCIAL LINKS", "").replace("\n", " ")
                # After the data cleaning is finished, the data is added to the list variable "Info_List".
                Info_List.append(Info_Raw)
            # The content of the list variable Info_List are joined to gethre by a comma and writen to "file".
            # This recreates the structure of the csv file.
            file.write(",".join(Info_List).replace(", ", ",") + "," + page + "," + "\n")
            file.flush()
            print("2 passed. Information extracted.")
        except:
            print("2 failed. Information missing or incomplete.")
