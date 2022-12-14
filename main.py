import cj_pyscan
# import cj_pycrack
import cj_pyscrape
# import cj_pysend
# import cj_ddos
import cj_pytest
import os

def start():

    print('Welcome to Noroff CodeJam 2022! What would you like to do?\n\
        1. Network Scanner\n\
        2. Password Cracker\n\
        3. DDoS attacker\n\
        4. E-mail Scraper\n\
        5. E-mail Sender\n\
        6. Test')
    
    

    choice = input('Choice: ')
    clear_screen()
    match choice:
        case '1':
            pass
            cj_pyscan.start()
        case '2':
            pass
            # cj_pycrack.start()
        case '3':
            pass
            # cj_ddos.start()
        case '4':
            pass
            cj_pyscrape.start()
        case '5':
            pass
            # cj_pysend.start()
        case '6':
            pass
            cj_pytest.loading_screen()

def clear_screen():
    try:
        os.system("cls")
    except:
        os.system("clear")
 
if __name__ == "__main__":
    start()