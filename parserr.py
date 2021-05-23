from config import DRIVER_PATH, URL
from selenium import webdriver
from db import find_all_search, process_rooms_card


class ParseRooms:
    def __init__(self, url, bot=None):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot

    def __del__(self):
        self.driver.close()

    async def parse(self):
        search_models = find_all_search()

        for page in range(1, 5):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))
            items = len(self.driver.find_elements_by_class_name("_93444fe79c--serp--2JEwc _93444fe79c--serp--light--3joGI"))
            for item in range(items):
                cards = self.driver.find_elements_by_class_name("_93444fe79c--container--2Kouc _93444fe79c--link--2-ANY")
                for card in cards:
                    product_item = card.find_element_by_class_name("_93444fe79c--container--JdWD4")
                    card_title = product_item.text
                    card_href = product_item.get_attribute('href')
                    for search_model in search_models:
                        if card_title.find(search_model.title) >= 0:
                            await process_rooms_card(card_title, card_href, search_model.chatid, self.bot)