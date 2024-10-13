import pandas as pd
import unittest

class LineageTracker:
	def __init__(self):
		self.lineage = []

	def log_transformation(self, step_name, input_datasets, output_dataset):
		self.lineage.append({
			"step": step_name,
			"inputs": input_datasets,
			"output": output_dataset
		})

	def get_lineage(self):
		return self.lineage

def data_processing_pipeline(lt):
	# Sample data
	data = {
		"name": ["David", "John", "Thomas"],
		"age": [20, 30, 28]
	}
	df = pd.DataFrame(data)

	lt.log_transformation("Data Load", [], "input_data.csv")

	# Data transformation step 1: Uppercasing names
	df['name'] = df['name'].str.upper()
	lt.log_transformation("Uppercase Names", ["input_data.csv"], "processed_data_step1.csv")

	# Data transformation step 2: Adding a new column
	df['age_plus_one'] = df['age'] + 1
	lt.log_transformation("Add Age Plus One", ["processed_data_step1.csv"], "output_data.csv")

	return df

class TestDataTransparency(unittest.TestCase):
	def test_lineage_tracking(self):
		lt = LineageTracker()
		result_df = data_processing_pipeline(lt)

		expected_lineage = [
			{
				"step": "Data Load",
				"inputs": [],
				"output": "input_data.csv"
			},
			{
				"step": "Uppercase Names",
				"inputs": ["input_data.csv"],
				"output": "processed_data_step1.csv"
			},
			{
				"step": "Add Age Plus One",
				"inputs": ["processed_data_step1.csv"],
				"output": "output_data.csv"
			}
		]
		self.assertEqual(lt.get_lineage(), expected_lineage, "Lineage tracking failed")

if __name__ == "__main__":
	unittest.main()
