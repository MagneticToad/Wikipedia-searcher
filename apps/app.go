package main

import (
    "bufio"
    "fmt"
	"os"
    "os/exec"
    "regexp"
    "sort"
    "strconv"
    "strings"
    "time"
)

type article struct {
    title string
    views int
}

func main() {
    // read the file into memory
    fmt.Println("Reading file...")
    start := time.Now()
    file, err := os.Open("../data/titles_and_views_greater_than_10000.txt")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    var allArticles []article
    
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()
        parts := strings.Split(line, "|")

        // parse the view count as an integer
        views, err := strconv.Atoi(strings.TrimSpace(parts[1]))
        if err != nil {
            fmt.Println("Error parsing view count:", err)
            return
        }

        // create an article struct
        a := article{title: strings.TrimSpace(parts[0]), views: views}
        allArticles = append(allArticles, a)
    }
    elapsed := time.Since(start)
    fmt.Printf("Read file in %s\n", elapsed)

    for {
        // prompt the user to enter a regular expression
        fmt.Print("Enter a regular expression: ")
        scanner := bufio.NewScanner(os.Stdin)
        scanner.Scan()
        regexStr := scanner.Text()

        // compile the regular expression
        regex, err := regexp.Compile("(?i)" + regexStr)
        if err != nil {
            fmt.Println("Invalid regular expression:", err)
            continue
        }

		maxTitleLen := 0
        // filter the articles that match the regular expression
        fmt.Println("Filtering articles...")
        start = time.Now()
        var articles []article
        for _, a := range allArticles {
            if regex.MatchString(a.title) {
                articles = append(articles, a)

                // track the maximum title length for later formatting
                if len(a.title) > maxTitleLen {
                    maxTitleLen = len(a.title)
                }
            }
        }
        elapsed = time.Since(start)
        fmt.Printf("Filtered articles in %s\n", elapsed)

        // sort the articles by view count in ascending order
        fmt.Println("Sorting articles...")
        start = time.Now()
        sort.Slice(articles, func(i, j int) bool {
            return articles[i].views < articles[j].views
        })
        elapsed = time.Since(start)
        fmt.Printf("Sorted articles in %s\n", elapsed)

        
        // print the matching articles in a table
        if len(articles) == 0 {
            fmt.Println("No matching articles found")
        } else {
            fmt.Printf("%-*s | Views\n", maxTitleLen, "Title")
            fmt.Println(strings.Repeat("-", maxTitleLen+9))
            for _, a := range articles {
                fmt.Printf("%-*s | %d\n", maxTitleLen, a.title, a.views)
            }
        }

        // print a separator line and prompt the user to perform another search
        fmt.Println(strings.Repeat("-", 80))
        fmt.Print("Perform another search? (y/n): ")
        scanner = bufio.NewScanner(os.Stdin)
        scanner.Scan()
        answer := strings.ToLower(scanner.Text())
		if answer != "y" && answer != "yes" {
            break
        }

		// clear the console
        cmd := exec.Command("cmd", "/c", "cls")
        cmd.Stdout = os.Stdout
        cmd.Run()

    }
}
