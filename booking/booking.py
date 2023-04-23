import os

from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By

import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport


class Booking(webdriver.Chrome):
    """
    A class to represent a booking.com web driver.

    Methods:
        __init__(driver_path=r"/Users/jayjohnson/Documents/chromedriver_mac64", teardown=False)
            Initializes the Chrome web driver.
        __exit__(exc_type, exc_val, exc_tb)
            Closes the Chrome web driver.
        land_first_page()
            Navigates to the booking.com home page.
        remove_popup()
            Removes the popup on the booking.com home page.
        select_place_to_go(place_to_go)
            Enters the user's desired location on the booking.com home page.
        select_dates(check_in_date, check_out_date)
            Selects the user's desired check-in and check-out dates on the booking.com home page.
        select_adults(count=1)
            Selects the number of adults on the booking.com home page.
        click_search()
            Clicks the search button on the booking.com home page.
        apply_filters()
            Applies filters to the search results on the booking.com home page.
        report_results()
            Reports the search results in a table.

    Attributes:
        driver_path (str): path to the chromedriver executable
        teardown (bool): whether to close the webdriver on exit
    """

    def __init__(self, driver_path=r"/Users/jayjohnson/Documents/chromedriver_mac64", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)

        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def remove_popup(self):
        popup = self.find_element(By.XPATH, "//button[@aria-label='Dismiss sign-in info.']")
        popup.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.NAME, 'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element(By.XPATH, "//ul[@data-testid='autocomplete-results']/li")
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(By.XPATH, "//button[@data-testid='occupancy-config']")
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(By.XPATH, "//input[@type='range' and @id='group_adults']/"
                                                                  "following-sibling::div/button[1]")
            decrease_adults_element.click()

            # If the value of adults reaches 1, then we should get out of the while loop.
            adults_value_element = self.find_element(By.ID, 'group_adults')
            adults_value = adults_value_element.get_attribute(
                'value'
            )

            if int(adults_value) == 1:
                break

        increase_button_element = self.find_element(By.XPATH, "//input[@type='range' and @id='group_adults']/"
                                                              "following-sibling::div/button[2]")

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_filters(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)

    def report_results(self):
        hotel_boxes = self.find_element(By.ID, 'search_results_table')

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.align["Hotel Name"] = "l"
        table.add_rows(report.pull_deal_box_attributes())

        print(table)
