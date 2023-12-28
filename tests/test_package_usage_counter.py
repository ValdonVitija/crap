import unittest
from crap.package_usage_counter import PackageUsageCounter

class PackageUsageCounterTests(unittest.TestCase):
    def test_increment_package_count(self):
        counter = PackageUsageCounter()
        package = "numpy"

        # Increment package count
        counter.increment_package_count(package)

        # Verify count is incremented
        self.assertEqual(counter.pack_counter[package], 1)

    def test_get_unused_packages(self):
        counter = PackageUsageCounter()
        important_packages = ["numpy", "pandas"]

        # Add some packages to the counter
        counter.pack_counter["numpy"] = 0
        counter.pack_counter["pandas"] = 1
        counter.pack_counter["matplotlib"] = 0

        # Get unused packages
        unused_packages = counter.get_unused_packages(important_packages)

        # Verify unused packages
        self.assertEqual(unused_packages, ["matplotlib"])

if __name__ == "__main__":
    unittest.main()