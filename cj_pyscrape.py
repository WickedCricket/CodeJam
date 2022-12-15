# This program should request a URL from the user, then scrape the email addresses from the page and print them to the screen.
# Author: imSiddis
import sys
import re
import urllib.request
import main
import bs4
import threading
import time
#===============#
# Build version #
#===============#
build_num = 0.1

#=========================#
# Ascii / UTF-8 error fix #
#=========================#
#text = "æ", "ø", "å", "Æ", "Ø", "Å"
#encoded_text = text.encode("ascii", errors="replace")

def get_url():
    url = input("Enter a URL: ")
    try: # This will check if the URL starts with http:// or https://
        if url.startswith("http://") or url.startswith("https://"):
            pass
        elif not url.startswith("http://") or not url.startswith("https://"): # This will check if the URL starts with http:// or https://
            url = "https://" + url # If it doesn't, it will add https:// to the start of the URL
    except urllib.error.URLError as e:
        print("Error: Invalid URL.")
        sys.exit()
    return url

def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}) # This will add a user-agent to the request
    html = urllib.request.urlopen(req).read() # This will read the HTML from the URL
    return html

def get_emails(html):
    email_list = []
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', str(html)) # This regex will find all email addresses on the page
    email_list.append(emails)
    return email_list

# This function removes duplicates from the list returned by getEmails()
# It will use a set to remove duplicates, then convert the set back to a list
def remove_duplicates(emails):
    email_list = []
    for email in emails:
        no_duplicates = list(set(email)) # This will remove duplicates from the list
        for i in no_duplicates:
            email_list.append(i)
        return email_list # This will return the list without duplicates

# A function that will remove emails not ending with TDL like .com, .net, .org, etc.
def remove_invalid_emails(emails):
    email_endwith = [".no",".se",".com",".uk",".to",".net",
                    ".gov",".org",".edu",".mil",".int",".arpa",
                    ".biz",".aero",".coop",".info",".name",".pro",
                    ".museum",".coop",".travel",".mobi",".cat",".jobs",
                    ".tel",".asia",".post",".edu",".mil",".net",
                    ".org",".biz",".info",".name",".pro",".aero",".coop",".museum",
                    ".int",".travel",".post",".jobs",".mobi",".tel",".xxx",".ac",".ad",
                    ".ae",".af",".ag",".ai",".al",".am",".an",".ao",".aq",".ar",".as",".at",".au",
                    ".aw",".az",".ba",".bb",".bd",".be",".bf",".bg",".bh",".bi",".bj",".bm",".bn",
                    ".bo",".br",".bs",".bt",".bv",".bw",".by",".bz",".ca",".cc",".cd",".cf",".cg",
                    ".ch",".ci",".ck",".cl",".cm",".cn",".co",".cr",".cu",".cv",".cx",".cy",".cz",
                    ".de",".dj",".dk",".dm",".do",".dz",".ec",".ee",".eg",".eh",".er",".es",".et",
                    ".fi",".fj",".fk",".fm",".fo",".fr",".ga",".gb",".gd",".ge",".gf",".gg",".gh",
                    ".gi",".gl",".gm",".gn",".gp",".gq",".gr",".gs",".gt",".gu",".gw",".gy",".hk",
                    ".hm",".hn",".hr",".ht",".hu",".id",".ie",".il",".im",".in",".io",".iq",".ir",
                    ".is",".it",".je",".jm",".jo",".jp",".ke",".kg",".kh",".ki",".km",".kn",".kp",
                    ".kr",".kw",".ky",".kz","."]
    valid_emails = [remove_duplicates(emails)]
    for email in emails:
        for i in email_endwith:
            if email.endswith(i):
                valid_emails.append(email)
    return valid_emails

def print_emails(emails):
    main.clear_screen()
    purged_emails = remove_invalid_emails(emails)
    emails = purged_emails[1:]
    print("=========================================")
    print("|    ~~ Emails found on the page ~~     |")
    print("=========================================")
    for email in emails:
        print(email)
    print("=========================================")
    print("          ~~ End of emails ~~           ")
    print("     \tTotal emails found: " + str(len(emails)))
    print("=========================================")

# A function to append the non-duplicate emails to a file.
def save_emails(emails):
    purged_emails = remove_invalid_emails(emails)
    emails = purged_emails[1:]
    with open("emails.txt", "a") as file: 
        for email in emails:
            file.write(email + "\n")
    print("=========================================")
    print("          ~~ Emails Scraped ~~           ")
    print("     \tTotal emails saved: " + str(len(emails)))
    print("=========================================")
    input("Press Enter to return to menu.")
    main.start()

