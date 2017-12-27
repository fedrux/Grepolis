from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sys
from random import randint
from selenium.webdriver.chrome.options import Options


###############
#MODIFICA QUESTI PARAMETRI
###############
numero_citta = 20
citta_riferimento = ""
username = ""
password = ""




##############
#INIZIO
##############


nomi_ita = ["senato", "caverna", "legno", "pietra", "argento", "mercato", "porto", "caserma", "muro", "magazzino", "fattoria", "accademia", "tempio", "terme", "torre"]
nomi = ["main", "hide", "lumber", "stoner", "ironer", "market", "docks", "barraks", "wall", "storage", "farm", "academy", "temple", "terme", "torre"]

matrix_buildings_real = [[0 for i in xrange(15)] for i in xrange(numero_citta)]


matrix_buildings = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#coda bloccata, risparmio energie
	#[21, 10, 15, 10, 10, 0, 10, 10, 0, 15, 20, 33, 10, 0, 0],#per arrivare alla coloniale piu infretta possibile
	#[20, 10, 15, 10, 10, 10, 10, 10, 0, 20, 30, 28, 10, 0, 0],#per arrivare alla conquista piu infretta possibile
	[21, 10, 15, 10, 10, 0, 10, 10, 0, 15, 20, 14, 10, 0, 0],#per arrivare alla coloniale piu infretta possibile

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

err_senato = False



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
	except:
		print("impossibile cambiare citta")



def allinea_citta(br):
	print("allineoooo")
	#allinea citta
	while(True):
		if(get_nome_citta(br) == citta_riferimento):
			print("trovata")
			break
		else:
			next_town(br)
			print("...")



#options = webdriver.ChromeOptions() 
#options.add_argument("user-data-dir=/home/kinder/.config/google-chrome") #Path to your chrome profile
#br = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options)
br = webdriver.Chrome()

#


TEMPO = 600 # 5 minuti di tempo refrattario

#start it up
print("Avvio di chrome....")
print(rand_time())


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
	if(a == 2):#NUMERO DEL MONDO CHE COMPARE IN ORDINE NELLA SCHERMATA DOPO LOGIN
		i.click()
	a += 1


print("Avvio Gioco")

time.sleep(3)


try:
	search = br.find_element_by_css_selector(".js-tooltip-resources div")
	search.click()
	time.sleep(5)
except:
	print("Nessun bonus giornaliero")




while(True):

	try:
		search = br.find_elements_by_css_selector(".world_name div")
		a = 0
		for i in search:
			if(a == 2):
				i.click()
				print("Avvio Gioco")
				time.sleep(10)
			a += 1
	except:
		print("gia all'interno del gioco")



	print("allineoooo")
	#allinea citta
	while(True):
		if(get_nome_citta(br) == citta_riferimento):
			print("trovata")
			break
		else:
			next_town(br)
			print("...")

	start = time.time()
	for n_city in range(0, numero_citta):
		time.sleep(2)
		print(get_nome_citta(br))

		try:
			search = br.find_element_by_css_selector(".city_overview div")
			search.click()
			print("visuale citta")
			time.sleep(2)
		except:
			print("visuale citta non disponibile")


		try:
			legno = br.find_element_by_css_selector(".ui_resources_bar .wood .amount").text
			pietra = br.find_element_by_css_selector(".ui_resources_bar .stone .amount").text
			argento = br.find_element_by_css_selector(".ui_resources_bar .iron .amount").text
			pop = br.find_element_by_css_selector(".ui_resources_bar .population .amount").text
			print("parametri citta: " + legno + " "  + pietra + " "  + argento + " "  + pop + " " )
		except:
			print("impossibile recuperare parametri citta")


		try:
			gratis = br.find_element_by_css_selector(".btn_time_reduction")
			if(gratis.text == "gratis"):
				gratis.click()
				print("coda velocizzata")
				time.sleep(2)
			else:
				print("impossibile velocizzare coda")
		except:
			print("errore nel velocizzare coda")


		if(int(pop) <= 20):
			print("Attenzione la popolazione e bassa")
			br.execute_script("BuildingMain.buildBuilding('farm', 20);")

		time.sleep(2)
		try:
			senato = br.find_element_by_xpath("//*[@id='building_main_area_main']")
			senato.click()
			print("visuale senato")
			err_senato = False
			time.sleep(2)
		except:
			print("visuale senato non disponibile")
			err_senato = True


		if(err_senato==False):
			edifici = br.find_elements_by_css_selector(".white")
			print("edifici ")
			#print edifici

			cnt_ed = 0
			for ed in edifici:
				matrix_buildings_real[n_city][cnt_ed] = int(ed.text)
				cnt_ed += 1


			print matrix_buildings[n_city]
			print matrix_buildings_real[n_city]

			for num_edificio in range(0, 13):
				if(matrix_buildings_real[n_city][num_edificio] < matrix_buildings[0][num_edificio]):
					print("Edificio "+ nomi_ita[num_edificio] +" sottosviluppato")
					comando_up = "BuildingMain.buildBuilding('"+nomi[num_edificio]+"', 50);"
					br.execute_script(comando_up)
					#print("Sviluppo edificio "+ nomi[num_edificio] +" sottosviluppato")



		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()


		print("fine buildings up, wait 5s")
		time.sleep(5)

		try:
			search = br.find_element_by_css_selector(".island_view div")
			search.click()
			search = br.find_element_by_css_selector(".btn_jump_to_town div")
			search.click()
			print("visuale isola")
		except:
			print("visuale isola non disponibile")

		time.sleep(4)


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


					'''try:
						ele = br.find_element_by_css_selector(".buttons_container .close")
						ele.click()
					except:
						print("impossibile chiudere")
					'''
					webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()





			i += 1
			time.sleep(rand_time())

        # prox citta

		next_town(br)


	end = time.time()
	print("tempo impiegato: " + str(int(end - start)))

	tempo_attesa = TEMPO - (int(end - start))*0.80
	if(tempo_attesa < 5):
		tempo_attesa = 5

	tempo_r = rand_time()*3.14+rand_time()*7/5 +rand_time()*19/7+20

	print("prossimo giro tra: " + str(tempo_attesa) + " + " + str(tempo_r) + " secondi")

	for i in range(0, int(tempo_attesa + tempo_r)):
		print(int(tempo_attesa + tempo_r - i))
		if(int(tempo_attesa + tempo_r - i) == 100 or int(tempo_attesa + tempo_r - i) == 10):
			sys.stdout.write("\033[K")
		else:
			sys.stdout.write("\033[F") # Cursor up one line

		time.sleep(1)
	print("-------------------------------------------------------------\n\n----------------------------------------------------------")

