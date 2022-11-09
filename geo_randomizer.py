
import pandas
import gspread
import gspread_dataframe
import geopy.distance
import random

from google.colab import auth
auth.authenticate_user()
import pandas as pd
import re
import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

def distance(lat1,long1,lat2,long2):
  coords_1 = (lat1,long1)
  coords_2 = (lat2,long2)
  d=int(geopy.distance.geodesic(coords_1, coords_2).meters)
  # print(d)
  return d

def google_sheet_update(secret_file_loc,sheet_name,sheet_tab):
    sa=gspread.service_account(filename=secret_file_loc)
    sh=sa.open(sheet_name)
    wk=sh.worksheet(sheet_tab)
    return wk

sheetUrl = input("Enter the URL of the Source Sheet: ")

wb = gc.open_by_url(sheetUrl)
ws = wb.worksheet("Radius")
rows_sheet = ws.get_all_records()
# df = pd.DataFrame(rows_sheet)
# print(df)
# print(rows_sheet)
latitude,longitude=ws.acell("B3").value.split(",")
print(latitude)
print(longitude)
r=int(ws.acell("C3").value)
p=int(ws.acell("D3").value)
d=int(ws.acell("E3").value)

check=1
points_list=[]
degree_list=[]
while(check==1):
  degree = random.randint(-90,270)
  ra=random.randint(0,r)
  point=geopy.distance.distance(meters=ra).destination((latitude, longitude), bearing=degree)
  val=[round(point.latitude,d),round(point.longitude,d)]
  if val in points_list:
    pass
  else:
    points_list.append(val)
    degree_list.append(degree)
  if len(points_list)==p:
    check=0
print(points_list)
loop=3
for each_val in points_list:
  cell_val="A{}".format(loop)
  cell_data=str(each_val[0])+","+str(each_val[1])
  ws.update(cell_val,cell_data)
  loop+=1
print('done')