#=====================#
# The Crawler Section #
#   ~ Starts here ~   #
#=====================#
class Spider:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.emails = []
        self.visited = []

    def get_links(self):
        req = urllib.request.Request(
            self.url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        )
        html = urllib.request.urlopen(req).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                if href.startswith("http"):
                    self.links.append(href)
                elif href.startswith("/"):
                    self.links.append(self.url + href)
                else:
                    self.links.append(self.url + "/" + href)
        return self.links

    def get_emails(self):
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', self.url)  # This regex will find all email addresses on the page
        self.emails += emails
        return self.emails

    def crawl(self, hops):
        self.get_links()
        self.get_emails()
        self.visited.append(self.url)
        if hops > 0:
            for link in self.links:
                if link not in self.visited:
                    spider = Spider(link)
                    spider.crawl(hops - 1)
                    self.visited += spider.visited
                    self.emails += spider.emails
        return self.emails

    def get_url():
        url = input("Enter a URL: ")
        try: # This will check if the URL starts with http:// or https://
            if url.startswith("http://") or url.startswith("https://"):
                pass
            elif not url.startswith("http://") or not url.startswith("https://"): # This will check if the URL starts with http:// or https://
                url = "https://" + url # If it doesn't, it will add https:// to the start of the URL
        except urllib.error.URLError as e:
            print("Error: Invalid URL.")
            sys.exit()
        return url

# Crawler threading function.
def crawl_thread(url, hops):
    spider = Spider(url)
    emails = spider.crawl(hops)
    print_emails(emails)

# This function will start the crawl by requesting the user to input the URL and the number of hops.
def start_crawl():
    main.clear_screen()
    print(f"====================| MailScrape v{build_num} |=====================")
    print("|                      By imSiddis                         |")
    print("============================================================")
    print("| This program will scrape email addresses from a website. |")
    print("| It will then print them to the screen or save them to a  |")
    print("| file.                                                    |")
    print("============================================================")
    print(" ")
    url = Spider.get_url()
    hops = int(input("Enter the number of hops: "))
    # Request the user to input the number of threads they want to use.
    threads = int(input("Enter the number of threads to use: "))
    # Create a list of threads.
    thread_list = []
    # Create a list of emails.
    emails = []
    # Create a list of visited links.
    visited = []
    # Create a list of links.
    links = []
    # Start the threads.
    for i in range(threads):
        thread = threading.Thread(target=crawl_thread, args=(url, hops))
        thread_list.append(thread)
        thread.start()
        time.sleep(1)
        if links in visited:
            pass
        else:
            visited.append(links)
    # Join the threads.
    for thread in thread_list:
        thread.join()
    # Get the emails.
    for thread in thread_list:
        emails += thread.emails
    # Validate the emails.
    valid_emails = remove_invalid_emails(emails)
    # Remove duplicates.
    valid_emails = remove_duplicates(valid_emails)
    # Print the emails.
    print_emails(valid_emails)

#=====================#
# The Crawler Section #
#    ~ Ends here ~    #
#=====================#

#=====================#
#   The Menu Section  #
#   ~ Starts here ~   #
#=====================#

# This function will print the program's information
def about():
    main.clear_screen()
    print(f"====================| MailScrape v{build_num} |=====================")
    print("|                      by imSiddis.                        |")
    print("============================================================")
    print("| This program will scrape email addresses from a website. |")
    print("| It will then print them to the screen or save them to a  |")
    print("| file.                                                    |")
    print("============================================================")

# A menu function to allow the user to choose what they want to do with the emails
# This menu should be called before the emails have been scraped and sorted.

def start(emails):
    main.clear_screen()
    print(f"====================| MailScrape v{build_num} |=====================")
    print("|                      By imSiddis                         |")
    print("============================================================")
    print("| This program will scrape email addresses from a website. |")
    print("============================================================")
    print("What would you like to do with the emails?")
    print("1. Print emails to screen")
    print("2. Save emails to file")
    print("3. Crawl site for emails (Currently not working)")
    print("4. About")
    print("0. Back")
    choice = input("Enter your choice: ")
    if choice == "1":
        url = get_url()
        html = get_html(url)
        emails = get_emails(html)
        no_duplicates = remove_duplicates(emails)
        sorted_emails = sorted(no_duplicates)
        print_emails(sorted_emails)
        input("Press enter to return to the menu") # This will pause the program until the user presses enter
        start(emails)
        
    elif choice == "2":
        url = get_url()
        html = get_html(url)
        emails = get_emails(html)
        no_duplicates = remove_duplicates(emails)
        sorted_emails = sorted(no_duplicates)
        save_emails(sorted_emails)
    
    elif choice == "3":
        pass
        #start_crawl()
    elif choice == "4":
        about()
        input("Press enter to return to the menu") # This will pause the program until the user presses enter
        print("\n\n\n\n\n\n")
        start(emails)
    elif choice == "0":
        confirm_exit()
    else:
        print("Invalid choice")
        start(emails)


# Confirm exit
def confirm_exit():
    print("Are you sure you want to exit? (Y/n)") # Ask the user if they want to exit
    choice = input("Enter your choice: ")
    if choice == "Y" or choice == "y" or choice == "":
        print("Exiting...")
        main.start()
    elif choice == "N" or choice == "n":
        start(emails=get_url)
    else:
        print("Invalid choice")
        confirm_exit()

#=====================#
#   The Menu Section  #
#    ~ Ends here ~    #
#=====================#