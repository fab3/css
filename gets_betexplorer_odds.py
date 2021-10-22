##Testing Only , scraping some data !
# In order for this file to run one needs to install some dependecies along side Python, Selenium , BS4, and mysql 
#



class Odds:
    def __init__(self, url):
        self.url = url

    def open_url(self):
        ### will open using seleniun and then BS4
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920,1080")
        # options.add_argument("headless")
        options.add_argument(f"user-agent={self.headers_agent.random}")
        self.driver = webdriver.Chrome(
            options=options, executable_path="/home/f/Downloads/chromedriver"
        )
        print("connecting now ...\n")
        self.driver.get(url)

    def next_matches_prevDate(self):
        # clik on Next Matches link
        driver = self.driver
        driver.find_element_by_link_text("Next Matches").click()
        time.sleep(3)
        ### lets select calendar and click on it - ok
        driver.find_element_by_xpath('//*[@id="lcmenu"]/a[2]').click()
        time.sleep(randint(3, 9))
        prevDay = driver.find_element_by_xpath('//*[@id="lcmenu"]/a[1]/i').click()
        time.sleep(3)
     

    def soupCallBs4(self):
        time.sleep(randint(1, 3))
        self.html = self.driver.page_source
        self.soup = bs(self.html, "lxml")
        return self.soup

    def writeLocal(self):
        pass
        #### write the HTML page on LOCAL
        file = open("/home/f/Desktop/venv/betx.html", "w")
        file.write(self.html)
        file.close()
        print("Writing THE FILE ON LOCAL MACHINE")

    def readLocal(self):
        ### reads LOCAL PAGE
        localfile = open("/home/f/Desktop/venv/betx.html", "r")
        self.soup = bs(localfile, "lxml")
        print("READING FROM MY PC !!!\n")

    def getDate(self):
        ### link by link , game by gam, ge the odds
        date = self.soup.select("p#match-date")
        for todaydate in date:
            self.date = todaydate.text[:10]
            print(self.date)

    def getTeams(self):
        #### get teams name
        tnames = []
        tnames = self.soup.select("ul.list-details")
        for li in tnames:
            self.home = li.select("h2.list-details__item__title")[0].text
            self.away = li.select("h2.list-details__item__title")[1].text
            print(self.home)
            print(self.away)
            break

    def getOdds1x2(self):
        # getting average odds
        try:
            odds1x2 = self.soup.select("tfoot#match-add-to-selection")
            for odds in odds1x2:
                odds = odds.select("td.table-main__detail-odds")
                self.odds1 = odds[0].text  ###afirst DIV
                self.oddsx = odds[1].text  ### second DIV
                self.odds2 = odds[2].text  ###3rd DIV
        except:
            self.odds1 = None
            self.oddsx = None
            self.odds2 = None
            pass

    def getOverUnder(self):
        ### use seleniun again - gets another link
        try:
            self.driver.find_element_by_partial_link_text("O/U").click()
            self.soupCallBs4()
            # self.writeLocal()
            mainDiv = self.soup.select("table.table-main.h-mb15.sortable")
            ov = {}
            for total_ou in mainDiv:
                total_goals = total_ou.select_one("td.table-main__doubleparameter").text
                tfoot = total_ou.select("tfoot#match-add-to-selection")
                for ou in tfoot:
                    over_odds0 = ou.select("td.table-main__detail-odds")[0].text
                    under_odds1 = ou.select("td.table-main__detail-odds")[1].text
                    ov.update({total_goals: (over_odds0, under_odds1)})

            outList = [
                "0.5",
                "1",
                "1.5",
                "1.75",
                "2",
                "3",
                "4",
                "4.5",
                "5",
                "5.5",
                "6",
                "6.5",
                "7",
                "7.5",
            ]
            for k, v in ov.items():
                if k in outList:
                    continue
                elif k == "2.5":
                    self.ov25 = v[0]
                    self.un25 = v[1]
                elif k == "3.5":
                    self.ov35 = v[0]
                    self.un35 = v[1]
                else:
                    continue

        except:
            self.ov25 = None
            self.un25 = None
            self.ov35 = None
            self.un35 = None
            self.ov35 = None
            self.un35 = None

            pass

    def getAsian(self):
        ##modify curert URL to get directly the new URL
        self.driver.find_element_by_partial_link_text("AH").click()
        self.soupCallBs4()
        #
        #
        mainDiv = self.soup.select("table.table-main.h-mb15.sortable")
        ah = {}
        for total_ou in mainDiv:
            total_goals = total_ou.select_one("td.table-main__doubleparameter").text
            tfoot = total_ou.select("tfoot#match-add-to-selection")
            for ou in tfoot:
                ah0 = ou.select("td.table-main__detail-odds")[0].text
                ah1 = ou.select("td.table-main__detail-odds")[1].text
                ah.update({total_goals: (ah0, ah1)})
        # print(ah)
        ahList = ["0"]
        for k, v in ah.items():
            if k in ahList:
                if k == "0":
                    self.ah_m0_1 = v[0]
                    self.ah_m0_2 = v[1]
                else:
                    None

    def getBts(self):
        try:
            self.driver.find_element_by_partial_link_text("BTS").click()
            self.soupCallBs4()
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

        except:
            self.bts_yes = None
            self.bts_no = None
            pass

    def close_pages(self):
        self.driver.close()
        self.driver.quit()

    def connection_to_mysql(self):
        config = {
            "host": "localhost",
            "user": "root",
            "password": "inhere_yourpasswordxxx_",
            "database": "inhere_your_DBxxxname",
        }
        self.conn = mysql.connector.connect(**config)
        self.cur = self.conn.cursor()

    def inserting_odds_into_db(self):
        # 30 in toal
        val = (
            self.date,
            self.home,
            self.away,
            self.odds1,
            self.oddsx,
            self.odds2,
            self.ov25,
            self.un25,
            self.ov35,
            self.un35,
            self.bts_yes,
            self.bts_no,
        )

        self.cur.execute(
            "INSERT IGNORE INTO odds(date, home, away, odds1, oddsx, odds2,  ov25, un25, ov35, un35,  bts_yes, bts_no) VALUE (  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            val,
        )
        self.conn.commit()
        self.cur.execute("SELECT * FROM odds ORDER BY id DESC LIMIT 1")
        print(self.cur.lastrowid, " -> last ID inserted <- ")

    def readingUrl_FromFile(self):
        url_final = []
        with open("/home/f/14oct.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("/https:", "/ https:").split()
                # line.replace("www.betexplorer.com/", "www.betexplorer.com")
                for x in line:
                    idx = x.rfind("-")
                    # print(x[idx]) ## this isour char e needs to be removed
                    first = x[:idx]
                    last = x[idx:]
                    res = first + "/" + x[idx + 1 :]
                    line = res.split()
                    ##removing bad data from urls / Cleaning URLS
                    urls_final = list(dict.fromkeys(line))
                    urls_final = list(filter(None, urls_final))
                    url_final.extend(urls_final)  ###this line after cleaning

        for i in range(0, len(url_final)):
            url = url_final[i]
            self.driver.get(url)
            self.soupCallBs4()
            time.sleep(randint(2, 3))
            self.getDate()
            time.sleep(randint(1, 3))
            self.getTeams()
            time.sleep(randint(1, 4))
            self.getOdds1x2()
            time.sleep(randint(2, 5))
            self.getOverUnder()
            time.sleep(randint(3, 6))
            self.getBts()
            time.sleep(randint(2, 4))
            self.connection_to_mysql()
            self.inserting_odds_into_db()


url = "https://www.betexplorer.com/soccer/"


i = Odds("url")
i.headers()
i.open_url()
i.soupCallBs4()
# i.readLocal()
i.next_matches_prevDate()
i.readingUrl_FromFile()
