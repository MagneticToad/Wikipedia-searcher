import re

while True:
    # Get user input for regex expression
    regex = input("Enter regex expression: ")
    print("Searching...")

    # Open file for reading in binary mode with encoding parameter
    with open("1-3000000.txt", "rb") as file:
        # Initialize temporary list
        matching_articles = []
        
        # Read each line in the file
        for line in file:
            # Decode line to string and split into article name and views
            article, views = line.decode('utf-8').strip().split("|")
            
            # Check if article matches regex expression (case-insensitive)
            if re.search(regex, article, re.IGNORECASE):
                # If it does, add it to temporary list
                matching_articles.append((article, int(views)))
        
        # Sort temporary list by number of views (in descending order)
        matching_articles.sort(key=lambda x: x[1], reverse=True)
        
        # Print list of matching articles and views as a table
        max_article_length = max([len(article) for article, _ in matching_articles])
        for article, views in matching_articles:
            print(f"{article.ljust(max_article_length)} | {views}")
        
        # Prompt user for new search
        response = input("Perform another search? (y/n): ")
        if response.lower() != "y":
            break
