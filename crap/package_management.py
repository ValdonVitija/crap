import pathlib
import shutil
from typing import List


class PackageManagement:
    def __init__(self, filename="important_packages.txt"):
        self.filename = filename
        self.filepath = pathlib.Path(__file__).parent / "data" / self.filename

    def add_important_package(self, package: str):
        """
        Add a package to the list of important packages.

        Args:
            package (str): The name of the package to add.
            filename (str, optional): The name of the file to store the list of important packages.
                Defaults to "important_packages.txt".
        """
        with open(self.filepath, "r+", encoding="utf-8") as file:
            existing_packages = {line.strip() for line in file}
            if package not in existing_packages:
                file.write(package + "\n")
                print(f"✅ Added '{package}' to important packages")
            else:
                print(f"'{package}' is already listed as an important package")

    def show_important_packages(self) -> List[str]:
        """
        Display the list of important packages.

        Args:
            filename (str): The name of the file containing the list of important packages.
                Default is "important_packages.txt".

        Returns:
            List[str]: The list of important packages.

        """
        with open(self.filepath, "r", encoding="utf-8") as file:
            important_packages = [line.strip() for line in file]
            print("📦 Important packages:")
            for package in important_packages:
                print(f" - {package}")

    def remove_important_package(self, package: str):
        """
        Removes a package from the list of important packages.

        Args:
            package (str): The name of the package to be removed.
            filename (str, optional): The name of the file containing the list of important packages.
                Defaults to "important_packages.txt".
        """
        with open(self.filepath, "r+", encoding="utf-8") as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate(0)
            for line in lines:
                if line.strip() != package:
                    file.write(line)

            if package in (line.strip() for line in lines):
                print(f"❌ Removed '{package}' from important packages")
            else:
                print(f"'{package}' was not found in important packages")

    def flush_important_packages(self):
        """
        Flushes the important packages by removing the contents of the specified file.

        Args:
            filename (str, optional): The name of the file to flush. Defaults to "important_packages.txt".
        """
        with open(self.filepath, "w", encoding="utf-8"):
            pass
        print("All important packages have been removed.")

    def factory_reset_important_packages(self):
        """
        Reset the list of important packages to the default packages
        """
        DEFAULT_PACKAGES_FILE = "default_important_packages.txt"
        default_packages_path = (
            pathlib.Path(__file__).parent / "data" / DEFAULT_PACKAGES_FILE
        )

        try:
            shutil.copyfile(default_packages_path, self.filepath)
            print("🔄 Reset important packages to default")
        except FileNotFoundError:
            print(f"Default packages file '{DEFAULT_PACKAGES_FILE}' not found")
