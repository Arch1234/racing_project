import requests
import pandas as pd 
from bs4 import BeautifulSoup as bs
import re
 

#git status
#git add . 
#git commit -m "message"
#git push


headers = { 'Accept-Language' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}


initial_horse_data = bs(requests.get("https://racingaustralia.horse/InteractiveForm/HorseAllForm.aspx?HorseCode=NzQ0MzI4NDk0MA%3d%3d&src=horsesearch",headers=headers).content, "html.parser")

links = initial_horse_data.select("a[href*=Meeting]")
link_df = pd.DataFrame(columns=['venue', 'date', 'link'])

for link in links:
    print(link.text.rsplit(",",1))
    print(link["href"])
    link_df.loc[len(link_df)] = link.text.rsplit(" ",1)+[link['href']]

##Scrape a horse at a time and record the race-days it has been to 
#check these against exhisting racedays
#add horses race stats into the dataframe
#once over a specific amount of races then concurrently scrape all the data
    #return horse name into dataframe if not in there
#when checking 
#df.loc[df.eq('Airbag').any(axis=1)]


horse_name_db = pd.DataFrame(columns = ["horseName","birthDate","link"])
horse_name_db.loc[0] = ["MR BRIGHTSIDE (NZ)","17-Oct-2017","/InteractiveForm/HorseAllForm.aspx?HorseCode=Nzk1NzUyODk4NQ%3d%3d&src=horsesearch"]
print(horse_name_db)