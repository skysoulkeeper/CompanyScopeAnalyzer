# tests/run_tests.py
import unittest


# Define a function to run tests
def run_tests():
    # Create a TestLoader instance to load test cases
    loader = unittest.TestLoader()

    # Specify the directory where tests are located
    start_dir = 'tests'

    # Discover and collect all test cases from the 'tests' directory
    suite = loader.discover(start_dir)

    # Create a TextTestRunner instance to run the tests and display results
    runner = unittest.TextTestRunner()

    # Run the test suite using the TextTestRunner
    runner.run(suite)


# This script allows running unit tests when executed directly
if __name__ == "__main__":
    # Call the run_tests() function to execute tests and display results
    run_tests()
