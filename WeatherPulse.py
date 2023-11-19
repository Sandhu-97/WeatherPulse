from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import requests
import pytz
from PIL import ImageTk, Image
from config import API_KEY

root = Tk()
root.title('WeatherPulse')
root.geometry('890x470+300+200') 
root.config(bg='#57adff')
root.resizable(False, False)
root.iconbitmap('images/icon.ico')

APP_KEY = API_KEY
base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}?key='+APP_KEY+'&unitGroup=uk&include=current'

def search_button():
    city = search_box_entry.get()
    request = requests.get(base_url.format(city))


    if request.status_code != requests.codes.ok:
        messagebox.showerror('Error','City not found!')
        return
    
    data = request.json()
    search_box_entry.delete(0, END)
    search_box_entry.insert(0, city.title())

    latitude, longitude, timezone = data['latitude'], data['longitude'], data['timezone']
    time = datetime.now(pytz.timezone(timezone))
    formatted_time = time.strftime('%I:%M %p')

    long_lat_label.config(text=f'{round(latitude, 2)}°N {round(longitude, 2)}°E')
    timezone_label.config(text=timezone)
    clock_label.config(text=formatted_time)

    current_temp = data['days'][0]['temp']
    current_humidity = data['days'][0]['humidity']
    current_pressure = data['days'][0]['pressure']
    current_windspeed = data['days'][0]['windspeed']
    current_conditions = data['days'][0]['conditions']
    
    current_label_values = [f"{current_temp}°C", f'{current_humidity}%', f'{current_pressure}mb', f'{current_windspeed}km/h', current_conditions]
    
    temp_value_label.config(text=current_label_values[0])
    humidity_value_label.config(text=current_label_values[1])
    pressure_value_label.config(text=current_label_values[2])
    windspeed_value_label.config(text=current_label_values[3])
    if len(current_label_values[4])<10:
        description_value_label.config(text=current_label_values[4], font=('Helvetica', 11, 'bold'))
    else:
        description_value_label.config(text=current_label_values[4], font=('Helvetica', 7, 'bold'))

    day1_label.config(text='Today')
    day2_label.config(text='Tommorrow')

    day_labels = [day3_label, day4_label, day5_label, day6_label, day7_label]
    days_to_add = 2
    for day_label in day_labels:
        day = (datetime.now()+timedelta(days=days_to_add)).strftime('%A')
        if len(day) >= 9:
            font = 'arial 7 bold'
        else:
            font = 'arial 10 bold'
        day_label.config(text=day, font=font)
        days_to_add+=1


    image1 = Image.open(f'images/weather_conditions/{data["days"][0]["icon"]}.png').resize((80, 80))
    image1 = ImageTk.PhotoImage(image1)
    image1_label.config(image=image1)
    image1_label.image = image1

    image_labels = [image2_label, image3_label, image4_label, image5_label, image6_label, image7_label]
    icon_no = 1
    for image_label in image_labels:
        icon = data['days'][icon_no]['icon']
        img = Image.open(f'images/weather_conditions/{icon}.png').resize((45, 40))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        icon_no+=1

    min1 = data['days'][0]['tempmin']
    max1 = data['days'][0]['tempmax']
    min_max_string = f"Max: {max1}°C\nMin: {min1}°C"
    day1temp_label.config(text=min_max_string)

    day_temp_labels = [day2temp_label, day3temp_label, day4temp_label, day5temp_label, day6temp_label, day7temp_label]
    day_temp_no = 1
    for day_temp in day_temp_labels:
        min = data['days'][day_temp_no]['tempmin']
        max = data['days'][day_temp_no]['tempmax']
        min_max_string = f"Max: {max}°C\nMin: {min}°C"
        day_temp.config(text=min_max_string)
        day_temp_no+=1



