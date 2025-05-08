import csv

input_path  = 'report_project2_crawl_en copy.csv'    # replace with your input file
output_path = 'outlinks.csv'   # desired output file

with open(input_path, newline='', encoding='utf-8') as infile, \
     open(output_path, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Copy header
    header = next(reader)
    writer.writerow(header)

    # Process each row, enumerating from 1
    for idx, row in enumerate(reader, start=1):
        url = row[0]
        # Replace the count with “{row_number}.txt”
        new_count = f"{idx}.txt"
        writer.writerow([url, new_count])

print(f"Done! Wrote {idx} rows to {output_path}")
