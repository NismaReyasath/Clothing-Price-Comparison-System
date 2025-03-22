import json

# Load Myntra Data
with open("data.json", "r") as f:
    myntra_data = json.load(f)

# Load Meesho Data
with open("meesho_data.json", "r") as f:
    meesho_data = json.load(f)

# Merge data
combined_data = {"myntra": myntra_data, "meesho": meesho_data}

# Save to new file
with open("combined_data.json", "w") as f:
    json.dump(combined_data, f, indent=4)

print("Combined data saved to combined_data.json!")
