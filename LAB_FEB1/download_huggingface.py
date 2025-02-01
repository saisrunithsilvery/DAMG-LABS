from datasets import load_dataset

# Load the dataset
dataset = load_dataset("gaia-benchmark/GAIA", "2023_all")

# Save the dataset to disk
dataset.save_to_disk("./GAIA_2023_all")
