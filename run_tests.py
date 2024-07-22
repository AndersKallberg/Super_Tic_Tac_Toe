import unittest
import sys
import os
import warnings
import contextlib

# Add the base directory to sys.path if it's not already there
base_dir = os.path.abspath(os.path.dirname(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

def run_all_tests():
    # Suppress Pygame warnings and messages
    with open(os.devnull, 'w') as fnull:
        with contextlib.redirect_stderr(fnull), contextlib.redirect_stdout(fnull):
            import pygame
            pygame.init()

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests')

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    print("\nTest Summary:")
    print("=============")
    print(f"Total tests run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")

    if result.wasSuccessful():
        print("\nAll tests passed!")
    else:
        if result.errors:
            print("\nSome tests encountered errors:")
            for test, reason in result.errors:
                print(f"ERROR: {test} - {reason}")
        if result.failures:
            print("\nSome tests failed:")
            for test, reason in result.failures:
                print(f"FAIL: {test} - {reason}")

if __name__ == '__main__':
    run_all_tests()
