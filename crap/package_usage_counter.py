from typing import List
from crap.subprocesses import get_package_counter_dict


class PackageUsageCounter:
    def __init__(self):
        self.pack_counter = get_package_counter_dict()

    def increment_package_count(self, package):
        if package in self.pack_counter:
            self.pack_counter[package] += 1

    def get_unused_packages(self, important_packages) -> List[str]:
        return [pkg for pkg, count in self.pack_counter.items() if count == 0 and pkg not in important_packages]
