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


# initial_horse_data = bs(requests.get("https://racingaustralia.horse/InteractiveForm/HorseAllForm.aspx?HorseCode=NzQ0MzI4NDk0MA%3d%3d&src=horsesearch",headers=headers).content, "html.parser")

# links = initial_horse_data.select("a[href*=Meeting]")
# link_df = pd.DataFrame(columns=['venue', 'date', 'link'])

# for link in links:
#     print(link.text.rsplit(",",1))
#     print(link["href"])
#     link_df.loc[len(link_df)] = link.text.rsplit(" ",1)+[link['href']]

##Scrape a horse at a time and record the race-days it has been to 
#check these against exhisting racedays
#add horses race stats into the dataframe
#once over a specific amount of races then concurrently scrape all the data
    #return horse name into dataframe if not in there
#when checking 
#df.loc[df.eq('Airbag').any(axis=1)]


headers = { 'Accept-Language' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

 
horse_name_db = pd.DataFrame(columns = ["horseName","birthDate","link"])
horse_name_db.loc[0] = ["MR BRIGHTSIDE (NZ)","17-Oct-2017","/InteractiveForm/HorseAllForm.aspx?HorseCode=Nzk1NzUyODk4NQ%3d%3d&src=horsesearch"]

raceday_db = pd.DataFrame(columns=["location", "date","trial","link"])


def get_horse_names(links):
    df_append_list = []
    global horse_name_db

    for link in links:
        t = time.time()
        raceday_request = bs(requests.get(f"https://racingaustralia.horse/{link}",headers=headers).content, "html.parser")#Meeting.aspx?meetcode=Nzc1ODI3ODc0MA%3d%3d#Race8
        print(time.time()-t)
        horses = raceday_request.select(".horse > .GreenLink")
        for horse in horses:
            print(horse)
            if len(horse_name_db['link'].to_numpy()[horse_name_db['link'].to_numpy() == horse["href"]]) == 0:
                horse_name_dict = {}
                horse_name_dict["horseName"] = horse.text.replace("\r","").replace("\t","").replace("\n","").rstrip()
                horse_name_dict["birthDate"] = ""
                horse_name_dict["link"] = horse["href"]
                df_append_list.append(horse_name_dict)
    horse_name_db = pd.concat([horse_name_db,pd.DataFrame(df_append_list,columns=["horseName","birthDate","link"])],ignore_index=True)


def get_horse_info(horse_link):
    horse_request = bs(requests.get(f"https://racingaustralia.horse/{horse_link}",headers=headers).content, "html.parser")
    horses = horse_request.find_all("tr",{"class":["OddRow","EvenRow"]})
    pattern = r'([A-Z\s]+) (\d{2}[A-Za-z]{3}\d{2}) (\d+m) ([A-Za-z]+\d+) ([A-Za-z\d\s-]+) \$([\d,]+) \$([\d,]+) ([A-Za-z]+\s[A-Za-z]+) (\d+(\.\d+)?kg) Barrier (\d+)' #([A-Za-z]+\s[A-Za-z]+) Barrier (\d+)'
    
    for horse in horses:

        if (horse.find("b").text.split(" ")[0] == "MATA") or ():
            pass
        else:
            print(horse)
            position = horse.find("td").text.rstrip().split(" ")[0]
            info = horse.find_all("b")
            

            print(info[0].text)
            loc_date = re.match(r'([A-Z\s]+) (\d{2}[A-Za-z]{3}\d{2})',info[0].text)
            # print(loc_date)
            loc,date = loc_date.groups()[0],loc_date.groups()[1]

            # print(horse.next_sibling.split("(")[0].strip().replace("  ", " "))
            race_info = re.match(r'(\d+m) ([A-Za-z]+\d+) ([A-Za-z\d\s-]+) \$([\d,]+)',info[0].next_sibling.split("(")[0].strip().replace("  ", " "))
            # print(race_info)
            distance, track_rating, rclass, prizeMoney = race_info.groups()[0],race_info.groups()[1],race_info.groups()[2],race_info.groups()[3]

            #horse_info = re.match(r'(\d+m) ([A-Za-z]+\d+) ([A-Za-z\d\s-]+) \$([\d,]+)',info[0].find_all("b")[0].next_sibling.split("(")[0].strip().replace("  ", " "))

            jockey = horse.find_all("b")[0].next_sibling.next_sibling.text

            timing_info = info[-1].next_sibling.split(",")
            weight, race_time, time_600 = timing_info[0].strip().split(" ")[0].replace("kg",""), timing_info[0].strip().split(" ")[1], timing_info[0].strip().split(" ")[-1].replace(")","") 
            margin, time_800, time_400, flucs = timing_info[1].strip().replace("L",""),timing_info[2].strip().replace("th@800m",""),timing_info[3].strip().replace("th@400m",""),timing_info[4].replace("$","").split("/")

            #print(position,loc,date,distance, track_rating, rclass, prizeMoney,jockey,weight, race_time, time_600,margin, time_800, time_400, flucs)







get_horse_info("InteractiveForm/HorseAllForm.aspx?HorseCode=OTAxNzgyNTk4NQ%3d%3d&src=horsesearch")

    






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
