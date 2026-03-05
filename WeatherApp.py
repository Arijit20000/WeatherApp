import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dotenv import load_dotenv, find_dotenv
import os

current_theme = 'dark'

def toggle_theme():
    global current_theme 
    if current_theme == 'dark':
        apply_light_theme()
        current_theme = 'light'
    else: 
        apply_dark_theme()
        current_theme = 'dark'
    
def apply_dark_theme():
    window.config(bg = '#2A2A2A')
    main_frame.config(bg = '#2A2A2A')
    title_label.config(bg = '#2A2A2A', fg = "#FFFFFF") 
    subtitle_label.config(bg = '#2A2A2A', fg = "#FFFFFF")
    search_frame.config(bg = '#2A2A2A')
    result_frame.config(bg = '#2A2A2A')
    card_frame.config(bg = '#2A2A2A')

    for widget in result_frame.winfo_children(): 
        try: 
            widget.config(bg = '#2A2A2A', fg = '#FFFFFF')
        except:
            pass


def apply_light_theme():
    window.config(bg = "#F5F5F5")
    main_frame.config(bg = '#F5F5F5')
    title_label.config(bg = '#F5F5F5', fg = "#1E1E1E") 
    subtitle_label.config(bg = '#F5F5F5', fg = "#555555")
    search_frame.config(bg = '#F5F5F5')
    result_frame.config(bg = '#F5F5F5')
    card_frame.config(bg = '#F5F5F5')

    for widget in result_frame.winfo_children():
        try:
            widget.config(bg = '#F5F5F5', fg = '#1E1E1E')
        except: pass


def get_forecast(city):

    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'

    try: 
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return []
        
        forecast = []
        already_seen = set()

        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]

            if date not in already_seen:
                temp = item['main']['temp']
                condition = item['weather'][0]['description']
                forecast.append(f'{date} | temp = {round(temp)} | {condition}')
                already_seen.add(date)
            
            if len(forecast) == 5:
                break
        return forecast
        
    except: 
        return []
    
    
def show_forecast(data):     # this data is different from the 'data = response.json'.
        for widget in forecast_frame.winfo_children():
            if widget != forecast_title: 
                widget.destroy()

        for line in data:
            forecast_label = tk.Label(forecast_frame, text = line, bg = forecast_frame['bg'], fg = 'white', font=("Segoe UI", 9))
            forecast_label.pack(anchor = 'center')


def enter_pressed(event):
    get_weather()


def get_weather():
    city = city_entry.get()

    if not city:
        messagebox.showwarning('Input Error', 'Please Enter a City Name')
        return
    
    city_label.config(text = "⏳ Fetching weather...")
    temp_label.config(text = '')
    feels_like_label.config(text = '')
    condition_label.config(text = '')
    description_label.config(text = '')
    humidity_label.config(text = '')
    wind_speed_label.config(text = '')

    window.update()
    
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'  

    try:
        response = requests.get(url, timeout = 5)
        weather_data = response.json()

        if response.status_code != 200:
            messagebox.showerror('Error', 'City not Found!')
        else:
            city = weather_data['name']

            forecast = get_forecast(city)
            show_forecast(forecast)
            
            temp = weather_data['main']['temp']
            feelslike = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            icon_code = weather_data['weather'][0]['icon']
            is_night = icon_code.endswith('n')

            condition = weather_data['weather'][0]['main']
            if condition == 'Clear':
                if is_night:
                    weathericon_label.config(image = moon_icon)
                else:
                    weathericon_label.config(image = sun_icon)
            elif condition == 'Clouds':
                weathericon_label.config(image = cloud_icon)
            elif condition == 'Rain':
                weathericon_label.config(image = rain_icon)
            elif condition in ['Mist', 'Haze', 'Fog']:
                weathericon_label.config(image = mist_icon)
            else: weathericon_label.config(image = sun_icon)

            description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
              

        city_label.config(text = f'📍 {city}')
        temp_label.config(text = f'TEMP: {temp}°C')
        feels_like_label.config(text = f'FEELS LIKE: {feelslike}')
        condition_label.config(text = f'CONDITION: {condition}')
        description_label.config(text = description.capitalize())
        humidity_label.config(text = f'HUMIDITY: {humidity}%')
        wind_speed_label.config(text = f'Wind Speed💨: {wind_speed} m/s')


    except requests.exceptions.ConnectionError:
        messagebox.showerror('Network Error', 'No Internet Connection')

    except requests.exceptions.Timeout:
        messagebox.showerror('Timeout', 'Request Timed Out')

    except Exception as e:
        print('Something Went Wrong: ', e)
        messagebox.showerror('Exception', 'Something Went Wrong')

    
