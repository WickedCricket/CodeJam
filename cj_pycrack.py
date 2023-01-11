import hashlib
import main
from time import sleep
list_of_results = [] # stores the strings containing type of hash, hash and password

# draws the logo when called
def logo():
    print("====================================================================================================")
    print("|    _    _       _     _           _    _           _        _____                _               |")
    print("|   | |  | |     | |   | |         | |  | |         | |      / ____|              | |              |")
    print("|   | |__| |_   _| | __| |_ __ __ _| |__| | __ _ ___| |__   | |     _ __ __ _  ___| | _____ _ __   |")
    print("|   |  __  | | | | |/ _` | '__/ _` |  __  |/ _` / __| '_ \  | |    | '__/ _` |/ __| |/ / _ \ '__|  |")
    print("|   | |  | | |_| | | (_| | | | (_| | |  | | (_| \__ \ | | | | |____| | | (_| | (__|   <  __/ |     |")
    print("|   |_|  |_|\__,_|_|\__,_|_|  \__,_|_|  |_|\__,_|___/_| |_|  \_____|_|  \__,_|\___|_|\_\___|_|     |")
    print("|                                                                                                  |")
    print("====================================================================================================")
    
# asks user if they want to save the cracked hashes to a file
def where_to_save_output(cracked):
    if input("\n Save output to file? (yes/no) :") == "yes" or "y":
        # open a file with user defined name, if not already existing it will create a new one.
        output = open(input(" Output FileName >"), "w")
        # goes thru every item in the list cracked/list_of_results and writes them in the file
        for x in cracked:
            output.write(f"{x}\n")
        # closes the file to not cause errors or corruptions
        output.close()
        # goes back to main menu when done
        input("\nPress Enter To Go Back To Main Menu...")
        main.start()
    else:
        # if user does not want to save the output aka user does not answer "yes" it will just return to main menu
        input("\nPress Enter To Go Back To Main Menu...")
        main.start()
        

def check_hash(password_list, hashes_list):
    # clears screen
    main.clear_screen()
    # calls logo function to draw logo
    logo()
    # opens the file containing hashes and names it "hashes_list"
    with open(hashes_list, 'r', encoding='latin-1') as hashes_list:
        # goes thru the lines of the file and find out what type of hash it is
        for line in hashes_list:
            # strips spaces from front and back of the hash to make it more accurate
            current_hash = line.strip()
            # compares the length of the current hash to an example one to determine if its the same length.
            if len(current_hash)==len(range(32)) and current_hash.isdigit()==False and current_hash.isalpha()==False and current_hash.isalnum()==True:
                # appends the result of crack_hash(current_hash, type, password_list) to a list called list_of_results. This would look something like this "type | hash:password"
                list_of_results.append(crack_hash(current_hash, "md5", password_list))

            elif len(current_hash)==len(range(128)) and current_hash.isdigit()==False and current_hash.isalpha()==False and current_hash.isalnum()==True:
                list_of_results.append(crack_hash(current_hash, "sha512", password_list))

            elif len(current_hash)==len(range(64)) and current_hash.isdigit()==False and current_hash.isalpha()==False and current_hash.isalnum()==True:
                list_of_results.append(crack_hash(current_hash, "sha256", password_list))

            elif len(current_hash)==len(40) and current_hash.isdigit()==False and current_hash.isalpha()==False and current_hash.isalnum()==True:
                list_of_results.append(crack_hash(current_hash, "sha1", password_list))

            else:
                # if a hash in the file does not match with the parameters of any of the types it will print an error
                print(f"Could not Identify the hash type | {current_hash}")
        # when all the hashes have been cracked you will be sendt to where_to_save_output with all the cracked hashes to choose if you want to save the output 
        where_to_save_output(list_of_results)
        
# this is where the hashes are "cracked" or compared to hashed passwords to see if any match
def crack_hash(hash, hash_type, password_list):
    # opens the file containing all the passwords and names it password_list
    with open(password_list, 'r', encoding='latin-1') as password_list:
        # goes thru one by one line in the password list to hash it and compare it to the current hash
        for line in password_list:
            try:
                # strips the string for spaces
                current_password = line.strip()
                # hashes the current password with the hash type of the current hash
                if hash_type == "md5":
                    hashed_password = hashlib.md5(current_password.encode("utf-8")).hexdigest()
                elif hash_type == "sha1":
                    hashed_password = hashlib.sha1(current_password.encode("utf-8")).hexdigest()
                elif hash_type == "sha256":
                    hashed_password = hashlib.sha256(current_password.encode("utf-8")).hexdigest()
                elif hash_type == "sha512":
                    hashed_password = hashlib.sha512(current_password.encode("utf-8")).hexdigest()
                else:
                    # if there is a error with hashing the password it will print a error
                    print("[!] error while hashing password in password list")
            except:
                print("[!] error while hashing password in password list")
            # if one of the hashed passwords matches a hash in the hash file it will print it to the console and return it to get appended to the list_of_results list
            if hashed_password == hash:
                print(f"{hash_type} | {hashed_password}:{current_password}")
                return f"{hash_type} | {hashed_password}:{current_password}"
        # if none of the hashed password could be matched with the current hash it will print that it cant crack that hash       
        print(f"Could not find password for hash | {hash}")
        
# function to get user input of the hash file and password file to be used for cracking
def send_hash_and_passwords():
    try:
        # tries to send the hash list and password list to the function check_hash
        check_hash(hashes_list=input("\n List Of Hashes > "), password_list=input(" Password List > "))
        # if it doesnt find the provided files you specified it will tell you and let you try again
    except FileNotFoundError:
        input("[!] Cant find one of the files, Try Again! (Press Enter To Continue...)")
        send_hash_and_passwords()
        # lets you exit out of the function with CTRL + C. incase you get stuck
    except KeyboardInterrupt:
        start()
    
# start of the program, this is where the main python script would call to start the pycracker
def start():
    # calls clear_screen() function from main.py to clear screen
    main.clear_screen()
    logo() # draws logo
    print("==================================")
    print("| 1. Start Cracking              |")
    print("| 2. About                       |")
    print("| 3. Return                      |")
    print("==================================")
    print("| [!] Supported hash types:      |")
    print("|     md5, sha1, sha256, sha512  |")
    print("==================================")

    option = input("\n option >")
    if option == "1":
        main.clear_screen()
        logo()
        send_hash_and_passwords()

    elif option == "2":
        main.clear_screen()
        print("==================================")
        print("|        ~~ About ~~             |")
        print("====================================================================================")
        print("| User inputs a list of hashes and a password list.                                |")
        print("| It can then identify the type of hashes in the list and attempt                  |")
        print("| to crack them by hashing the passwords in the password list and                  |")
        print("| comparing them with the hashes in the provided hash list. If a match is found,   |")
        print("| the program will print the hash type (e.g. SHA256, SHA512, etc.),                |")
        print("| followed by the matching hash and password.                                      |")
        print("====================================================================================")
        print("| Enter to return |")
        print("===================")
        input()
        start()    
    elif option == "3":
        main.start()
    else:
        print("\n [!] Invalid Option, Try Again")
        sleep(1)
        start()