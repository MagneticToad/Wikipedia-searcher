# Open the input and output files with utf-8 encoding
with open('titles_and_views_all.txt', 'r', encoding='utf-8') as input_file, open('titles_and_views_greater_than_10000.txt', 'a', encoding='utf-8') as output_file:
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
        # Check if the view count is greater than 10000
        if view_count > 10000:
            # If yes, append the line to the output file
            output_file.write(line)
        # Increment the lines processed counter
        lines_processed += 1
        # Every 10000 lines, output the percentage progress
        if lines_processed % 10000 == 0:
            progress_percent = lines_processed / total_lines * 100
            print(f"Progress: {progress_percent:.2f}%")
