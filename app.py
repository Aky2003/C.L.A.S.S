import os
import random
import re
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gridpinning

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

otp_storage = {}

custom_user_agent = "my-geolocation-app"
geolocator = Nominatim(user_agent=custom_user_agent)

@app.route('/')
def index():
    return render_template('agent_login.html')

@app.route('/agent_login', methods=['GET''POST'])
def agent_login():
    agent_name = request.form.get('agent_name', '')
    agent_password = request.form.get('agent_password', '')
    email=request.form.get('email', '')
   
    hardcoded_username = 'adm'
    hardcoded_password = 'asdf'

    if agent_name == hardcoded_username and agent_password == hardcoded_password:
       
        return render_template('login.html',email=email)  
    else:
        
        return redirect(url_for('index', error='Invalid credentials'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '')  
    if email:
        otp = generate_otp()
        send_otp_email(email, otp)  
        otp_storage[email] = otp  
        return render_template('otp_verification.html', email=email)
    else:
        return redirect(url_for('index', error='Email field is missing'))

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    email = request.form.get('email', '')  
    otp_entered = request.form.get('otp', '')  
    
    if email in otp_storage and otp_storage[email] == otp_entered:
        return render_template('upload_image.html')
    else:
        return redirect(url_for('index', error='Invalid OTP'))

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            image.save(os.path.join(UPLOAD_FOLDER, image.filename))
            location_info = get_location_info()
            if location_info:
                location_url, latitude, longitude = location_info
                return render_template('display_url.html', 
                location_url=location_url, latitude=latitude, 
                longitude=longitude)
            else:
                return 'Failed to get location information.'
    return 'No image selected or invalid file format.'

@app.route('/display_address')
def display_address():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if latitude is not None and longitude is not None:
        address = get_address_from_coordinates(latitude, longitude)
        return render_template('display_address.html', address=address)
    else:
        return 'Latitude and longitude parameters are missing.'

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(email, otp):
    sender_email = 'legendguyreports@gmail.com'  
    receiver_email = email
    password = 'bltosyznxhklaydz'  
    smtp_server = 'smtp.gmail.com'  
    smtp_port = 587  
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Your OTP'

    body = f'Your OTP is: {otp}'
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

def get_location_info():
    latitude = None
    longitude = None
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.google.com/maps")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q")))
        location = ""
        search_box.send_keys(location)
        search_box.send_keys(Keys.RETURN)
        time.sleep(9)  
        current_url = driver.current_url
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', 
                          current_url)
        if match:
            latitude = match.group(1)
            longitude = match.group(2)
            gridpinning.droppin(latitude, longitude)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
    return current_url, latitude, longitude




def get_address_from_coordinates(latitude, longitude):
    location = geolocator.reverse((latitude, longitude))
    return location.address

if __name__ == '__main__':
    app.run(debug=True)
