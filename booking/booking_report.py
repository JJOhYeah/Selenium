import selenium.common.exceptions as sel_exc
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    """
    A class to parse data from the deal boxes on the Booking.com website.

    Attributes:
        boxes_section_element (WebElement): the element containing the deal boxes
        deal_boxes (list of WebElement): a list of the deal box elements
    """

    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.XPATH, '//div[@data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []

        for deal_box in self.deal_boxes[:3]:
            try:
                hotel_name = deal_box.find_element(By.XPATH, './/div[@data-testid="title"]') \
                    .get_attribute('innerHTML').strip()

                hotel_price = deal_box.find_element(By.XPATH, './/span[@data-testid="price-and-discounted-price"]') \
                    .get_attribute('innerHTML').strip()

                hotel_score = deal_box.find_element(By.XPATH, './/div[@data-testid="review-score"]/div') \
                    .get_attribute('innerHTML').strip()

                collection.append(
                    [hotel_name, hotel_price, hotel_score]
                )
            except sel_exc.NoSuchElementException:
                pass

        return collection
