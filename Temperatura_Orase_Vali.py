import requests
from datetime import datetime, timedelta
import folium
import time
import json
#VARIABILE TEMPERATURA
#La geo_url dupa name se pune {oras} sau alt termen concomitent cu imputul "input" catre API
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name=&count=1&language=ro&format=json"
geo_response = requests.get(geo_url)
geo_data = geo_response.json()
lista_opriri = []
def get_coord(oras):
    url = "https://nominatim.openstreetmap.org/search"
    params={
    "q":oras,
    "format":"json",
    "limit":12}
    r=requests.get(url,params=params,headers={"User-Agent":"MyApp"})
    data=r.json()
    return float(data[0]["lat"]),float(data[0]["lon"])
oras_start = input("Din ce oras vrei sa pleci ? : ")
opriri_suma = int(input("Cate opriri doresti sa faci pana la destinatie?:"))
for i in range(opriri_suma):
    oprire = input(f"Unde vrei sa te opresti? {i+1}:")
    lista_opriri.append(oprire)
if opriri_suma > 0:
    
    lat_opr, lon_opr = get_coord(oprire)
    geo_url_opr = f"https://geocoding-api.open-meteo.com/v1/search?name={oprire}&count=1&language=ro&format=json"
    geo_response_opr = requests.get(geo_url_opr)
    geo_data_opr = geo_response_opr.json()
    if "results" in geo_data_opr:
        lat = geo_data_opr["results"][0]["latitude"]
        lon = geo_data_opr["results"][0]["longitude"]
        nume_oras = geo_data_opr["results"][0]["name"]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        temperatura_opr = weather_data ["current_weather"]["temperature"]
        vant = weather_data["current_weather"]["windspeed"]
        print(f"\nOras destinatie: {nume_oras}")
        print(f"Temperatura:{temperatura_opr} C")
        print(f"Vant : {vant} km/h")


oras_end = input("In ce oras vrei sa ajungi ? : ")
lat_start, lon_start = get_coord(oras_start)
lat_end, lon_end = get_coord(oras_end)
geo_url_start = f"https://geocoding-api.open-meteo.com/v1/search?name={oras_start}&count=1&language=ro&format=json"
geo_url_end = f"https://geocoding-api.open-meteo.com/v1/search?name={oras_end}&count=1&language=ro&format=json"
geo_response_start = requests.get(geo_url_start)
geo_response_end = requests.get(geo_url_end)
geo_data_start = geo_response_start.json()
geo_data_end = geo_response_end.json()

#Functie temperatura in oras start, oprire, destinatie 
def temperatura_oras():
    #functia pentru afisare temperatura al primului oras
    if "results" in geo_data_start:
        lat = geo_data_start["results"][0]["latitude"]
        lon = geo_data_start["results"][0]["longitude"]
        nume_oras = geo_data_start["results"][0]["name"]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        temperatura_start = weather_data ["current_weather"]["temperature"]
        vant = weather_data["current_weather"]["windspeed"]
        print(f"\nOras destinatie: {nume_oras}")
        print(f"Temperatura:{temperatura_start} C")
        print(f"Vant : {vant} km/h")
                                       
    #functia pentru afisare temperatura destinatie
    if "results" in geo_data_end:
        lat = geo_data_end["results"][0]["latitude"]
        lon = geo_data_end["results"][0]["longitude"]
        nume_oras = geo_data_end["results"][0]["name"]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        temperatura_end = weather_data ["current_weather"]["temperature"]
        vant = weather_data["current_weather"]["windspeed"]
        print(f"\nOras destinatie: {nume_oras}")
        print(f"Temperatura:{temperatura_end} C")
        print(f"Vant : {vant} km/h")

    m=folium.Map(location=[lat_start,lon_start],zoom_start=13)
    folium.Marker(
        location=[lat_start,lon_start],
        popup=f"Locatie inceput:{oras_start}",
        tooltip=f"Punct de plecare: Temperatura plecare {temperatura_start} \n Coordonatele pentru {oras_start}:{lat_start},{lon_start}").add_to(m)
    if opriri_suma>0:
        folium.Marker(
        location = [lat_opr,lon_opr],
        popup=f"Oprire:{oprire}",
        tooltip=f"Punct oprire: Temperatura: {temperatura_opr} \n Coordonate pentru {oprire}:{lat_opr},{lon_opr}",
        icon = folium.Icon(color="red")).add_to(m)
    
    folium.Marker(
        location = [lat_end,lon_end],
        popup=f"Destinatie:{oras_end}",
        tooltip=f"Punct Sosire:Temperatura sosire: {temperatura_end}\n Coordonatele pentru {oras_end}:{lat_end},{lon_end} ",
        icon=folium.Icon(color="red")).add_to(m)
    if opriri_suma >0:
        folium.PolyLine(
        locations=[(lat_start,lon_start),(lat_opr,lon_opr),(lat_end,lon_end)],
        weight=5,
        opacity=0.7).add_to(m)
    
    folium.PolyLine(
        locations=[(lat_start,lon_start),(lat_end,lon_end)],
        weight=5,
        opacity=0.7).add_to(m)
    m.save("Harta_orase_noi.html")
    print("Harta a fost generata: Harta_orase.html")
        
        #Functia cu traseul Georgrafic
temperatura_oras()    
print(f"Coordonatele pentru {oras_start}:{lat_start},{lon_start}")
if opriri_suma>0:
    print(f"Coordonatele pentru {oprire}:{lat_opr},{lon_opr}")
print(f"Coordonatele pentru {oras_end}:{lat_end},{lon_end}")




   
        
        
        
        
        
        
        

        

