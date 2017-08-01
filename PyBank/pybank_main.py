import os
import csv

# Establish the root path, data path and export output path
root_path = os.path.join(os.getcwd(), ".")
data_path = os.path.join(root_path, "raw_data")
output_path = os.path.join(root_path, "output")

# Iterate through the listdir results
filepaths = []
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        filepaths.append(os.path.join(data_path, file))

# Using csv.DictReader()
for file in filepaths:
    tot_revenue = 0
    month_count = 0
    revenue = 0
    rev_change = 0
    data_dict_list = []
    with open(file, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Creating new revenue difference per month dictionary to calculate greatest inc/dec.
            rev_diff = {"rev_diff": int("{Revenue}".format(**row)) - revenue}
            rev_change = rev_change + int("{Revenue}".format(**row)) - revenue
            revenue = int("{Revenue}".format(**row))
            tot_revenue += revenue
            month_count += 1
            data_dict_list.append({**row, **rev_diff})
        # Turn dictionary housing max and min rev_diff values as indvidual dicts outside of list.
        increase_dict = dict(max(data_dict_list, key=lambda x:x["rev_diff"]))
        decrease_dict = dict(min(data_dict_list, key=lambda x:x["rev_diff"]))
        # Pull date and rev_diff values for the corresponding greatest inc/dec months.
        increase_date = increase_dict.get("Date")
        increase_revdiff = increase_dict.get("rev_diff")
        decrease_date = decrease_dict.get("Date")
        decrease_revdiff = decrease_dict.get("rev_diff")
        # Adjust rev_diff to discount first row.
        first_row = data_dict_list[0]
        first_row_revdiff = first_row.get("rev_diff")
        rev_change = rev_change - first_row_revdiff
        avg_change = int(rev_change/(month_count - 1))
        
        # Grab the filename from the original path.
        # The _, gets rid of the path. The , _ gets rid of the .csv.
        _, filename = os.path.split(file)
        filename, _ = filename.split(".csv")     
        # Print the analysis to the terminal.
        print(
            f"Financial Analysis - {filename}\n"
            f"----------------------------\n"
            f"Total Months: {month_count}\n" 
            f"Total Revenue: ${tot_revenue}\n"
            f"Average Revenue Change: ${avg_change}\n"
            f"Greatest Increase in Revenue: {increase_date} (${increase_revdiff})\n"
            f"Greatest Decrease in Revenue: {decrease_date} (${decrease_revdiff})\n"
        )

        # Export a text file with the results.
        text_path = os.path.join(output_path, filename + ".txt")
        with open(text_path, "w") as text_file:
            text_file.write(
                f"Financial Analysis: {filename}\n"
                f"----------------------------\n"
                f"Total Months: {month_count}\n" 
                f"Total Revenue: ${tot_revenue}\n"
                f"Average Revenue Change: ${avg_change}\n"
                f"Greatest Increase in Revenue: {increase_date} (${increase_revdiff})\n"
                f"Greatest Decrease in Revenue: {decrease_date} (${decrease_revdiff})\n"
            )