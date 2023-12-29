import unittest
from crap.package_usage_counter import PackageUsageCounter

class PackageUsageCounterTests(unittest.TestCase):
    def setUp(self):
        self.package_usage_counter = PackageUsageCounter()

    def test_increment_package_count(self):
        package = 'typer'
        self.package_usage_counter.increment_package_count(package)
        self.assertEqual(self.package_usage_counter.pack_counter[package], 1)

    def test_get_unused_packages(self):
        important_packages = ['important_package']
        unused_package = 'unused_package'
        self.package_usage_counter.pack_counter[unused_package] = 0
        unused_packages = self.package_usage_counter.get_unused_packages(important_packages)
        self.assertIn(unused_package, unused_packages)

if __name__ == "__main__":
    unittest.main()