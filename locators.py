from selenium.webdriver.common.by import By

class PageLocators(object):
    state_select_id = 'ctl00_ctl00_Cphcontent_Cphleftcontent_ddlstate'
    states_xpath = '//*[@id="' + state_select_id + '"]'
    CountryNameTag = "ctl00$ctl00$Cphcontent$Cphleftcontent$ddlcountry"
    SearchButtonNameTag = 'ctl00$ctl00$Cphcontent$Cphleftcontent$btnsearch'
    SchoolDataTagID = 'ctl00_ctl00_Cphcontent_Cphleftcontent_result'
    School = (By.ID, SchoolDataTagID)
    TableLocator = (By.ID, SchoolDataTagID)
    StateLocator = (By.XPATH, f"{states_xpath}")
    CellLocator = (By.TAG_NAME, "td")
    #OptionLocator = f"//select[@name='{StateTag}']/option[text()='{state}']"
