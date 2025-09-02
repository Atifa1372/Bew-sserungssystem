from flask import Flask, request, jsonify , render_template 
from apscheduler.schedulers.background import BackgroundScheduler
import RPi.GPIO as GPIO 
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import threading
from flask_cors import CORS



app = Flask(__name__)

CORS(app, resources=r'/*')

#gpio setup
GPIO.setmode(GPIO.BCM)

RELAY_PINS={
    1:17,  # relay_pin 1 an gpio 18 von rasp
    2:23,
    3:24
}

for pin in RELAY_PINS.values():

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH) 




#dictionery zur Speicherung value of sensoren und pumpe status
pumpen={
    1:{"sensor_pin" : "A0" , "pump_status": False},  # sensor_id
    2:{"sensor_pin" : "A1" , "pump_status": False},
    3:{"sensor_pin" : "A2" , "pump_status": False},
}



i2c = busio.I2C(board.SCL , board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain=1
 #kanäle für sensoren (sensor_id)
channels ={
    1:AnalogIn( ads,ADS.P0),
    2:AnalogIn( ads,ADS.P1),
    3:AnalogIn( ads,ADS.P2)

} 


def rechnug_feuchtigkeit(sensor_id):
    rueckgabe = 100
    

    total_value = 0
    succsess_measures = 0
    chan = channels[sensor_id]  # zur Azswahl von Sensoren 
    
  
    # Mehrere Messungen vornehmen und mitteln
    for _ in range(10): # Anzahl der Messungen für den Durchschnitt-berechnungen 
        try:
            raw_value = chan.value  # Roher Wert des Sensors
            succsess_measures += 1
            total_value += raw_value
        except:
            print(f"error in run {_}")
        
        time.sleep(0.1) 

    # Durchschnitt berechnen
    
    avg_raw_value = total_value / succsess_measures

    # Umrechnung des Rohwerts in Prozent (Skala von 0 bis 100%)
    prozent = (avg_raw_value / 32767.0) * 100
    rueckgabe = 100 - prozent
    
    return rueckgabe



@app.route('/status' , methods=['GET']) 

def get_status():
    statuses = {}

    for sensor_id , _ in pumpen.items():
        feuchtigkeit_prozent = rechnug_feuchtigkeit(sensor_id)
        pump_status = "off" if feuchtigkeit_prozent > 20 else "on"
        statuses[sensor_id] = {
            "feuchtigkeit":f"{feuchtigkeit_prozent:.2f}","Pumpe":pump_status
        }
        response = jsonify(statuses)

    response.headers.add('Access-control-Allow-Origin' , '*')
    
    
    return response 


    


#  http://127.0.0.1:5001/control?action=stop  oder http://127.0.0.1:5001/control?sensor_id=1&action=start
@app.route('/control' , methods=['GET'])

def control_pump():

    
    action = request.args.get('action')
    sensor_id = int(request.args.get('sensor_id'))
    
    
    if action == 'start':
        
        pumpe_start(sensor_id)
        return jsonify({"Status" : "Pumpe gestartet!"}) ,200
    
    elif action == 'stop':
        
        pumpe_stop(sensor_id)
        return jsonify({"Status": "Pumpe gestoppt!"}),200
    
    else:
        return jsonify({"Status": "Ungültige action"}), 400
   



@app.route('/auto-control' , methods=['GET'])

def auto_control():

    result= auto_control_logic()


    return jsonify({"Status": result})


def auto_control_logic():

    result = []

    for sensor_id in pumpen:
        feuchtigkeit_prozent = rechnug_feuchtigkeit(sensor_id)
        
        if feuchtigkeit_prozent < 20:  # Feuchtigkeit unter 20% - Pumpe an
            pumpe_start(sensor_id)
            result.append(f"Pumpe {sensor_id}: Der Boden ist trocken, Pumpe eingeschaltet.") 
        else:
            pumpe_stop(sensor_id)
            result.append(f"Pumpe {sensor_id}: Der Boden ist feucht, Pumpe ausgeschaltet.")

    return result

    
# Initialisiere den Scheduler
# 2 mal Bewässerung im Woche reicht 
scheduler = BackgroundScheduler()
scheduler.add_job(func=auto_control_logic, trigger="interval", days=2)  #hours=20  minutes=10

scheduler.start()




def pumpe_start(sensor_id):
    GPIO.output(RELAY_PINS[sensor_id], GPIO.LOW)  # Relais aktivieren und pumpe starten
    pumpen[sensor_id]["pump_status"] = True
    print(f"Pumpe {sensor_id} wurde gestartet!")
    
    threading.Thread(target=run_pump_for_5_seconds, args=(sensor_id,)).start()
    
    

def pumpe_stop(sensor_id):
    try:
        GPIO.output(RELAY_PINS[sensor_id], GPIO.HIGH)  # Relais deaktivieren und pumpe stoppen
        pumpen[sensor_id]["pump_status"] = False  
        print(f"Pumpe {sensor_id} wurde gestoppt!")
    except:
        print('error')



# Funktion: Pumpe für 5 Sekunden laufen lassen und dann stoppen
def run_pump_for_5_seconds(sensor_id):
    time.sleep(5) 
    pumpe_stop(sensor_id)  


    
if __name__ == '__main__':
    
    app.run(host='0.0.0.0' , port=5001 , debug=True )




