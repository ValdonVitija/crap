from typing import List
from crap.subprocesses import get_package_counter_dict


class PackageUsageCounter:
    def __init__(self):
        self.pack_counter = get_package_counter_dict()

    def increment_package_count(self, package):
        if package in self.pack_counter:
            self.pack_counter[package] += 1

    def get_unused_packages(self, important_packages) -> List[str]:
        """
        Returns a list of unused packages.

        A package is considered unused if its count is 0 and it is not in the list of important packages.
        
        Args:
            important_packages (List[str]): A list of important packages.

        Returns:
            List[str]: A list of unused packages.
        """
        return [pkg for pkg, count in self.pack_counter.items() if count == 0 and pkg not in important_packages]