# images for to display data    
bigbox_image = PhotoImage(file='images/Rounded Rectangle 2.png')
smallbox_image = PhotoImage(file='images/Rounded Rectangle 2 copy.png')
round_box = PhotoImage(file='images/Rounded Rectangle 1.png')

#label for current weather
round_box_label = Label(root, image=bigbox_image, bg='#203243')
round_box_label.place(x=30, y=90)

#font for round box
round_box_font = ('Helvetica', 11, 'bold')

#labels to show what is being displayed
temperature_label = Label(root, text='Temperature', font=round_box_font, fg='white', bg='#203243')
temperature_label.place(x=40, y=100)
humidity_label = Label(root, text='Humidity', font=round_box_font, fg='white', bg='#203243')
humidity_label.place(x=40, y=125)
pressure_label = Label(root, text='Pressure', font=round_box_font, fg='white', bg='#203243')
pressure_label.place(x=40, y=150)
windspeed_label = Label(root, text='Wind Speed', font=round_box_font, fg='white', bg='#203243')
windspeed_label.place(x=40, y=175)
description_label = Label(root, text='Description', font=round_box_font, fg='white', bg='#203243')
description_label.place(x=40, y=200)

# current weather details
temp_value_label = Label(root, font=round_box_font,fg='white', bg='#203243')
humidity_value_label = Label(root, font=round_box_font,fg='white', bg='#203243')
pressure_value_label = Label(root, font=round_box_font,fg='white', bg='#203243')
windspeed_value_label = Label(root, font=round_box_font,fg='white', bg='#203243')
description_value_label = Label(root, font=round_box_font,fg='white', bg='#203243')

# x coordinate for current weather labels
X = 160
temp_value_label.place(x=X, y=100)
humidity_value_label.place(x=X, y=125)
pressure_value_label.place(x=X, y=150)
windspeed_value_label.place(x=X, y=175)
description_value_label.place(x=X, y=200)


search_box_image = PhotoImage(file='images/Rounded Rectangle 3.png')
search_box_label = Label(root, image=search_box_image, bg='#57adff')
search_box_label.place(x=300, y=120)

cloud_image = PhotoImage(file='images/Layer 7.png')
cloud_image_label = Label(root, image=cloud_image, bg='#203243')
cloud_image_label.place(x=320, y=127)

search_box_entry = Entry(root, justify='center', width=15, font=('poppins', 25, 'bold'), bg='#203243', border=0, fg='white')
search_box_entry.place(x=390, y=130)
search_box_entry.focus()

#search button
search_icon = PhotoImage(file='images/Layer 6.png')
search_icon_button = Button(root, image=search_icon, bg='#203243', borderwidth=0, cursor='hand2', command=search_button)
search_icon_button.place(x=676, y=125)

bottom_frame = Frame(root, width=900, height=180, bg='#212120')
bottom_frame.pack(side=BOTTOM)

bigbox_image = PhotoImage(file='images/Rounded Rectangle 2.png')
smallbox_image = PhotoImage(file='images/Rounded Rectangle 2 copy.png')

# labels for forecast data
Label(bottom_frame, image=bigbox_image, bg='#212120').place(x=30, y=20)
Label(bottom_frame, image=smallbox_image, bg='#212120').place(x=300, y=30)
Label(bottom_frame, image=smallbox_image, bg='#212120').place(x=400, y=30)
Label(bottom_frame, image=smallbox_image, bg='#212120').place(x=500, y=30)
Label(bottom_frame, image=smallbox_image, bg='#212120').place(x=600, y=30)
Label(bottom_frame, image=smallbox_image, bg='#212120').place(x=700, y=30)
Label(bottom_frame, image=smallbox_image, bg='#212120').place(x=800, y=30)


clock_label = Label(root, font=('Helvetica', 30, 'bold'), fg='white', bg='#57adff')
clock_label.place(x=30, y=20)

timezone_label = Label(root, font=('Helvetica', 16, 'bold'), fg='white', bg='#57adff')
timezone_label.place(x=660, y=20)

