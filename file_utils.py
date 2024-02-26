from pathlib import Path
from datetime import datetime

class FileUtils:

    @staticmethod
    def write_readme(img_list):
        readme_path = Path("README.md")
        readme_path.touch(exist_ok=True)  # Create the file if it does not exist

        with readme_path.open("w", encoding="utf-8") as file:
            file.write("## Pixiv Daily\n")
            file.write(f"Update: {datetime.now().strftime('%Y-%m-%d')}\n")
            file.write("|      |      |      |\n")
            file.write("| :----: | :----: | :----: |\n")

            for i, image in enumerate(img_list, start=1):
                file.write(f"|{image}")
                if i % 3 == 0:
                    file.write("|\n")

            if len(img_list) % 3 != 0:
                file.write("|\n")

# Example usage, assuming img_list is a list of Image objects
# FileUtils.write_readme(img_list)
