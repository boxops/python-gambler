# reset budget
import json

records_file = "records.json"
budget = 10000
with open(records_file, "w") as wr:
    data = {"budget": budget}
    json.dump(data, wr)