window = tk.Tk()
window.config(background = '#1E1E1E')
window.geometry('500x600')
window.title('Weather App')
sun_icon = tk.PhotoImage(file = 'Sun.png')
cloud_icon = tk.PhotoImage(file = 'Cloud.png')
rain_icon = tk.PhotoImage(file = 'Rain.png')
mist_icon = tk.PhotoImage(file = 'Mist.png')
moon_icon = tk.PhotoImage(file = 'Moon.png')


window.iconphoto(True, sun_icon)
style = ttk.Style()
style.theme_use('clam')
weathericon = tk.PhotoImage(file = 'Sunny.png')


main_frame = tk.Frame(window, bg = '#1E1E1E' ,padx = 20, pady = 20)
main_frame.pack(fill = 'both', expand = True) # both = width and height | "expand = true" stretch when windows resizes for responsiveness

title_label = tk.Label(main_frame, text = 'Weather App', font = ('Segoe UI', 20, 'bold'), bg = '#1E1E1E', fg = "#FFFFFF")
title_label.pack(pady = (0, 20))    # custom padding up 0 down 20 different from pady = 20

subtitle_label = tk.Label(main_frame, text = 'Real time Weather App at your Fingertips', font = ('Segoe UI', 10), fg = '#BBBBBB', bg = '#1E1E1E')
subtitle_label.pack(pady = (0, 25))

theme_button = tk.Button(main_frame, text = "☀ / 🌙" ,command = toggle_theme, bg = '#444444', fg = "#C4BEBE", relief = 'flat', padx = 18, cursor = 'hand2', pady = 5)
theme_button.pack(anchor = 'e', pady=(0, 10))

search_frame = tk.Frame(main_frame, bg = '#1E1E1E')
search_frame.pack(pady = (0, 25), fill = 'x')

card_frame = tk.Frame(main_frame, bg = '#2A2A2A', bd = 0, highlightthickness = 0)
card_frame.pack(fill = 'x', pady = (10, 20))

result_frame = tk.Frame(card_frame, bg = '#2A2A2A', padx = 20, pady = 18)
result_frame.pack(fill = 'x')

forecast_frame = tk.Frame(main_frame, bg = main_frame['bg'])
forecast_frame.pack(fill = 'x', pady = (10, 0))

forecast_title = tk.Label(forecast_frame, text = '📅 5-Day Forecast', bg = forecast_frame['bg'], fg = '#AAAAAA', font=('Segoe UI', 10, 'bold'))
forecast_title.pack(anchor = 'center', pady = (0, 5))

weathericon_label = tk.Label(result_frame, bg = "#2A2A2A", highlightthickness = 0, bd = 0)
weathericon_label.pack(anchor = 'center', pady = (0, 12))
weathericon_label.config(image = weathericon)

city_label = tk.Label(result_frame, text = '', font = ('Segoe UI', 14, 'bold'), fg = '#FFFFFF', bg = '#2A2A2A')
city_label.pack(anchor = 'w', pady = (0, 5))

temp_label = tk.Label(result_frame, text = '', font = ('Segoe UI', 28, 'bold'),  fg = '#F1ECEC', bg = '#2A2A2A')       
temp_label.pack(anchor = 'w', pady =(0, 5))

feels_like_label = tk.Label(result_frame, text = '', font = ('Segoe UI', 12),  fg = '#CCCCCC', bg = '#2A2A2A')           
feels_like_label.pack(anchor = 'w', pady = (0, 2))

condition_label = tk.Label(result_frame, text = '', font = ('Segoe UI', 13, 'bold'),  fg = '#FFFFFF', bg = '#2A2A2A')      
condition_label.pack(anchor = 'w', pady = (0, 2))

description_label = tk.Label(result_frame, text = '' , font = ('Segoe UI', 11), fg = '#BBBBBB', bg = '#2A2A2A')
description_label.pack(anchor = 'w', pady = (0, 4))

wind_speed_label = tk.Label(result_frame, text = '', font = ('Segoe UI', 11), fg = '#BBBBBB', bg = '#2A2A2A')
wind_speed_label.pack(anchor = 'w', pady = (0 ,4))

humidity_label = tk.Label(result_frame, text = '', font = ('Segoe UI', 11),  fg = '#AAAAAA', bg = '#2A2A2A')            
humidity_label.pack(anchor = 'w')

city_entry = ttk.Entry(search_frame, font = ('Segoe UI', 12), cursor = 'xterm')
city_entry.pack(side = 'left', fill = 'x', padx = (0, 10), expand = True)
city_entry.focus()

city_entry.bind('<Return>', enter_pressed)

search_button = ttk.Button(search_frame, text = 'Search', cursor = 'hand2', command = get_weather)
search_button.pack(side = 'right')

apply_dark_theme()

window.mainloop()