from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BookingFiltration:
    """
    A class to interact with the Booking.com website to apply filters.

    Attributes:
        driver (WebDriver): the webdriver instance to use for interaction
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values: int):
        star_filtration_box = self.driver.find_element(By.XPATH, '//div[@data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    star_element.click()
