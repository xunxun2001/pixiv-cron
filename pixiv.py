import json

from file_utils import FileUtils
from http_utils import HttpUtils
from image import Image

class Pixiv:
    PIXIV_API = "https://www.pixiv.net/ranking.php?format=json&mode=daily&p=1"

    @staticmethod
    def main():
        http_content = HttpUtils.get_http_content(Pixiv.PIXIV_API)
        json_data = json.loads(http_content)
        images_data = json_data['contents']
        print(f'images_data:{len(images_data)}')

        images_list = []

        for i in range(50):
            image_data = images_data[i]
            print(image_data)

            # Image URLs
            origin_url = image_data['url']
            small_url = origin_url.replace("i.pximg.net", "i.pixiv.re")
            big_url = small_url.replace("/c/240x480/img-master/", "/img-original/").replace("_master1200", "")
            print(big_url)

            # Image details
            date = image_data['date']
            title = image_data['title']
            page_url = f"https://www.pixiv.net/artworks/{image_data['illust_id']}"
            user_name = image_data['user_name']

            images_list.append(Image(title, user_name, date, page_url, small_url, big_url, i + 1))


        FileUtils.write_readme(images_list)

if __name__ == "__main__":
    Pixiv.main()
