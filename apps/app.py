import re
import os
from collections import defaultdict

# Read the file into memory
print("Reading...")

with open("titles_and_views.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize defaultdict to store article names and views
print("Creating dictionary...")
articles = defaultdict(int)
articles = {article: int(views) for article, views in [line.strip().split("|") for line in lines]}

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

    searchedCount = 0

    # Loop through the keys of the dictionary to find the matching articles and their views
    matching_articles = {article: views for article, views in articles.items() if regex.search(article)}

    # Sort matching articles by number of views (in descending order)
    print("Sorting...")
    matching_articles = sorted(matching_articles.items(), key=lambda x: x[1], reverse=False)


    # Print list of matching articles and views as a table
    max_article_length = max([len(article) for article, _ in matching_articles])
    print("_"*os.get_terminal_size().columns)
    for article, views in matching_articles:
        print(f"{article.ljust(max_article_length)} | {views}")
    print("‾"*os.get_terminal_size().columns)

    # Prompt user for new search
    response = input("Perform another search? (y/n): ")
    if response.lower() != "y":
        break
    os.system('cls')