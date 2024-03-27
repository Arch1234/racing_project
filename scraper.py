import requests
import pandas as pd 
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
import time
import re
 

#git status
#git add . 
#git commit -m "message"
#git push


##Scrape a horse at a time and record the race-days it has been to 
#check these against exhisting racedays
#add horses race stats into the dataframe
#once over a specific amount of races then concurrently scrape all the data
    #return horse name into dataframe if not in there
#when checking 
#df.loc[df.eq('Airbag').any(axis=1)]


## Need to take trials into account


headers = { 'Accept-Language' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

 
horse_name_db = pd.DataFrame(columns = ["horseName","birthDate","link"])
horses_in_race_db = pd.DataFrame(columns=["location", "date","raceNumber","horsesNumber","link"])
horse_name_db.loc[0] = ["MR BRIGHTSIDE (NZ)","17-Oct-2017","/InteractiveForm/HorseAllForm.aspx?HorseCode=Nzk1NzUyODk4NQ%3d%3d&src=horsesearch"]

raceday_db = pd.DataFrame(columns=["location", "date","link"])


def get_horse_names_from_meetings(link,date):
    horse_name_append_list = []
    horses_in_race_append_list = []
    global horse_name_db
    global horses_in_race_db

    t = time.time()
    raceday_request = bs(requests.get(f"https://racingaustralia.horse/{link}",headers=headers).content, "html.parser")#Meeting.aspx?meetcode=Nzc1ODI3ODc0MA%3d%3d#Race8
    horses = raceday_request.select(".horse > .GreenLink")
    for horse in horses:
        if len(horse_name_db['link'].to_numpy()[horse_name_db['link'].to_numpy() == horse["href"].replace("HorseFullForm","HorseAllForm")]) == 0:
            horse_name_dict = {}
            horse_name_dict["horseName"] = horse.text.replace("\r","").replace("\t","").replace("\n","").rstrip()
            horse_name_dict["birthDate"] = ""
            horse_name_dict["link"] = horse["href"].replace("HorseFullForm","HorseAllForm")
            horse_name_append_list.append(horse_name_dict)
    
    races = raceday_request.find_all("table",{"cellpadding":"3"})
    print(races)
    rr = 1
    for race in races:
        horse_no = race.select('span[class*="Finish"]')
        print(horse_no)
        b = 0
        for a in horse_no:
            if a.text == "FF":
                pass
            elif (int(a.text) > b):
                b = int(a.text)
        horse_name = {}
        horse_name["location"] = raceday_request.find("h2").text.split(":")[0]
        horse_name["date"] = date
        horse_name["raceNumber"] = rr
        horse_name["horsesNumber"] = b
        horse_name["link"] = link
        horses_in_race_append_list.append(horse_name)
        rr += 1

    horse_name_db = pd.concat([horse_name_db,pd.DataFrame(horse_name_append_list,columns=["horseName","birthDate","link"])],ignore_index=True)
    horses_in_race_db = pd.concat([horses_in_race_db,pd.DataFrame(horses_in_race_append_list,columns=["location", "date","raceNumber","horsesNumber","link"])],ignore_index=True)




get_horse_names_from_meetings("InteractiveForm/Meeting.aspx?meetcode=MTIxNjc5MzA0MDM%3d#Race1","dd")


def get_horse_race_info(horse_link):
    horse_request = bs(requests.get(f"https://racingaustralia.horse/{horse_link}",headers=headers).content, "html.parser")
    horses = horse_request.find_all("tr",{"class":["OddRow","EvenRow"]})

    horse_name = horse_request.find("h2").text.strip()
    horse_brithday = horse_request.find("h2").next_sibling.next_sibling.next_sibling.text.split(":")[1].strip()

    raceday_append_list = []

    for horse in horses:
        if str(re.match(r'([A-Z\s]+)',horse.find_all("b")[0].text).group()).strip() in ["MATA","ALSP", "T CK"]:
            pass
        else:
            position = horse.find("td").text.rstrip().split(" ")[0]
            if position == "T":
                continue
            info = horse.find_all("b")
            
            loc_date = re.match(r'([A-Z\s]+) (\d{2}[A-Za-z]{3}\d{2})',info[0].text)
            loc,date = loc_date.groups()[0],loc_date.groups()[1]
            
            race_info = re.match(r'(\d+m) ([A-Za-z]+\d+) ([A-Za-z\d\s-]+) \$([\d,]+)',info[0].next_sibling.split("(")[0].strip().replace("  ", " ").replace("&",""))
           
            distance, track_rating, rclass, prizeMoney = race_info.groups()[0],race_info.groups()[1],race_info.groups()[2],race_info.groups()[3]

            jockey = horse.find_all("b")[0].next_sibling.next_sibling.text

            timing_info = info[-1].next_sibling.split(",")
            weight, race_time, time_600 = timing_info[0].strip().split(" ")[0].replace("kg",""), timing_info[0].strip().split(" ")[1], timing_info[0].strip().split(" ")[-1].replace(")","") 
            margin, time_800, time_400, flucs = timing_info[1].strip().replace("L",""),timing_info[2].strip().replace("th@800m",""),timing_info[3].strip().replace("th@400m",""),timing_info[4].replace("$","").split("/")

            print([horse_name, date,loc,position,distance, track_rating, rclass, prizeMoney,jockey,weight, race_time, time_600,margin, time_800, time_400, flucs])
            print([loc,date, info[0].find("a")["href"]])

            raceday_append_list.append([loc,date, info[0].find("a")["href"]])






get_horse_race_info("InteractiveForm/HorseAllForm.aspx?HorseCode=MTI1MjM5NjgzMzM%3d&src=horseform&raceEntry=MzM2NTE1MTMyNjE%3d")

    






# while True:
    
#     with ThreadPoolExecutor() as executor:
#         a = executor.map(get_raceday_data, location_ids) ##input of [date,location,horsename,meetingId] and output of [date, location, horse_name, position, price]
   
#     p = 0
#     for i in a:
#         if str(i) == "None":
#             pass
#         else:
            
#             race_tips.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6]])
#             print([i[0],i[1],i[2],i[3],i[4],i[5],i[6]])
#         p = p+1
#     print(len(race_tips))
