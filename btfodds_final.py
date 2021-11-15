import mysql.connector
import time
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import requests
from random import randint
from time import sleep
import fake_useragent
import datetime


class Odds:
    def __init__(self, url):
        self.url = url

    def headers(self):
        # USE random USER AGENT 
        self.headers_agent = UserAgent()

    def open_url(self):
        ### will open using seleniun and then BS4
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920,1080")
        # options.add_argument("headless")
        options.add_argument(f"user-agent={self.headers_agent.random}")
        # driver = webdriver.Chrome("/home/f/Downloads/chromedriver", options=options)
        self.driver = webdriver.Chrome(
            options=options, executable_path="/home/f/Downloads/chromedriver"
        )
        print("connecting now ...\n")
        self.driver.get(url)
      
   
    #### using BS4
    def soupCallBs4(self):
        sleep(randint(1, 3))
        self.html = self.driver.page_source
        self.soup = bs(self.html, "lxml")

   

    def getDate(self):

        date = self.soup.select_one("span#startDate").text
        ##using sele for click on dates
        date = self.driver.find_element_by_xpath(
            '//*[@id="datepicker"]/span[2]'
        ).click()

        # calendar opener
        tr_main = self.driver.find_elements_by_tag_name("table.table-condensed")

        for i in range(0, len(tr_main)):
            ### MOnth to start #prev click starting point
            previous = self.driver.find_element_by_class_name("prev")
            sleep(randint(2, 3))
            ActionChains(self.driver).click(previous).perform()
            sleep(randint(2, 4))
            ActionChains(self.driver).click(previous).perform()
            sleep(randint(2, 4))
            ActionChains(self.driver).click(previous).perform()  ###from25iuly /all AUG
            sleep(randint(2, 4))
            ActionChains(self.driver).click(previous).perform()
            sleep(randint(2, 4))
            ActionChains(self.driver).click(previous).perform()
            sleep(randint(2, 4))

            days = self.driver.find_elements_by_class_name("day")
            # print(len(days))
            for day in range(3, 47):
                print("we click on DAY = ", days[day].text)
                # time.sleep(7)
                if days[day]:
                    days[day].click()
                    # ActionChains(self.driver).click(python_botton).perform()
                    self.soupCallBs4()  #### THIS IS IMPORTANT ##to be here !!!!
                    date = self.soup.select_one("span#startDate").text
                    self.date = date.replace("-", ".")
                    self.date = datetime.datetime.strptime(
                        self.date, "%Y.%m.%d"
                    ).strftime("%d.%m.%Y")
                    print("select my Day : ", self.date)
                    self.get_all_links()
            print("FINNish")

    def get_all_links(self):
        all_games_url = []
        tr_all = self.soup.select("tr.mw")
        for a in tr_all:
            href = a.select_one("a")["href"]
            # print(href)
            res = "https://www.btfodds.com" + href
            all_games_url.append(res)
        print("total Urls TOday: ", len(all_games_url))
        ### stat open the url and we use bs4 for fo check
        ##reseet affter maxin rechead
        # reset = 0
        # if len(all_games_url):
        for idx, url in enumerate(all_games_url[:], start=1):
            self.driver.get(url)  ###open urls one by one
            print("GameID => ", idx)
            # print("AFTER RESET LEN_games_URLS => ", len(all_games_url))
            self.driver.current_url
            self.soupCallBs4()  #### BS4 START HERE !!!!!!!!!!
            ## get teams name
            self.teams_name = self.soup.select_one("h1").text
            self.teams_name = self.teams_name.strip()[9:].split("VS")
            self.hometeam, self.awayteam = self.teams_name
            self.hometeam = self.hometeam.strip()
            self.awayteam = self.awayteam.strip()
            print("HO : ", self.hometeam)
            print("AW : ", self.awayteam)
            try:
                ## get the last elem from list
                average_odds = self.soup.select("tr.mw.static")[-1]
            except IndexError:
                continue
            final_odds = {}
            all_elem = ["1", "X", "2", "u250", "o250", "bts1", "bts2"]
            for odds in average_odds:
                try:
                    our_attr = odds.select_one("a")["href"]
                    our_attr_text = odds.select_one("a").text
                    elem = our_attr.split(",")[-1]
                    final_odds.update({elem: our_attr_text})
                except TypeError as err:
                    continue
            ### remove dnb1 and dnb2 adn /bookmaker/average
            elem = "dnb1"
            elem1 = "/bookmaker/average"
            if elem in final_odds and elem1 in final_odds:
                # if final_odds["dnb1"]:
                del final_odds["dnb1"]
                del final_odds["dnb2"]
                del final_odds["/bookmaker/average"]
            else:
                continue
                
            ### 0 elem inside for perfection
            res = list(filter(lambda k: k in final_odds.keys(), final_odds))
            res1 = list(filter(lambda k: k not in final_odds, all_elem))
  
            if len(res1) == 0:
                pass
            elif "1" in res1:
                pass
            elif "u250" in res1 and "bts1" in res1:
                final_odds.update({"u250": None})
                final_odds.update({"o250": None})
                final_odds.update({"bts1": None})
                final_odds.update({"bts2": None})
            else:
                final_odds.update({"bts1": None})
                final_odds.update({"bts2": None})
          
            if "/bookmaker/average" in final_odds:
                del final_odds["/bookmaker/average"]
            # print("final_odds BEFIRE  INSERT into DB: ", final_odds)
            for k, v in final_odds.items():
                if k == "1":
                    self.odds_1 = v
                    # print(self.odds_1)
                elif k == "X":
                    self.odds_x = v
                    # print(self.odds_x)
                elif k == "2":
                    self.odds_2 = v
                elif k == "u250":
                    self.under25 = v
                elif k == "o250":
                    self.over25 = v                  
                elif k == "bts1":
                    self.bts_yes = v
                elif k == "bts2":
                    self.bts_no = v
                    #### send DATA to mysql_DB
                    self.connection_to_mysql()
                    self.insert_odds_into()
                   
     
     
        self.driver.get(url)

        mainDiv = self.soup.select("table.table-main.h-mb15.sortable")
        ov = {}
        for total_ou in mainDiv:
            total_goals = total_ou.select_one("td.table-main__doubleparameter").text
            tfoot = total_ou.select("tfoot#match-add-to-selection")
            for ou in tfoot:
                over_odds0 = ou.select("td.table-main__detail-odds")[0].text
                under_odds1 = ou.select("td.table-main__detail-odds")[1].text
                ov.update({total_goals: (over_odds0, under_odds1)})
        print(ov)

        outList = ["0.5", "1", "1.75", "4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5"]
        for k, v in ov.items():
            if k in outList:
                continue
            elif k == "1.5":
                ov15 = v[0]
                un15 = v[1]           
            elif k == "2":
                ov2 = v[0]
                un2 = v[1]
            elif k == "2.25":
                ov225 = v[0]
                un225 = v[1]
            elif k == "2.5":
                ov25 = v[0]
                un25 = v[1]            
            elif k == "2.75":
                ov275 = v[0]
                un275 = v[1]             
            elif k == "3":
                ov3 = v[0]
                un3 = v[1]            
            elif k == "3.5":
                ov35 = v[0]
                un35 = v[1]              
            else:
                continue

        mainDiv = self.soup.select("table.table-main.h-mb15.sortable")
        ah = {}
        print(mainDiv)
        for total_ou in mainDiv:
            total_goals = total_ou.select_one("td.table-main__doubleparameter").text
            tfoot = total_ou.select("tfoot#match-add-to-selection")
        for ou in tfoot:
            ah0 = ou.select("td.table-main__detail-odds")[0].text
            ah1 = ou.select("td.table-main__detail-odds")[1].text
            ah.update({total_goals: (ah0, ah1)})
            print(ah)
            ahList = ["-1.5", "-1", "-2", "0"]
        for k, v in ah.items():
            if k in ahList:
                if k == "0":
                    ah0_1 = v[0]
                    ah0_2 = v[1]
                elif k == "-1":
                    ah_m1_1 = v[0]
                    ah_m1_2 = v[1]
                elif k == "-1.5":
                    ah_m15_1 = v[0]
                    ah_m15_2 = v[1]
                elif k == "-2":
                    ah_m2_1 = v[0]
                    ah_m2_2 = v[1]
                else:
                    continue

     
        newURL = self.driver.current_url + "#bts"
        self.driver.get(newURL)
        print("CURRENT URL ", self.driver.current_url)
        #
        mainDiv = self.soup.select("table.table-main.h-mb15.sortable")
        bts = {}
     
        for total_ou in mainDiv:
            tfoot = total_ou.select("tfoot#match-add-to-selection")
            for ou in tfoot:
                YES = ou.select("td.table-main__detail-odds")[0].text
                NO = ou.select("td.table-main__detail-odds")[1].text
                bts.update({"BTS": (YES, NO)})
   
        for k, v in bts.items():
            self.bts_yes = v[0]
            self.bts_no = v[1]
            print(type(self.bts_yes), self.bts_no)

    def connection_to_mysql(self):
        config = {
            "host": "localhost",
            "user": "root",
            "password": "db_passwordxxx",
            "database": "db_namexxx",
        }
        self.conn = mysql.connector.connect(**config)
        self.cur = self.conn.cursor()

    def insert_odds_into(self):

        val = (
            self.date,
            self.hometeam,
            self.awayteam,
            self.odds_1,
            self.odds_x,
            self.odds_2,
            self.over25,
            self.under25,
            self.bts_yes,
            self.bts_no,
        )

        self.cur.execute(
            "INSERT INTO yourTABLE_namexxx (date, hometeam, awayteam, odds_1, odds_x, odds_2, over25, under25, bts_yes, bts_no) VALUE ( %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)",
            val,
        )
        self.conn.commit()
        self.cur.execute("SELECT * FROM yourTABLE_namexxx  ORDER BY id DESC LIMIT 1")
        print(self.cur.lastrowid, " -> last ID inserted <- ")

    def close_driver(self):
        return self.driver.close()


url = "https://www.btfodds.com/soccer/football-odds/historical-odds,,league"


i = Odds("url")
i.headers()
i.open_url()
i.soupCallBs4()
i.getDate()