long_lat_label = Label(root, font=('Helvetica', 10, 'bold'), fg='white', bg='#57adff')
long_lat_label.place(x=660, y=45)

#frames for forecast data

# first frame data
first_frame = Frame(root, width=230, height=132, bg='#282829')
first_frame.place(x=35, y=315)
second_frame = Frame(root, width=70, height=115, bg='#282829')
second_frame.place(x=305, y=325)
third_frame = Frame(root, width=70, height=115, bg='#282829')
third_frame.place(x=405, y=325)
fourth_frame = Frame(root, width=70, height=115, bg='#282829')
fourth_frame.place(x=505, y=325)
fifth_frame = Frame(root, width=70, height=115, bg='#282829')
fifth_frame.place(x=605, y=325)
sixth_frame = Frame(root, width=70, height=115, bg='#282829')
sixth_frame.place(x=705, y=325)
seventh_frame = Frame(root, width=70, height=115, bg='#282829')
seventh_frame.place(x=805, y=325)

day1_label = Label(first_frame, bg='#282829', fg='#fff', anchor=CENTER, font='arial 15 bold')
day2_label = Label(second_frame, bg='#282829', fg='#fff', anchor=CENTER, font='arial 7 bold')
day3_label = Label(third_frame, bg='#282829', fg='#fff', anchor=CENTER)
day4_label = Label(fourth_frame, bg='#282829', fg='#fff', anchor=CENTER)
day5_label = Label(fifth_frame, bg='#282829', fg='#fff', anchor=CENTER)
day6_label = Label(sixth_frame, bg='#282829', fg='#fff', anchor=CENTER)
day7_label = Label(seventh_frame, bg='#282829', fg='#fff', anchor=CENTER)
day1_label.place(x=80, y=5)
day2_label.place(x=8, y=5)
day3_label.place(x=8, y=5)
day4_label.place(x=8, y=5)
day5_label.place(x=8, y=5)
day6_label.place(x=8, y=5)
day7_label.place(x=8, y=5)



image1_label = Label(first_frame, bg='#282829')
image2_label = Label(second_frame, bg='#282829', width=65, justify='center')
image3_label = Label(third_frame, bg='#282829', width=65, justify='center')
image4_label = Label(fourth_frame, bg='#282829', width=65, justify='center')
image5_label = Label(fifth_frame, bg='#282829', width=65, justify='center')
image6_label = Label(sixth_frame, bg='#282829', width=65, justify='center')
image7_label = Label(seventh_frame, bg='#282829', width=65, justify='center')
image1_label.place(x=10, y=41)
image2_label.place(x=1, y=24)
image3_label.place(x=1, y=24)
image4_label.place(x=1, y=24)
image5_label.place(x=1, y=24)
image6_label.place(x=1, y=24)
image7_label.place(x=1, y=24)

day1temp_label = Label(first_frame, bg='#282829', justify='center', fg='#57adff', font='arial 15 bold')
day2temp_label = Label(second_frame, bg='#282829', justify='center', fg='white', anchor='w')
day3temp_label = Label(third_frame, bg='#282829', justify='center', fg='white', anchor='w')
day4temp_label = Label(fourth_frame, bg='#282829', justify='center', fg='white', anchor='w')
day5temp_label = Label(fifth_frame, bg='#282829', justify='center', fg='white', anchor='w')
day6temp_label = Label(sixth_frame, bg='#282829', justify='center', fg='white', anchor='w')
day7temp_label = Label(seventh_frame, bg='#282829', justify='center', fg='white', anchor='w')
day1temp_label.place(x=105, y=55)
day2temp_label.place(x=1, y=70)
day3temp_label.place(x=1, y=70)
day4temp_label.place(x=1, y=70)
day5temp_label.place(x=1, y=70)
day6temp_label.place(x=1, y=70)
day7temp_label.place(x=1, y=70)


root.mainloop()