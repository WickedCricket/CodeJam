# import cj_pyscan
# import cj_pycrack
# import cj_pyscrape
# import cj_pysend

def start():

    print('Welcome to Noroff CodeJam 2022! What would you like to do?\n\
        1. Network Scanner\n\
        2. Password Cracker\n\
        3. DDoS attacker\n\
        4. E-mail Scraper\n\
        5. E-mail Sender')
    

    choice = input('Choice: ')
    match choice:
        case '1':
            pass
            # cj_pyscan.start()
        case '2':
            pass
            # cj_pycrack.start()
        case '3':
            pass
            # cj_ddos.start()
        case '4':
            pass
            # cj_pyscrape.start()
        case '5':
            pass
            # cj_pysend.start()

if __name__ == "__main__":
    start()