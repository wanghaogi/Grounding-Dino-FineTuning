#multimodal-data/images
import os
import json
import csv
import glob

json_dir = "./multimodal-data/images"
csv_file = "merged.csv"
keys = ["label_name","points", "bbox_x", "bbox_y", "bbox_width", "bbox_height", "image_name", "image_width", "image_height"]

def get_width_height(points):
    # points[0] 是左上角的坐标，points[1] 是右下角的坐标
    width = abs(points[1][0] - points[0][0])
    height = abs(points[1][1] - points[0][1])
    return points[0][0], points[0][1], width, height

json_files = glob.glob(os.path.join(json_dir, "*.json"))
data = []

for json_file in json_files:
    with open(json_file, "r") as f:
        json_data = json.load(f)
        shapes_data = json_data.get("shapes", [])

        for item in shapes_data:
            if item.get("label") == "mask":
                continue
            row = {k: v for k, v in item.items() if k in keys}
            x, y, width, height = get_width_height(row.get("points", [[0,0],[0,0]]))
            row["bbox_x"] = x
            row["bbox_y"] = y
            row["bbox_width"] = width
            row["bbox_height"] = height
            row["image_name"] = json_data.get("imagePath", "")
            row["image_width"] = json_data.get("imageHeight", "")
            row["image_height"] = json_data.get("imageWidth", "")
            data.append(row)

try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
except IOError:
    print("I/O error")
