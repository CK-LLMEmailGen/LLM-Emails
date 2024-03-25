import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TargetPerson():

    element_type_dict = {
        0 : "CSS_SELECTOR",
        1 : "CLASS_NAME",
        2 : "ID",
        3 : "TAG_NAME",
        4 : "XPATH"
    }

    def __init__(self, target_person_name = None, target_person_url = None):
        self.target_person_name = target_person_name
        self.target_person_url = target_person_url



    # Getting child element from the parent element
    def get_element(self, parent_element = None, child_element_name = "", element_type = 1, wait_time = 8) -> None:
        try:
            by_attr = getattr(By, self.element_type_dict[element_type])
            child_element = WebDriverWait(parent_element, wait_time).until(EC.presence_of_element_located((by_attr, child_element_name)))
            return child_element
        except Exception as e:
            print(f"{type(e).__name__} occurred for the child element name {child_element_name}.")
            pass



    # Getting all the child elements for a parent element
    def get_elements(self, parent_element = None, child_elements_name = "", element_type = 1, wait_time = 8) -> None:
        try:
            by_attr = getattr(By, self.element_type_dict[element_type])
            child_elements = WebDriverWait(parent_element, wait_time).until(EC.presence_of_all_elements_located((by_attr, child_elements_name)))
            return child_elements
        except Exception as e:
            print(f"{type(e).__name__} occurred for the child element name {child_elements_name}.")
            pass



    # Getting elements from a list of parent elements:
    def get_elements_from_list(self, parent_list = [], child_element = "", element_type = 1, wait_time = 3):
        element_list = []
        for element in parent_list:
            element_list_temp = self.get_elements(element, child_element, element_type)
            content = ""
            for temp_element in element_list_temp:
                content += temp_element.text + "\n"
            element_list.append(content)
        return element_list



    # Getting name
    def get_name(self, parent_element = None) -> str:
        name = None
        if parent_element:
            name_elem = self.get_element(parent_element, "h1", 3)
            name = name_elem.text if name_elem else None
        return name



    # Location
    def get_location(self, parent_element = None) -> str:
        location = None
        if parent_element:
            location_elem = self.get_element(parent_element, ".text-body-small.inline.t-black--light.break-words", 0)
            location = location_elem.text if location_elem else None
        return location



    # Intro
    def get_intro(self, parent_element = None) -> str:
        intro = None
        if parent_element:
            intro_elem = self.get_element(parent_element, ".text-body-medium.break-words", 0)
            intro = intro_elem.text if intro_elem else None
        return intro



    # Work Preference
    def get_work_preference(self, parent_element = None) -> str:
        photo_element = self.get_element(parent_element, "pv-top-card--photo", 1)
        img_element = self.get_element(photo_element, "img", 3)
        work_preference = img_element.get_attribute("alt") if img_element else ""
        work_preference_text = None
        if("#OPEN_TO_WORK" in work_preference):
            work_preference_text = "Open to work"
        elif("#HIRING" in work_preference):
            work_preference_text = "Hiring"
        return work_preference_text



    # Contact details
    def get_contact_details(self, driver = None, person_url = None):
        if person_url == None:
            return None
        profile_contact_url = person_url + "/overlay/contact-info/"
        driver.get(profile_contact_url)
        contact_details = None
        contact_card = self.get_element(driver, ".pv-profile-section__section-info.section-info",0)
        urls_text_list = self.get_elements(contact_card,"h3",0)
        urls_text = []
        for text in urls_text_list:
            urls_text.append(text.text)
        urls_list = self.get_elements(contact_card,"a",0)
        urls = []
        for url in urls_list:
            urls.append(url.get_attribute("href"))
        contact_details = dict(zip(urls_text,urls))
        return contact_details



    # About section
    def get_about(self, parent_element = None) -> str:
        about = None
        if parent_element:
            about_element = self.get_element(parent_element, ".display-flex.ph5.pv3", 0)
            about_element_span = self.get_element(about_element, "span", 3)
            about = about_element_span.text if about_element_span else ""
        return about



    # Experiences
    def get_experiences(self, driver = None, person_url = None) -> str:
        if person_url == None:
            return None
        experiences_url = person_url + "details/experience/"
        driver.get(experiences_url)
        experiences_top_card = self.get_element(driver, "scaffold-layout__main",1)
        experiences_list_card = self.get_elements(experiences_top_card, ".pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column", 0)
        experiences = self.get_elements_from_list(experiences_list_card,"visually-hidden")
        return experiences if experiences else None



    # Education
    def get_educations(self, driver = None, person_url = None) -> str:
        if person_url == None:
            return None
        education_url = person_url + "details/education/"
        driver.get(education_url)
        education_top_card = self.get_element(driver, "scaffold-layout__main")
        education_list_card = self.get_elements(education_top_card,".pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column",0)
        education = self.get_elements_from_list(education_list_card,"visually-hidden",1)
        return education if education else None


    def get_person_details(self) -> str:
        # Setting the path of the webdriver
        path = "/lib/chromium-browser/chromedriver"
        sys.path.insert(0,path)
        os.environ["PATH"] += os.pathsep + path

        # Setting the options for the driver
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.binary_location = path
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # starting the webdriver, and getting the cookies
        driver = webdriver.Chrome(options = chrome_options)
        # cookie_val = getpass.getpass("Enter cookie value for the LinkedIn session: ")  # Present in Applications->Storage->Storage->li_at for linkedin
        cookie_val = os.getenv("LINKEDIN_COOKIE")

        # Starting the driver
        driver.get("https://in.linkedin.com/?src=go-pa&trk=sem-ga_campid.14650114788_asid.151761418307_crid.657403558721_kw.linkedin%20login_d.c_tid.kwd-12704335873_n.g_mt.e_geo.9182462&mcid=6844056167778418689&cid=&gad_source=1&gclid=EAIaIQobChMI6I7N8uPLhAMVh6lmAh34lw7MEAAYASAAEgL2NvD_BwE&gclsrc=aw.ds")
        new_cookie = {
            "name" : "li_at",
            "value" : cookie_val,
            "domain" : ".linkedin.com",
            "path" : "/",
            "secure" : True
        }
        driver.add_cookie(new_cookie)
        driver.refresh()

        # Returning the result as a dictionary
        personal_details = dict()

        driver.get(self.target_person_url)

        # Top-Level cards in the site
        top_card = self.get_element(driver, "scaffold-layout__main")
        top_panel = self.get_element(top_card, ".mt2.relative", 0)

        personal_details["Name"] = self.get_name(top_panel)
        personal_details["Location"] = self.get_location(top_panel)
        personal_details["Headline"] = self.get_intro(top_panel)
        personal_details["Work_Preference"] = self.get_work_preference(top_card)
        personal_details["Contact_Details"] = self.get_contact_details(driver, self.target_person_url)
        driver.get(self.target_person_url)
        top_card = self.get_element(driver, "scaffold-layout__main")
        personal_details["About"] = self.get_about(top_card)
        personal_details["Experiences"] = self.get_experiences(driver, self.target_person_url)
        personal_details["Education"] = self.get_educations(driver, self.target_person_url)

        driver.close()

        details = ""
        for key in personal_details.keys():
            details += f"{key}:\n\n{personal_details[key]}\n\n\n"

        return details