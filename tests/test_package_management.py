import unittest
from crap.package_management import PackageManagement

class TestPackageManagement(unittest.TestCase):
    def setUp(self):
        self.package_management = PackageManagement()

    def test_add_important_package(self):
        package = 'test-package'
        self.package_management.add_important_package(package)
        with open(self.package_management.filepath, 'r') as file:
            self.assertIn(package, file.read())

    def test_factory_reset_important_packages(self):
        package = 'test-package'
        self.package_management.add_important_package(package)
        self.package_management.factory_reset_important_packages()

        with open(self.package_management.filepath, 'r') as file:
            self.assertNotIn(package, file.read())

if __name__ == "__main__":
    unittest.main()