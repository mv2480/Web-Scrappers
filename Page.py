from .locators import PageLocators
from validateme.scrapper.web.selenium.base.basepage import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):

    def fill_country(self):
        select = Select(self.driver.find_element_by_name(PageLocators.CountryNameTag))
        select.select_by_visible_text('India')

    def school_data(self):
        return self.driver.find_element(*PageLocators.School)

    def get_table(self):
        return WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(PageLocators.TableLocator))

    def get_cells(self, table_id):
        return table_id.find_elements(*PageLocators.CellLocator)

    def get_state_select_elem(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(PageLocators.StateLocator))    

    def get_states(self):
        element = self.get_state_select_elem()
        element.click()
        stateSelectElem = Select(self.driver.find_element(*PageLocators.StateLocator))
        return [s.text for s in stateSelectElem.options]
       

    def fill_state(self, state):
        state_option = WebDriverWait(self.driver, 5).until(
            lambda x: x.find_element_by_xpath(f"//select[@id='{PageLocators.state_select_id}']/option[text()='{state}']"))
        state_option.click()

    def click_search_button(self):
        Button_Name = PageLocators.SearchButtonNameTag
        self.driver.find_element_by_name(Button_Name).click()
