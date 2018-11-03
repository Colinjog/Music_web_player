from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re

class Crawler:
    def __init__(self):
        self.spider_name = "wangyiyun"
        self.domain = "music.163.com"
        self.outer_base_url = "http://music.163.com/song/media/outer/url?id={}"
        self.__music_url = "https://music.163.com/#/search/m/?s={}&type=1"
        self.option = webdriver.ChromeOptions()
        self.__music_exist = True
        # self.option.add_argument('--headless')
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2
            }
        }
        self.option.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=self.option)
        self.__music_id = ""

    def getmusic(self, music_name):
        self.__music_url = "https://music.163.com/#/search/m/?s={}&type=1"
        self.__music_url = self.__music_url.format(music_name)

    def getouterurl(self):
        self.driver.get(self.__music_url)
        self.driver.switch_to.frame('contentFrame')
        # print(self.driver.page_source)
        item_list = self.driver.find_elements_by_xpath('.//div[@class="srchsongst"]/div')
        if item_list:
            href = item_list[0].find_element_by_xpath(".//div[@class='td w0']//div[@class='text']/a[1]").get_attribute('href')
            match = re.search(r'\d+$', href)
            self.__music_id = match.group(0)
            print(self.__music_id)
            return self.outer_base_url.format(self.__music_id)
        else:
            print("无搜索结果!")
            self.__music_id = ""
            self.__music_exist = False
    def getlyrics(self):
        if self.driver and self.__music_exist:
            self.driver.get("https://music.163.com/#/song?id=".format(self.__music_id))
            self.driver.switch_to.frame('contentFrame')
            print("https://music.163.com/#/song?id=".format(self.__music_id))

            wait = WebDriverWait(self.driver,5)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flag_ctrl"]'))).click()
            text1 = self.driver.find_element_by_xpath('//*[@id="lyric-content"]').text
            text1 = text1[:-2]
            text1 = text1.rstrip()
            lyrics_list = text1.split('\n')
            return lyrics_list
        else:
            return []
    def close(self):
        self.driver.close()


if __name__=="__main__":
    spider = Crawler()

    spider.getmusic("shake it off")
    print(spider.getouterurl())
    print(spider.getlyrics())
    spider.getmusic('成都')
    print(spider.getouterurl())
    print(spider.getlyrics())
    spider.close()

