# To run single controls in the api

from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from utils.sap_itsm_utils import *
from controls.bus001 import *
from controls.itsec001 import *
from controls.mc_mm_p003 import *
from controls.mc_mm_p006 import *
from controls.mc_sd_s002 import *

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

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

@app.route('/run_function', methods=['POST'])
def run_function():
    data = request.get_json()

    control = data.get('control')
    interval = data.get('interval')

    if control == 'BUS001':
        scheduler.add_job(BUS001, 'interval', seconds=int(interval))
        return jsonify(message="BUS001 function scheduled successfully")
    elif control == 'ITSEC001':
        scheduler.add_job(ITSEC_001, 'interval', seconds=int(interval))
        return jsonify(message="ITSEC001 function scheduled successfully")
    elif control == 'MCMMP033':
        scheduler.add_job(MCMMP033, 'interval', seconds=int(interval))
        return jsonify(message="MCMMP033 function scheduled successfully")
    elif control == 'MCMMP006':
        scheduler.add_job(MCMMP006, 'interval', seconds=int(interval))   
        return jsonify(message="MCMMP006 function scheduled successfully")
    elif control == 'MCSDS002':
        scheduler.add_job(MCSDS002, 'interval', seconds=int(interval))
        return jsonify(message="MCSDS002 function scheduled successfully")
    else:
        return jsonify(error="Function not found"), 404

@app.route('/stop_cron_job', methods=['POST'])
def stop_cron_job():
    scheduler.shutdown()
    return 'Cron job stopped'

if __name__ == '__main__':
    app.run()
    
# { "control": "BUS001" , "interval": "20"}