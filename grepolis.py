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
numero_citta = 10
citta_riferimento = ""
username = ""
password = ""


TEMPO = 10*60 # 5 minuti di tempo refrattario

OPZIONE_NUM = 0 # da 0 a 3 rispettivamente 5-20-180-480 min

##############
#INIZIO
##############

br = webdriver.Chrome()
"""
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=/home/fede3/.config/google-chrome/Default")
options.add_extension('/home/fede3/.config/google-chrome/Default/Extensions/dhdgffkkebhmkfjojejmpbldmpobfkfo/4.7_0/')

br = webdriver.Chrome(chrome_options=options)
"""


nomi_ita = ["senato", "caverna", "legno", "pietra", "argento", "mercato", "porto", "caserma", "muro", "magazzino", "fattoria", "accademia", "tempio", "terme", "torre"]
nomi = ["main", "hide", "lumber", "stoner", "ironer", "market", "docks", "barraks", "wall", "storage", "farm", "academy", "temple", "terme", "torre"]

matrix_buildings_real = [[0 for i in range(15)] for i in range(numero_citta)]
matrix_caserma_real = [[0 for i in range(10)] for i in range(numero_citta)]
matrix_porto_real = [[0 for i in range(10)] for i in range(numero_citta)]


matrix_buildings = [
	# corretta --> |
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#[17, 10, 16, 16, 16, 8, 12, 10, 20, 30, 25, 30, 15, 0, 0], # full off
	[16, 10, 16, 16, 16, 7, 11, 10, 20, 30, 0, 30, 15, 0, 0], # full def
	[0, 0, 0, 0, 0, 0, 15, 0, 20, 0, 0, 16, 0, 0, 0],#[17, 10, 25, 16, 16, 5, 20, 5, 20, 30, 45, 30, 15, 0, 0], #full ince
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0],
	#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#coda bloccata, risparmio energie
	
	#[15, 10, 15, 10, 10, 0, 10, 10, 0, 15, 20, 33, 10, 0, 0],#per arrivare alla coloniale piu infretta possibile
	#[17, 10, 15, 10, 10, 10, 10, 10, 0, 20, 30, 28, 15, 0, 0],#per arrivare alla conquista piu infretta possibile

	#[17, 10, 20, 20, 21, 10, 15, 10, 0, 25, 45, 30, 17, 0, 0],

	#[17, 10, 20, 20, 21, 10, 15, 10, 0, 25, 45, 30, 17, 0, 1],
	#[10, 10, 15, 10, 10, 5, 15, 5, 0, 16, 15, 30, 15, 0, 0],#cresci veloce
	
]

matrix_caserma = [
    [0, 800, 0, 0, 100, 0, 20, 0, 50, 0], # full off e manticore
    [1000, 0, 0, 120, 0, 0, 0, 0, 0, 0], #full def
    [0, 600, 0, 0, 200, 0, 20, 0, 0, 0], #full off
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #full birre
   # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # full ince
]

