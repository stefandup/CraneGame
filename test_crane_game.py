import unittest
import pandas as pd
import glob
import os
# from view_csv import <functions_to_test>


class TestCraneGame(unittest.TestCase):
    """Test suite for Crane Game functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # TODO: Initialize test data or resources
        pass
    
    def tearDown(self):
        """Clean up after each test method."""
        # TODO: Clean up any resources created in setUp
        pass
    
    def test_load_csv(self):
        """Test that CSV file loads correctly."""
        # TODO: Fill in test logic
        self.assertTrue(True)  # Placeholder assertion
    
    def test_csv_structure(self):
        """Test that loaded CSV has expected structure/columns."""
        # TODO: Fill in test logic
        self.assertTrue(True)  # Placeholder assertion
    
    def test_data_validation(self):
        """Test that CSV data meets validation requirements."""
        # Find the longest TEST CSV file
        saved_dir = r"C:\Users\stefan\Documents\Unreal Projects\TowerCrane\Saved"
        test_csv_files = glob.glob(os.path.join(saved_dir, "*TEST*.csv"))
        
        if not test_csv_files:
            self.fail("No TEST CSV files found in Saved directory")
        
        # Find the file with the most lines
        file_sizes = [(f, sum(1 for _ in open(f))) for f in test_csv_files]
        longest_file = max(file_sizes, key=lambda x: x[1])[0]
        
        # Load the CSV
        df = pd.read_csv(longest_file)
        
        # Validate that Time column exists
        self.assertIn("Time", df.columns, "Time column not found in CSV")
        
        # Check that max Time value is more than 5 minutes (300 seconds)
        max_time = df["Time"].max()
        five_minutes_seconds = 300
        self.assertGreater(
            max_time, 
            five_minutes_seconds,
            f"Time column max value ({max_time} seconds) must be greater than 5 minutes ({five_minutes_seconds} seconds)"
        )


if __name__ == "__main__":
    unittest.main()

