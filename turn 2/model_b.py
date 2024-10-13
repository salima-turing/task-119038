class DataSource:
    def __init__(self, name):
        self.name = name

class DataTransformation:
    def __init__(self, name, input_data_sources):
        self.name = name
        self.input_data_sources = input_data_sources

class DataOutput:
    def __init__(self, name, input_data_transformation):
        self.name = name
        self.input_data_transformation = input_data_transformation

class LineageTracker:
    def __init__(self):
        self.lineage = {}

    def add_data_source(self, data_source):
        self.lineage[data_source.name] = {
            "type": "DataSource",
            "inputs": [],
            "outputs": []
        }

    def add_data_transformation(self, data_transformation):
        self.lineage[data_transformation.name] = {
            "type": "DataTransformation",
            "inputs": [src.name for src in data_transformation.input_data_sources],
            "outputs": []
        }
        for src in data_transformation.input_data_sources:
            self.lineage[src.name]["outputs"].append(data_transformation.name)

    def add_data_output(self, data_output):
        self.lineage[data_output.name] = {
            "type": "DataOutput",
            "inputs": [data_output.input_data_transformation.name],
            "outputs": []
        }
        transfromation_name = data_output.input_data_transformation.name
        self.lineage[transfromation_name]["outputs"].append(data_output.name)

    def get_lineage(self, data_item_name):
        return self.lineage.get(data_item_name, {})

    def print_lineage(self, data_item_name):
        lineage = self.get_lineage(data_item_name)
        if lineage:
            print(f"Lineage for '{data_item_name}':")
            print(f"Type: {lineage['type']}")
            print("Inputs:")
            for input_name in lineage["inputs"]:
                print(f"  - {input_name}")
            print("Outputs:")
            for output_name in lineage["outputs"]:
                print(f"  - {output_name}")
        else:
            print(f"Item '{data_item_name}' not found in lineage.")

# Example Usage:
if __name__ == "__main__":
    # Create lineage tracker
    tracker = LineageTracker()

    # Define data sources, transformations, and outputs
    source_a = DataSource("Source_A")
    source_b = DataSource("Source_B")

    transform_1 = DataTransformation("Transform_1", [source_a, source_b])

    output_1 = DataOutput("Output_1", transform_1)

    # Add to lineage tracker
    tracker.add_data_source(source_a)
    tracker.add_data_source(source_b)
    tracker.add_data_transformation(transform_1)
    tracker.add_data_output(output_1)

    # Print lineage for a specific data item
    tracker.print_lineage("Transform_1")
