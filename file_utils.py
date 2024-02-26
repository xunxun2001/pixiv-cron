from pathlib import Path
from datetime import datetime
import pytz

class FileUtils:

    @staticmethod
    def write_archive(img_list):
        archive_dir = Path("archive/daily")
        archive_dir.mkdir(exist_ok=True)

        tz = pytz.timezone('Asia/Shanghai')
        archive_file = archive_dir / f"{datetime.now(tz).strftime('%Y-%m-%d')}.md"
        archive_file.touch(exist_ok=True)

        with archive_file.open("w", encoding="utf-8") as file:
            FileUtils._write_content(file, img_list)

    @staticmethod
    def write_readme(img_list):
        readme_path = Path("README.md")
        readme_path.touch(exist_ok=True)  # Create the file if it does not exist

        with readme_path.open("w", encoding="utf-8") as file:
            FileUtils._write_content(file, img_list)

        FileUtils.write_archive(img_list)

    @staticmethod
    def _write_content(file, img_list):
        tz = pytz.timezone('Asia/Shanghai')
        file.write("## Pixiv Daily\n")
        file.write(f"Update: {datetime.now(tz).strftime('%Y-%m-%d %Z')}\n\n")
        file.write("|      |      |      |\n")
        file.write("| :----: | :----: | :----: |\n")

        # Initialize an empty string to hold the row content
        row_content = ""
        for i, image in enumerate(img_list, start=1):
            # Wrap each image and its download link in a markdown table cell
            row_content += f"| ![]({image.small_url})<br>**#{image.rank}** [{image.title}]({image.page_url})<br>[Download]({image.big_url_jpg}) "
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