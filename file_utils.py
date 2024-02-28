from pathlib import Path
from datetime import datetime
import pytz
import json

class FileUtils:

    @staticmethod
    def write_archive(img_list, ranking_type):
        archive_dir = Path(f"archive/{ranking_type}")
        archive_dir.mkdir(exist_ok=True)

        tz = pytz.timezone('Asia/Shanghai')
        archive_file = archive_dir / f"{datetime.now(tz).strftime('%Y-%m-%d')}.md"
        archive_file.touch(exist_ok=True)

        with archive_file.open("w", encoding="utf-8") as file:
            FileUtils._write_content(file, img_list, ranking_type)
        FileUtils._write_json(archive_dir, img_list, ranking_type)
    @staticmethod
    def update_readme():
        readme_path = Path("README.md")
        readme_path.touch(exist_ok=True)  # Create the file if it does not exist

        # 定义子目录的处理顺序
        subdirs_priority = ['daily', 'weekly', 'monthly']

        # 获取所有archive子目录中最新的.md文件
        archive_dir = Path("archive")
        toc = "## Table of Contents\n"
        latest_content = ""

        # 按照指定的顺序处理子目录
        for subdir in subdirs_priority:
            ranking_type_dir = archive_dir / subdir
            if ranking_type_dir.is_dir():
                # 获取每个子目录中最新的.md文件
                latest_md_files = sorted(ranking_type_dir.glob('*.md'), reverse=True)
                if latest_md_files:
                    latest_md_file = latest_md_files[0]
                    with latest_md_file.open("r", encoding="utf-8") as file:
                        # 假设第一行是文件的主标题
                        first_line = file.readline().strip()
                        # 提取Markdown标题（去掉"## "）
                        title = first_line.replace('## ', '')
                        # 生成目录项和内容
                        toc += f"- [{title}](#{subdir})\n"
                        latest_content += f"{first_line}\n"
                        latest_content += f"<div id='{subdir}'></div>\n\n"
                        # 添加剩余的文件内容
                        latest_content += file.read() + "\n\n"

        # 更新README.md文件
        with readme_path.open("w", encoding="utf-8") as file:
            file.write(toc + "\n\n" + latest_content)

    @staticmethod
    def write_readme(img_list, ranking_type):
        FileUtils.write_archive(img_list, ranking_type)
        FileUtils.update_readme()

    @staticmethod
    def _write_content(file, img_list, ranking_type):
        tz = pytz.timezone('Asia/Shanghai')
        file.write(f"## {ranking_type.replace('_', ' ').capitalize()} Ranking\n")
        file.write(f"Update: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')}\n\n")
        file.write("|      |      |      |\n")
        file.write("| :----: | :----: | :----: |\n")

        # Initialize an empty string to hold the row content
        row_content = ""
        for i, image in enumerate(img_list, start=1):
            # Wrap each image and its download link in a markdown table cell
            row_content += f"| ![]({image.small_url})<br>**#{image.rank}** [{image.title}]({image.page_url})<br>[Download]({image.big_url}) "
            # Every 3 images or at the end of the list, end the table row
            if i % 3 == 0 or i == len(img_list):
                row_content += "|\n"
                file.write(row_content)
                row_content = ""  # Reset row content for the next line

        # Check if there are less than 3 images in the last row
        remainder = len(img_list) % 3
        if remainder > 0:
            # Add empty cells to complete the row
            for _ in range(3 - remainder):
                row_content += "|      "
            row_content += "|\n"
            file.write(row_content)

    @staticmethod
    def _write_json(archive_dir, img_list, ranking_type):
        tz = pytz.timezone('Asia/Shanghai')
        # 定义JSON文件的路径
        json_file_path = archive_dir / f"{datetime.now(tz).strftime('%Y-%m-%d')}.json"

        images_data = []
        for image in img_list:
            images_data.append({
                'rank': image.rank,
                'title': image.title,
                'small_url': image.small_url,
                'page_url': image.page_url,
                'big_url': image.big_url
            })

        # 将图像信息列表写入JSON文件
        with json_file_path.open('w', encoding='utf-8') as json_file:
            json.dump(images_data, json_file, ensure_ascii=False, indent=4)