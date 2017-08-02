import os
import pandas as pd
import numpy as np

# Establish the root path, data path and export output path
root_path = os.path.join(os.getcwd(), ".")
data_path = os.path.join(root_path, "raw_data")
output_path = os.path.join(root_path, "output")

# Iterate through the listdir results
filepaths = []
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        filepaths.append(os.path.join(data_path, file))

for file in filepaths:
    df = file
    df_pd = pd.read_csv(df)
    # Total votes cast
    tot_votes = df_pd["Candidate"].count()
    # Make a dataframe of the candidates and the votes cast for each candidate
    cand_votes = df_pd["Candidate"].value_counts()
    cand_votes_df = pd.DataFrame(cand_votes)
    cand_votes_df.columns=["Votes"]
    # Make a list of the candidates and votes cast
    candidate_list = cand_votes_df.index.tolist()
    vote_list = cand_votes_df.iloc[:, 0].tolist()
    # Get the percentage of votes per candidate 

    percent_votes = ((vote_list/tot_votes)*100).round(1)
    percent_list = list(map("{}%".format, percent_votes))
    # Make a dataframe of the voting results
    results_df = pd.DataFrame({
        "Candidate": candidate_list,
        "Number of Votes": vote_list,
        "Percentage of Votes": percent_list
    })
    # Index by number of votes to pull the winner of the election
    win_df = results_df.set_index("Number of Votes")
    win_votes = max(vote_list)
    winner = win_df.loc[win_votes].Candidate

    # Grab the filename from the original path.
    # The _, gets rid of the path. The , _ gets rid of the .csv.
    _, filename = os.path.split(file)
    filename, _ = filename.split(".csv")

    # Print the analysis to the terminal.
    print(
        f"Election Results - {filename}\n"
        f"-----------------------------------------\n"
        f"Total Votes: {tot_votes}\n"
        f"-----------------------------------------\n" 
        f"{results_df.to_string(index=False)}\n"
        f"-----------------------------------------\n" 
        f"Winner: {winner}\n"
    )
    # Export a text file with the results.
    text_path = os.path.join(output_path, filename + ".txt")
    with open(text_path, "w") as text_file:
        text_file.write(
            f"Election Results - {filename}\n"
            f"-----------------------------------------\n"
            f"Total Votes: {tot_votes}\n"
            f"-----------------------------------------\n" 
            f"{results_df.to_string(index=False)}\n"
            f"-----------------------------------------\n" 
            f"Winner: {winner}\n"
        )