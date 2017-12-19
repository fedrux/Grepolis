
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from random import randint


###############
MODIFICA QUESTI PARAMETRI
###############
numero_citta = 1
citta_riferimento = "----nome citta riferimento-----"
username = ""
password = ""




##############
INIZIO
##############


# senato, caverna, legno, pietra, argento, mercato, porto, casema, muro, magazzino, fattoria, accademia, tempio, terme, torre

matrix_buildings = [
    [24, 10, 40, 40, 40, 17, 20, 20, 25, 25, 45, 30, 17, 1, 1],
    [24, 10, 40, 40, 40, 17, 20, 20, 25, 25, 45, 30, 17, 1, 1],
    [24, 10, 40, 40, 40, 17, 20, 20, 25, 25, 45, 30, 17, 1, 1],
]

matrix_caserma = [
    [0, 0, 0, 0, 0, 0, 0, 0, 50, 0], # full manticore
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #full mare
    [500, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

matrix_porto = [
    [0, 0, 40, 0, 0, 0, 0, 0, 0, 0], # full manticore
    [0, 0, 330, 0, 0, 0, 0, 0, 0, 0], #full ince
    [0, 200, 0, 0, 0, 0, 0, 0, 0, 0],
]





def rand_time():
    return (0.5 + randint(0, 15)/10)


def get_nome_citta(br):
    name = br.find_element_by_css_selector(".town_name").text
    return name


def next_town(br):
    try:
        search = br.find_element_by_css_selector(".btn_next_town")
        search.click()
        search = br.find_element_by_css_selector(".btn_jump_to_town")
        search.click()
        print(get_nome_citta(br))
        print("prossima citta")
        time.sleep(rand_time())
    except NoSuchElementException:
        print("impossibile cambiare citta")


    


br = webdriver.Chrome()


TEMPO = 300 # 10 minuti di tempo refrattario

#start it up
print("Avvio di chrome....")
print(rand_time)


br.get("https://it.grepolis.com/")

time.sleep(3)
#To fill out a form    ui-button-text

search = br.find_element_by_name('login[userid]')
search.send_keys(username)
search = br.find_element_by_name('login[password]')
search.send_keys(password)
search = br.find_element_by_name("login[Login]")
search.send_keys(Keys.RETURN)

time.sleep(5)

search = br.find_elements_by_css_selector(".world_name div")
a = 0
for i in search:
    if(a == 1):#NUMERO DEL MONDO CHE COMPARE IN ORDINE NELLA SCHERMATA DOPO LOGIN
        i.click()
    a += 1


print("Avvio Gioco")

time.sleep(10)


try:
    search = br.find_element_by_css_selector(".js-tooltip-resources div")
    search.click()
    time.sleep(5)
except NoSuchElementException:
    print("Nessun bonus giornaliero")





#allinea citta
while(True):
    if get_nome_citta(br) == citta_riferimento:
        print("trovata")
        break
    else:
        next_town(br)
    

 


while(True):
    
    try:
        search = br.find_elements_by_css_selector(".world_name div")
        a = 0
        for i in search:
            if(a == 1):
                i.click()
                print("Avvio Gioco")
                time.sleep(10)
            a += 1
    except:
        print("gia all'interno del gioco")
        
        
    try:
        search = br.find_element_by_css_selector(".island_view div")
        search.click()
        search = br.find_element_by_css_selector(".btn_jump_to_town div")
        search.click()
        print("visuale isola")
    except NoSuchElementException:
        print("visuale isola non disponibile")

    time.sleep(4)

    
    for n_city in range(0, numero_citta):
        print(get_nome_citta(br))
        
        start = time.time()

        search = br.find_elements_by_xpath("//*[@data-same_island='true']")
        print(len(search))
        i = 0
        for sc in search:

            print("agisco sul villaggio " + str(i + 1))

            time.sleep(rand_time()+1)

            search = br.find_elements_by_xpath("//*[@data-same_island='true']") #.owned


            a = -1
            for sc in search:
                a += 1
                if(a == i):
                    try:
                        sc.click()
                    except:
                        print("impossibile aprire pannello villagio")

                    time.sleep(rand_time())


                    try:
                        ele = br.find_element_by_css_selector(".card_click_area")
                        ele.click()
                    except:
                        print("impossibile raccogliere risorse")


                    time.sleep(rand_time())


                    try:
                        ele = br.find_element_by_css_selector(".buttons_container .close")
                        ele.click()
                    except:
                        print("impossibile chiudere")





            i += 1
            time.sleep(rand_time())
 
        # prox citta
        
        next_town(br)
        
 
    end = time.time()
    print("tempo impiegato: " + str(int(end - start)))

    tempo_attesa = TEMPO - int(end - start)
    if(tempo_attesa < 5):
        tempo_attesa = 5

    tempo_r = rand_time()*3.14+rand_time()*7/5 +rand_time()*11/7

    print("prossimo giro tra: " + str(tempo_attesa) + " + " + str(tempo_r) + " secondi")
    
    for i in range(0, int(tempo_attesa + tempo_r)):
        print(int(tempo_attesa + tempo_r - i))
        time.sleep(1)
    

