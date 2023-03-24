import re
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# Read the file into memory
print("Reading...")
with open("1-12000000.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize defaultdict to store article names and views
print("Creating dictionary...")
articles = defaultdict(int)

# Define a function to process a chunk of lines
def process_lines(lines_chunk):
    for line in lines_chunk:
        article, views = line.strip().split("|")
        articles[article] += int(views)

# Split the lines into smaller chunks
chunk_size = 1000000
line_chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]

# Process the chunks using multithreading
print("Processing lines...")
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_lines, chunk) for chunk in line_chunks]
    for future in futures:
        future.result()

# Compile regular expression
regex = re.compile("", re.IGNORECASE)

while True:
    # Get user input for regex expression
    regex_string = input("Enter regex expression: ")
    print("Searching...")

    # Update compiled regular expression if necessary
    if regex_string != regex.pattern:
        regex = re.compile(regex_string, re.IGNORECASE)

    # Initialize temporary list
    matching_articles = []

    # Find the matching articles and their views using multithreading
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(lambda article_views: (article_views[0], article_views[1]), (article, views)) for article, views in articles.items() if regex.search(article)]
        for future in futures:
            matching_articles.append(future.result())

    # Sort matching articles by number of views (in descending order)
    print("Sorting...")
    matching_articles = sorted(matching_articles, key=lambda x: x[1], reverse=False)

    # Print list of matching articles and views as a table
    max_article_length = max([len(article) for article, _ in matching_articles])
    for article, views in matching_articles:
        print(f"{article.ljust(max_article_length)} | {views}")

    # Prompt user for new search
    response = input("Perform another search? (y/n): ")
    if response.lower() != "y":
        break
    os.system('cls')
