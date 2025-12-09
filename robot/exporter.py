import csv

def export_path(path, filename):
    """
    Saves the path as a CSV file: row, col
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["row", "col"])

        for (r, c) in path:
            writer.writerow([r, c])
