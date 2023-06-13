# To run multiple controls in API

from flask import Flask, request, jsonify, current_app
from apscheduler.schedulers.background import BackgroundScheduler
from utils.sap_itsm_utils import *
from controls.bus001 import *
from controls.itsec001 import *
from controls.mc_mm_p003 import *
from controls.mc_mm_p006 import *
from controls.mc_sd_s002 import *

app = Flask(__name__)
scheduler = BackgroundScheduler()

# set the environment variable
# either "DEV" or "PROD"
os.environ["Deployment"] = "DEV"

print("Deployment is set as --> ",os.environ["Deployment"])

def BUS001():
    # Implement your logic for the BUS001 function here
    control1 = BussCtrl_001()
    # This is just a placeholder function for demonstration purposes
    print("Running BUS001 function")
    
    control1.bus001Execute()

def ITSEC_001():
    # Implement your logic for the BUS001 function here
    control2 = ITSEC001()
    # This is just a placeholder function for demonstration purposes
    print("Running ITSEC001 function")
    
    control2.itsecExecute()

def MCMMP033():
    # Implement your logic for the BUS001 function here
    control3 = MC_MM_P003()
    # This is just a placeholder function for demonstration purposes
    print("Running MCMMP033 function")
    
    control3.p003Execute()

def MCMMP006():
    # Implement your logic for the BUS001 function here
    control4 = MC_MM_P006()
    # This is just a placeholder function for demonstration purposes
    print("Running MCMMP006 function")
    
    control4.p006Execute()

def MCSDS002():
    # Implement your logic for the BUS001 function here
    control5 = MC_SD_S002()
    # This is just a placeholder function for demonstration purposes
    print("Running MCSDS002 function")
    
    control5.s002Execute()

def job_function(control):
    
    if control == 'BUS001':
        scheduler.add_job(BUS001)
        return jsonify(message="BUS001 function scheduled successfully")
    elif control == 'ITSEC001':
        scheduler.add_job(ITSEC_001)
        return jsonify(message="ITSEC001 function scheduled successfully")
    elif control == 'MCMMP033':
        scheduler.add_job(MCMMP033)   
        return jsonify(message="MCMMP033 function scheduled successfully")
    elif control == 'MCMMP006':
        scheduler.add_job(MCMMP006)   
        return jsonify(message="MCMMP006 function scheduled successfully")
    elif control == 'MCSDS002':
        scheduler.add_job(MCSDS002)   
        return jsonify(message="MCSDS002 function scheduled successfully")
    else:
        print(f"Unknown control: {control}")


@app.route('/run_function', methods=['POST'])
def run_function():
    try:
        with app.app_context():
            
            data = request.get_json()

            controls = data.get('control')
            interval = data.get('interval')

            if controls and isinstance(controls, list):
                for control in controls:
                    scheduler.add_job(job_function, 'interval', args=[control], seconds=int(interval))      
                return jsonify(message="Cron jobs scheduled successfully")
            else:
                return jsonify(error="Invalid controls"), 400
    
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/display_input', methods=['POST'])
def display_input():
    try:
        with app.app_context():
            
            data = request.get_json()
            
            print(data)    
            return jsonify(message="Input received successfully")

    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)