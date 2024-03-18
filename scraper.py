import requests
import pandas as pd 


# race_month_calendar = "https://graphql.rmdprod.racing.com/?query=query%20GetMeetingByMonth_CD(%24year%3A%20Int!%2C%20%24month%3A%20Int!)%20%7B%0A%20%20GetMeetingByMonth(year%3A%20%24year%2C%20month%3A%20%24month)%20%7B%0A%20%20%20%20id%0A%20%20%20%20venue%0A%20%20%20%20venueAbbr%0A%20%20%20%20venueCode%0A%20%20%20%20date%0A%20%20%20%20state%0A%20%20%20%20meetCode%3A%20id%0A%20%20%20%20meetUrl%0A%20%20%20%20clubCategory%0A%20%20%20%20meetQualityColor%0A%20%20%20%20status%0A%20%20%20%20isJumpOut%0A%20%20%20%20isTrial%0A%20%20%20%20isPicnic%0A%20%20%20%20dayNight%0A%20%20%20%20sortOrder%0A%20%20%20%20races%20%7B%0A%20%20%20%20%20%20raceNumber%0A%20%20%20%20%20%20time%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20status%0A%20%20%20%20%20%20distance%0A%20%20%20%20%20%20group%0A%20%20%20%20%20%20class%0A%20%20%20%20%20%20nameForm%0A%20%20%20%20%20%20videoItems%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20createdAt%0A%20%20%20%20%20%20%20%20videoId%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%20%20contenttype%0A%20%20%20%20%20%20%20%20poster%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D&operationName=GetMeetingByMonth_CD&variables=%7B%22year%22%3A2024%2C%22month%22%3A3%7D"
# for year in ["2018","2019","2020","2021","2022","2023","2024"]:
#     for month in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
#         url = f"https://graphql.rmdprod.racing.com/?query=query%20GetMeetingByMonth_CD(%24year%3A%20Int!%2C%20%24month%3A%20Int!)%20%7B%0A%20%20GetMeetingByMonth(year%3A%20%24year%2C%20month%3A%20%24month)%20%7B%0A%20%20%20%20id%0A%20%20%20%20venue%0A%20%20%20%20venueAbbr%0A%20%20%20%20venueCode%0A%20%20%20%20date%0A%20%20%20%20state%0A%20%20%20%20meetCode%3A%20id%0A%20%20%20%20meetUrl%0A%20%20%20%20clubCategory%0A%20%20%20%20meetQualityColor%0A%20%20%20%20status%0A%20%20%20%20isJumpOut%0A%20%20%20%20isTrial%0A%20%20%20%20isPicnic%0A%20%20%20%20dayNight%0A%20%20%20%20sortOrder%0A%20%20%20%20races%20%7B%0A%20%20%20%20%20%20raceNumber%0A%20%20%20%20%20%20time%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20status%0A%20%20%20%20%20%20distance%0A%20%20%20%20%20%20group%0A%20%20%20%20%20%20class%0A%20%20%20%20%20%20nameForm%0A%20%20%20%20%20%20videoItems%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20createdAt%0A%20%20%20%20%20%20%20%20videoId%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20url%0A%20%20%20%20%20%20%20%20contenttype%0A%20%20%20%20%20%20%20%20poster%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D&operationName=GetMeetingByMonth_CD&variables=%7B%22year%22%3A2024%2C%22month%22%3A3%7D"

#git status
#git add . 
#git commit -m "message"
#git push




import requests
print("Hello")
a = requests.get("https://racingaustralia.horse/InteractiveForm/HorseAllForm.aspx?HorseCode=NzQ0MzI4NDk0MA%3d%3d&src=horsesearch").text
print(a)