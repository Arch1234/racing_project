import requests
import pandas as pd 
from bs4 import BeautifulSoup as bs
import re
from concurrent.futures import ThreadPoolExecutor
import time
 

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


def get_race_data(links):
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

get_race_data(["InteractiveForm/Meeting.aspx?meetcode=Nzc1ODY5MzAxNg%3d%3d"])
get_race_data(["InteractiveForm/Meeting.aspx?meetcode=Nzc1ODY5MzAxNg%3d%3d"])
print(horse_name_db)







#raceday_request = bs(requests.get("https://racingaustralia.horse/InteractiveForm/Meeting.aspx?meetcode=Nzc1ODY5MzAxNg%3d%3d",headers=headers).content, "html.parser")
#horses = raceday_request.select(".horse")
#print(horses)












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
