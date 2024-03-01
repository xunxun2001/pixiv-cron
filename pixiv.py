import json
import requests
from datetime import datetime, timedelta
from file_utils import FileUtils
from http_utils import HttpUtils
from image import Image
import logging
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Pixiv:
    PIXIV_API_DAILY = "https://www.pixiv.net/ranking.php?format=json&mode=daily&p=1"
    PIXIV_API_WEEKLY = "https://www.pixiv.net/ranking.php?format=json&mode=weekly&p=1"
    PIXIV_API_MONTHLY = "https://www.pixiv.net/ranking.php?format=json&mode=monthly&p=1"
    # TODO: PIXIV_API_DAILY_R18 = "https://www.pixiv.net/ranking.php?format=json&mode=daily_r18&p=1"
    # TODO: PIXIV_API_WEEKLY_R18 = "https://www.pixiv.net/ranking.php?format=json&mode=weekly_r18&p=1"

    def fetch_big_url(self, url, index, ugoira):
        response = requests.head(url)
        if response.status_code == 404:
            # 如果返回 404，替换 jpg 为 png 并再次尝试
            new_url = url.replace('.jpg', '.png')
            response = requests.head(new_url)
            if response.status_code == 200:
                logger.info(f"Image #{index}: .jpg not found, .png found.")
                return new_url
            else:
                logger.info(f"Image #{index}: Neither .jpg nor .png found.")
                return ugoira
            #Todo: https://github.com/xuejianxianzun/PixivBatchDownloader/blob/824e542880987eb761c15bd9124cd5eaf171ce91/notes/%E9%A2%84%E8%A7%88%E5%8A%A8%E5%9B%BE.md?plain=1#L10
            #https://bgm.tv/group/topic/349618
            #Todo: https://plasmacookie.github.io/2021/12/21/pixiv%E7%88%AC%E8%99%AB/
        else:
            logger.info(f"Image #{index}: .jpg found.")

        return url

    def fetch_ranking_data(self, api_url):
        http_content = HttpUtils.get_http_content(api_url)
        json_data = json.loads(http_content)
        return json_data['contents']

    def process_images(self, images_data):
        images_list = []

        for i, image_data in enumerate(images_data[:50]):  # 假设我们只处理前50个图片
            image_data = images_data[i]

            # Image URLs
            origin_url = image_data['url']
            small_url = origin_url.replace("i.pximg.net", "i.pixiv.re")
            big_url = small_url.replace("/c/240x480/img-master/", "/img-original/").replace("_master1200", "")
            # print(big_url)

            # Image details
            date = image_data['date']
            title = image_data['title']
            page_url = f"https://www.pixiv.net/artworks/{image_data['illust_id']}"
            user_name = image_data['user_name']
            tags, rating_count, view_count = image_data['tags'], image_data['rating_count'], image_data['view_count']

            big_url = self.fetch_big_url(big_url, i + 1, page_url)
            images_list.append(Image(title, user_name, date, page_url, small_url, big_url, i + 1, tags, rating_count, view_count))

        return images_list
    @staticmethod
    def main():
        pixiv = Pixiv()

        tz = pytz.timezone('Asia/Shanghai')
        today = datetime.now()
        today_weekday = datetime.now(tz).weekday()
        tomorrow = today + timedelta(days=1)

        api_urls_and_types = {
            Pixiv.PIXIV_API_DAILY: "daily",
            Pixiv.PIXIV_API_WEEKLY: "weekly",
            Pixiv.PIXIV_API_MONTHLY: "monthly",
        }


        for api_url, ranking_type in api_urls_and_types.items():
            images_data = pixiv.fetch_ranking_data(api_url)
            images_list = pixiv.process_images(images_data)
            FileUtils.write_readme(images_list, ranking_type)

if __name__ == "__main__":
    Pixiv.main()
