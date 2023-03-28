import csv

file = input("File to normalise: ")
# Open the input and output files
with open(f'../data/{file}.txt', 'r', encoding='utf-8') as infile, open(f'../data/{file}_normalised.txt', 'w', encoding='utf-8') as outfile:

    # Read the input file as a CSV file with the '|' separator
    reader = csv.reader(infile, delimiter='|')

    # Reset the file pointer to the beginning of the file
    infile.seek(0)

    # Read the input file again as a CSV file
    reader = csv.reader(infile, delimiter='|')

    # Write the normalised view counts to the output file
    writer = csv.writer(outfile, delimiter='|')
    for row in reader:
        view_count = int(row[1])
        normalised_view_count = round((view_count / 768819502) * 100) #normalise based on the view count of the article "Donald_Trump"
        writer.writerow([row[0], str(normalised_view_count)])
