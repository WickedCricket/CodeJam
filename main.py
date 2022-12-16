import cj_pyscan
import cj_pycrack
import cj_pyscrape
# import cj_pysend
# import cj_ddos
import cj_pytest
import os


def start():
    clear_screen()
    print('\n\
    ██████████████████████████████████████████████████████████████\n\
                                                                  \n\
    █ █ █ █ █ █ █ █ █ █ █ [codejam 2022/2023]█ █ █ █ █ █ █ █ █ █ █\n\
     █ █ █ █ █ █ █ █ █ █ █[@ Noroff students] █ █ █ █ █ █ █ █ █ █ \n')
    print(" _    _           _       _                ")
    print("| |  | |         | |     | |               ")
    print("| |__| |  _   _  | |   __| |  _ __    __ _ ")
    print("|  __  | | | | | | |  / _` | | '__|  / _` |")
    print("| |  | | | |_| | | | | (_| | | |    | (_| |")
    print("|_|  |_|  \__,_| |_|  \__,_| |_|     \__,_|\n")      
    print(" ")                         
    print('         What would you like to do?\n\
        _________________________\n\
        |                       |\n\
        |   1. Network Scanner  |\n\
        |   2. Password Cracker |\n\
        |   3. DDoS attacker    |\n\
        |   4. E-mail Scraper   |\n\
        |   5. E-mail Sender    |\n\
        |   6. Test             |\n\
        |   0. Exit             |\n\
        |_______________________|\n\
            ')
    
    choice = input('Choice: ')
   
    match choice:
        case '1': cj_pyscan.start()
        case '2': cj_pycrack.start()
        case '3': pass # cj_ddos.start()
        case '4': cj_pyscrape.start(emails=None)
        case '5': pass # cj_pysend.start()
        case '6': pass # cj_pytest.loading_screen()
        case '0': print("Exiting.."); quit()
        case default: start()

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
 
if __name__ == "__main__":
    start()

