threshold = int(input("Keep articles with view count greater than: "))

# Open the input and output files with utf-8 encoding
with open('../data/titles_and_views_all.txt', 'r', encoding='utf-8') as input_file, open(f'../data/titles_and_views_greater_than_{threshold}.txt', 'a', encoding='utf-8') as output_file:
    # Get the total number of lines in the input file
    total_lines = sum(1 for line in input_file)
    # Reset the file pointer to the beginning of the file
    input_file.seek(0)
    # Initialize a counter for the number of lines processed
    lines_processed = 0
    # Loop through each line in the input file
    for line in input_file:
        # Split the line into title and view count
        title, view_count = line.strip().split('|')
        # Convert the view count to an integer
        view_count = int(view_count)
        # Check if the view count is greater than threshold
        if view_count > threshold:
            # If yes, append the line to the output file
            output_file.write(line)
        # Increment the lines processed counter
        lines_processed += 1
        # Every 100000 lines, output the percentage progress
        if lines_processed % 100000 == 0:
            progress_percent = lines_processed / total_lines * 100
            print(f"Progress: {progress_percent:.2f}%")
