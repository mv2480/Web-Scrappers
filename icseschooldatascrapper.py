from validateme.scrapper.web.selenium.icse_school.locators import PageLocators
from validateme.config.vmbotconfig import boot_config as config
from validateme.scrapper.base.basescrapper import BaseScrapper
from validateme.vmbots import VmBots
import validateme.scrapper.base.vmdatatypes as vmdatatypes
from validateme.scrapper.base import vmscrappedrecord as vmd
from validateme.scrapper.base import vmbotutil
from validateme.db.mongo import vmmongo
import traceback as tb
from validateme.scrapper.web.selenium.icse_school.Page import HomePage


class SchoolInfo:
    def __init__(self):
        self.code = None
        self.name = None
        self.contact_details = None
        self.state = None
        self.address = None
        self.raw_info = None


class StoreData:

    def insert_into_db(self, school_info,scrapper_report):
        rec = vmd.VmScrappedRecord()
        rec.code = school_info.code
        rec.name = school_info.name
        rec.displayName = school_info.name
        acronym = vmbotutil.acronym_or_empty_list(rec.name)
        rec.VMType = vmdatatypes.VmType.SCHOOL.value
        rec.country = 'INDIA'
        rec.source = VmBots.SCHOOL_ICSE.value

        Contacts = vmd.VmContact()
        Contacts.raw_contact = school_info.contact_details

        addr = vmd.VmAddress()
        addr.country = 'INDIA'
        addr.streetAddress = school_info.address
        addr.state = school_info.state
        rec.address = addr

        vmTags = vmd.VmSearchTags()
        vmTags.groupTags = ['SCHOOL', 'EDUCATIONAL', 'SCHOOL-ICSE', 'ICSE', school_info.state]
        vmTags.nameTags = [rec.name]
        vmTags.acronym = acronym
        rec.searchTags = vmTags

        origin = vmd.VmRecordOrigin()
        origin.generatedUniqueId = rec.code
        origin.uniqueIdAtSrc = rec.code
        origin.originSource = rec.source
        origin.rawAddress = school_info.address
        rawData = vmd.VmRecordRawData()
        rawData.rawData = school_info.__dict__
        origin.rawData.append(rawData)

        rec.origin.append(origin)
        rec.createdBy = rec.source
        rec.updatedBy = rec.source

        vmmongo.insert_scrapped_record(rec,scrapper_report)

    def extract_data(self, all_school_data,state, scrapper_report):
        for school_data in all_school_data:
            School = SchoolInfo()
            separator = ','
            general_details = school_data[0].split('\n')
            School.code = general_details[0]
            name = general_details[1]
            School.name = name.translate({ord(','): None})
            School.address = general_details[2]
            School.state = state
            contacts = school_data[1].split('\n')
            School.contact_details = separator.join(contacts)
            School.raw_info = school_data


            self.insert_into_db(School,scrapper_report)


class IcseSchoolDataScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(VmBots.SCHOOL_ICSE.value)
        self.icse_website_url = config['app']['bot']['school']['icseUrl']
        self.HomePage = HomePage(self.driver)


    def scrap(self, *args, **kwargs):
        self.logger.log_event_started('Extract all States name')
        self.driver.get(self.icse_website_url)
        self.HomePage.fill_country()
        self.states = self.HomePage.get_states()
        self.states.remove('--Select--')
        self.logger.log_event_completed('All States name Extracted')
        self.collect_data()


    def collect_data(self):
        self.logger.log_event_started('Data collection started')

        for state in self.states:
            self.driver.get(self.icse_website_url)
            self.HomePage.fill_country()
            self.HomePage.fill_state(state)
            self.HomePage.click_search_button()
            self.logger.log_event_started('processing state=' + state)
            self.HomePage.get_table()
            table_id = self.HomePage.school_data()
            cells = self.HomePage.get_cells(table_id)  # get all of the cell in the table
            all_school_data = []
            
            for i in range(5,len(cells),5):
                school_data = []
                
                for b in range(5):
                    school_data.append(cells[i+b].text)
                all_school_data.append(school_data)

            StoreData().extract_data(all_school_data,state,self.scrapper_report)
            self.logger.log_event_started('processing state=' + state)


        self.logger.log_event_completed('Data collection completed')

def main():
    IcseSchoolDataScrapper().start_scrapping()

if __name__ == '__main__':
        main()