matrix_porto = [
    [0, 0, 70, 0, 50, 0, 0, 0, 0, 0], # full manticore
	[0, 60, 0, 0, 50, 0, 0, 0, 0, 0], #full def
	[0, 0, 70, 0, 50, 0, 0, 0, 0, 0],#full off
	[0, 99999, 0, 0, 0, 0, 0, 0, 0, 0], #full birre
	#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]





def rand_time():
    return (0.5 + randint(0, 15)/30)


def get_nome_citta(br):
	try:
		name = br.find_element_by_css_selector(".town_name").text
		return name
	except:
		login(br)


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
		login(br)



def allinea_citta(br):
	try: 
		print("allineo")
		#allinea citta
		while(True):
			if(get_nome_citta(br) == citta_riferimento):
				print("trovata")
				break
			else:
				next_town(br)
				print("...")
	except:
		print("impossibile allineare citta\nrifaccio login")
		login(br)

def missioni_iniziali(br):
	try:
		search = br.find_element_by_css_selector(".collect_reward")
		search.click()
		time.sleep(rand_time())
		search = br.find_element_by_css_selector(".gp_item_reward_all")
		search.click()
		time.sleep(rand_time())
		search = br.find_element_by_id("item_reward_stash")
		search.click()
		print("missione reward depositata")
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	except:
		print("visuale reward NON aperta")
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()	
		
		
	try:
		search = br.find_element_by_css_selector(".attack_spot")
		search.click()
		print("visuale missione possibile aperta")
		time.sleep(rand_time())
		search = br.find_element_by_css_selector(".select_all")
		search.click()
		time.sleep(rand_time())
		search = br.find_element_by_css_selector(".btn_attack")
		search.click()
		
		
		time.sleep(rand_time())
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	except:
		print("visuale missione possibile NON aperta")
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()



def login(br):
	try:
		br.get("https://it.grepolis.com/")
		time.sleep(3)

		search = br.find_element_by_name('login[userid]')
		search.send_keys(username)
		search = br.find_element_by_name('login[password]')
		search.send_keys(password)
		search = br.find_element_by_name("login[Login]")
		search.send_keys(Keys.RETURN)
		time.sleep(3)
	except:
		print("login già fatto, entro nel mondo")
		
	try:
		search = br.find_elements_by_css_selector(".world_name div")
		a = 0
		for i in search:
			if(a == 0):#NUMERO DEL MONDO CHE COMPARE IN ORDINE NELLA SCHERMATA DOPO LOGIN
				i.click()
			a += 1
		print("Avvio Gioco")
	except:
		print("errore scelta del mondo")
		
	time.sleep(3)
	
	
def bonus_giornaliero(br):
	try:
		search = br.find_element_by_css_selector(".js-tooltip-resources div")
		search.click()
		time.sleep(2)
	except:
		print("Nessun bonus giornaliero")



def recluta_porto(br, n_city):
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
			
	try:
		br.execute_script("BuildingWindowFactory.open('docks');")
		#units = br.find_elements_by_id("units div")
		time.sleep(2)

		units = br.find_elements_by_css_selector(".unit_order_tab .unit_order_total")
		i = 0
		for unit in units:
			if(unit.text ==""): 
				matrix_porto_real[n_city][i] = 0
			else:
				matrix_porto_real[n_city][i] = int(unit.text)
			i += 1
	except:
		print("Errore nell'aprire la caserma")
		
	print(matrix_porto[n_city])
	print(matrix_porto_real[n_city])
	
	cnt = 0
	for n_soldato in matrix_porto_real[n_city]:
		try:
			div1  = br.find_element_by_id("unit_order")
			div2 = div1.find_element_by_id("units")
			nome_barca = div2.find_elements_by_xpath("./div")[cnt].get_attribute("id")
			
			if(n_soldato < matrix_porto[n_city][cnt]):
				print("Barca  "+ nome_barca +" sottosviluppato")
				
				comando1 = "UnitOrder.selectUnit('"+nome_barca+"'); return false;"
				comando_up = "UnitOrder.build(w("+nome_barca+"));"
				
				try:
					br.execute_script(comando1)
					time.sleep(rand_time()/5)
					br.execute_script(comando_up)
				except:
					print("Errore comando barca")
		except:
			print("Errore nel trovare alcuni parametri barca")
		cnt += 1

	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
					
	

def recluta_caserma(br, n_city):
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	try:
		br.execute_script("BuildingWindowFactory.open('barracks');")
		time.sleep(2)

		units = br.find_elements_by_css_selector(".unit_order_tab .unit_order_total")
		i = 0
		for unit in units:
			if(unit.text ==""): 
				matrix_caserma_real[n_city][i] = 0
			else:
				matrix_caserma_real[n_city][i] = int(unit.text)
			i += 1
	except:
		print("Errore nell'aprire la caserma")
		
	print(matrix_caserma[n_city])
	print(matrix_caserma_real[n_city])
	
	cnt = 0
	for n_soldato in matrix_caserma_real[n_city]:
		try:
			div1  = br.find_element_by_id("unit_order")
			div2 = div1.find_element_by_id("units")
			nome_soldato = div2.find_elements_by_xpath("./div")[cnt].get_attribute("id")
			#print(nome_soldato)
			
			if(n_soldato < matrix_caserma[n_city][cnt]):
				print("Soldato  "+ nome_soldato +" sottosviluppato")
				
				comando1 = "UnitOrder.selectUnit('"+nome_soldato+"'); return false;"
				comando_up = "UnitOrder.build(w("+nome_soldato+"));"
				
				try:
					br.execute_script(comando1)
					time.sleep(rand_time()/5)
					br.execute_script(comando_up)
				except:
					print("Errore comando soldato")
		except:
			print("Errore nel trovare alcuni parametri soldato")
		cnt += 1	
		
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
			
	
		
		
		
	



















#start it up
print("Avvio di chrome....")
print(rand_time())

login(br)
bonus_giornaliero(br)




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



	print("allineo")
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

		comando_fattoria_up_dato = False
		
		if(int(pop) <= 20):
			print("Attenzione la popolazione e bassa")
			try:
				br.execute_script("BuildingMain.buildBuilding('farm', 20);")
				print("Comando fattoria dato correttamente")
				comando_fattoria_up_dato = True
			except: 
				print("Errore comando fattoria pop bassa")
		else:
			comando_fattoria_up_dato = False

		time.sleep(2)
		
		recluta_porto(br, n_city)
		time.sleep(2)
		recluta_caserma(br, n_city)
		time.sleep(2)
		
		
		err_senato = False
		try:
			#senato = br.find_element_by_id("building_main_area_main")#xpath("//*[@id='building_main_area_main']")
			#senato.click()
			br.execute_script("BuildingWindowFactory.open('main');")
			print("visuale senato")
			err_senato = False
			time.sleep(1)
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


			print (matrix_buildings[n_city])
			print (matrix_buildings_real[n_city])

			for num_edificio in range(0, 13):
				#if(not(comando_fattoria_up_dato == True and num_edificio == 10)):
				if(matrix_buildings_real[n_city][num_edificio] < matrix_buildings[n_city][num_edificio]):
					print("Edificio "+ nomi_ita[num_edificio] +" sottosviluppato")
					comando_up = "BuildingMain.buildBuilding('"+nomi[num_edificio]+"', 50);"
					try:
						br.execute_script(comando_up)
					except:
						print("Errore comando up")
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

		time.sleep(2)
		
#		missioni_iniziali(br)
	#	missioni_isola(br)

		search = br.find_elements_by_xpath("//*[@data-same_island='true']")
		#print(len(search))
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
						ele = br.find_elements_by_css_selector(".card_click_area")
						n_opz=0
						for el in ele:
							if(n_opz == OPZIONE_NUM):	
								el.click()
							n_opz+=1
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

	tempo_attesa = TEMPO - (int(end - start))#*0.80
	if(tempo_attesa < 5):
		tempo_attesa = 5

	tempo_r = rand_time()*3.14+rand_time()*7/5 +rand_time()*19/7+20+13*rand_time()

	print("prossimo giro tra: " + str(tempo_attesa) + " + " + str(tempo_r) + " secondi")

	for i in range(0, int(tempo_attesa + tempo_r)):
		print(int(tempo_attesa + tempo_r - i))
		if(int(tempo_attesa + tempo_r - i) == 100 or int(tempo_attesa + tempo_r - i) == 10):
			sys.stdout.write("\033[K")
		else:
			sys.stdout.write("\033[F") # Cursor up one line

		time.sleep(1)
	print("-------------------------------------------------------------\n\n----------------------------------------------------------")
