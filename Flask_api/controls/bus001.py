from utils.sap_itsm_utils import *
from utils.text_to_json_util import *

class BussCtrl_001(object):
    # A class to host all business controls for the py_sap module.

    def __init__(self) -> None:
        self.utils = Utilities()
        
        creds_fileName = "/home/SAPITSM/finalsapdemo/config/sap_cred.json"
        mongodb_cred = "/home/SAPITSM/finalsapdemo/config/mongodb_creds.json"
        self.rfc_creds = self.utils.read_json_file(creds_fileName)
        self.mongodb_creds = self.utils.read_json_file(mongodb_cred)
    
    def bus001Execute(self):
        
        exc_data = self.l1_date_filtering()
        
        bus001_jsondata = self.convert_df_to_json(exc_data)
        
        print("bus001 json --> ",bus001_jsondata)
        
        bus001_uqid = self.bus001_create_uniqueid(bus001_jsondata)
        
        print("uqid --> ", bus001_uqid)
        
        check_db = self.bus001_checkdb(bus001_uqid)
        
        return
    
    def l1_date_filtering(self): 
        
        # erev = ["bstyp","edokn","fgdat","fgnam"]
        erev_fields = ['BSTYP', 'EDOKN', 'FGDAT', 'FGNAM']
        erev_options = []
        
        # ekko = ["ebeln","bukrs","bstyp","aedat","ernam","lifnr","ekorg","ekgrp","reswk","ktwrt","frggr","frgsx","frgke","loekz"]
        ekko_fields = ['EBELN', 'BUKRS', 'BSTYP', 'AEDAT', 'ERNAM', 'LIFNR', 'EKORG', 'EKGRP', 'RESWK', 'KTWRT', 'FRGGR', 'FRGSX', 'FRGKE', 'LOEKZ']
        ekko_options = []
        
        # lfa1 = ["lifnr","name1"]
        lfa1_fields = ['LIFNR', 'NAME1']
        lfa1_options = []
        
        # ekpo = ["ebeln","ebelp","werks","banfn","loekz"]
        ekpo_fields = ['EBELN', 'EBELP', 'WERKS', 'BANFN', 'LOEKZ']
        ekpo_options = []
        
        # ekkn = ["ebeln","ebelp","kostl","loekz"]
        ekkn_fields = ['EBELN', 'EBELP', 'KOSTL', 'LOEKZ']
        ekkn_options = []
        
        # read the environment variable
        env_var = os.environ["Deployment"]
        
        # Check if the deployment is for dev or for prod        
        if env_var == 'DEV' :
            # set the file path
            print("--------------------- Accessing JSON files ---------------------")
            
            file_path1 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/bus001/erev.json'
            file_path2 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/bus001/ekko.json'
            file_path3 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/bus001/ekpo.json'
            file_path4 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/bus001/lfa1.json'
            file_path5 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/bus001/ekkn.json'
            

            # read the data into a string
            with open(file_path1, 'r') as f1:
                data_erev = json.load(f1)
            with open(file_path2, 'r') as f2:
                data_ekko = json.load(f2)
            with open(file_path3, 'r') as f3:
                data_ekpo = json.load(f3)
            with open(file_path4, 'r') as f3:
                data_lfa1 = json.load(f3)
            with open(file_path5, 'r') as f3:
                data_ekkn = json.load(f3)
        
        elif env_var == 'PROD' :
            # get the data from SAP table            
            print("------------------------Accessing SAP server------------------------")
        
            # get the data from SAP table        
            data_erev = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EREV', erev_fields, erev_options)['DATA']                    
            data_ekko = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EKKO', ekko_fields, ekko_options)['DATA']                    
            data_ekpo = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EKPO', ekpo_fields, ekpo_options)['DATA']            
            data_lfa1 = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'LFA1', lfa1_fields, lfa1_options)['DATA']            
            data_ekkn = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EKKN', ekkn_fields, ekkn_options)['DATA']
    
        # create a pandas DataFrame from the list of dictionaries
        for i in range(5):
            if i==0:
                erev=pd.json_normalize(data_erev)
                erev[["bstyp","edokn","fgdat","fgnam"]] = erev['WA'].str.split('|', expand=True)
                erev=erev.drop("WA",axis=1)
            elif i==1:
                ekko=pd.json_normalize(data_ekko)
                ekko[["ebeln","bukrs","bstyp","aedat","ernam","lifnr","ekorg","ekgrp","reswk","ktwrt","frggr","frgsx","frgke","loekz"]] = ekko['WA'].str.split('|', expand=True)
                ekko=ekko.drop("WA",axis=1)
            elif i==2:
                lfa1=pd.json_normalize(data_lfa1)
                lfa1[["lifnr","name1"]] = lfa1['WA'].str.split('|', expand=True)
                lfa1=lfa1.drop("WA",axis=1)
            elif i==3:
                ekpo=pd.json_normalize(data_ekpo)
                ekpo[["ebeln","ebelp","werks","banfn","loekz"]] = ekpo['WA'].str.split('|', expand=True)
                ekpo=ekpo.drop(["WA"],axis=1)
            else:
                ekkn=pd.json_normalize(data_ekkn)
                ekkn[["ebeln","ebelp","kostl","loekz"]] = ekkn['WA'].str.split('|', expand=True)
                ekkn=ekkn.drop(["WA"],axis=1)
        
        start_date = '2023-02-01'
        end_date = '2023-02-28'
        
        # Generate a range of dates 
        date_range = pd.date_range(start= start_date, end=end_date)
        
        # Convert the date range to the list
        it_date = [date.strftime("%Y%m%d") for date in date_range]
        
        result1= erev[(erev['fgdat'].isin(it_date)) & (erev['bstyp']== 'F')][['bstyp','edokn','fgdat']]
        
        result2 = ekko.loc[(ekko['ebeln'].isin(result1['edokn'])) &
                    (ekko['bstyp'] == 'F') &
                    ((ekko['frgke'] == 'R') | (ekko['frgke'] == 'N')) & (ekko['loekz']== '')]
        
        result2 = result2[['ebeln', 'bukrs', 'bstyp', 'aedat', 'ernam', 'lifnr', 'ekorg', 'ekgrp', 'reswk', 'ktwrt', 'frggr', 'frgsx', 'frgke']]
        result3 = erev.loc[erev['edokn'].isin(result2['ebeln'])]
        result3 = result3[['edokn','fgdat','fgnam']]
    
        output_df = result3.merge(result2, left_on='fgnam', right_on='ernam', how='left')        
        output_df = output_df[['edokn', 'fgdat', 'fgnam']]
        
        print("----------01--> BUS001------------------------------------------------------")
        print("Final exceptions filtered length is > ", len(output_df))
        
        # print(output_df)
        
        return output_df
    
    def convert_df_to_json(self, exception_data):
        
        # Step 1 :  Generate a dataframe variable        
        mongo_df = pd.DataFrame(exception_data)
        
        # Step 2 : convert dataframe into json
        # orient = 'records' to get an o/p of list of dictionaries.
        mongodb_data = mongo_df.to_dict(orient='records')
        
        return mongodb_data
    
    def bus001_create_uniqueid(self, exception_data):
        # A function to create unique ids for exception data to put in mongodb
        
        for item in exception_data:
            purchasing_document = str(item['edokn'])
            created_by = item['fgnam']
            created_on = str(item['fgdat'])
            combined_key = purchasing_document + '_' + created_by + '_' + created_on
            item['uqid'] = combined_key
            
        return exception_data
    
    def bus001_checkdb(self, exception_data):
        
        username = urllib.parse.quote_plus('SAPITSM')
        password = urllib.parse.quote_plus('Azureuser@123')

        # client = MongoClient("mongodb://sapitsm:haihello@123@20.204.119.18:27017")
        client = MongoClient('mongodb://%s:%s@127.0.0.1:27017' % (username, password))

        mydb = client["sapsample01"]

        mycol = mydb["zbus001"]
        
        final_exception_list = []
        
        for item in exception_data:
            combined_value = item['uqid']
            query = {'uqid': combined_value}
            document = mycol.find_one(query)
            if document:
                print("Entry is present in the Database")
                
                # Set the flag to send the JSON request
                send_request = False
                
            else:
                mycol.insert_one(item)
                print("Inserting in the Database...")
                final_exception_list.append(item)
                
                # Set the flag to send the JSON request
                send_request = True
        
        # Send JSON request if the flag is True
        if send_request:
            
            self.l2_create_json_ticket(final_exception_list)    
        
        client.close()
            
        return final_exception_list
    
    def l2_create_json_ticket(self, exception_data):
        
        # <----------------Attachement--------------------->     
        # create an attachment file from the exception data
        # create a .txt file to send as attachment
        df = pd.DataFrame(exception_data)
        file_name = 'bus001_data.txt'
        
        bus001_result = df.to_string(index = False)
        
        self.utils.write_to_a_txt(bus001_result, file_name)
        
        # <----------------Attachement--------------------->
        
        # <--------- Generate ITSM header data ---------------------------->       
        # A module to send json tickets to ITSM and EKS    
        output_list = []           
        
        print("Creating JSON ticket - BUS001")  
        
        # for value in data_list:
        json_skeleton = self.utils.read_json_file('/home/SAPITSM/finalsapdemo/config/itsec001/itsm_schema.json')          
          
        json_skeleton['MANDT'] = '1001'
        json_skeleton['RFC'] = '100'
        json_skeleton['REQ_NO'] = '1000000094'
        json_skeleton['ALERT_SEND_DATE'] = self.utils.current_date()
        json_skeleton['ALERT_SEND_TIME'] = '12:05:2023'
        json_skeleton['EVENT_ID'] = 'BUS001'
        json_skeleton['EVENT_DESCRIPTION'] = 'To highlight PO creation and approval done by the same user'
        json_skeleton['PROGRAM_NAME'] = 'ZBUS001'
        json_skeleton['SEVERITY'] = 'HIGH'
        json_skeleton['RISK_DESCRIPTION'] = 'PO released by same user'
        json_skeleton['EVENT_CLASS'] = 'BUSINESS'
        json_skeleton['CATEGORIES'] = 'SOD VIOLATIONS'
        json_skeleton['RISK_OWNER'] = 'ETD_ALERT'
        json_skeleton['ALERT_CLOSED_DATE'] = ''
        json_skeleton['ALERT_STATUS'] = 'SUCCESS'
        json_skeleton['STATUS'] = 'OPEN'
        json_skeleton['INCIDENT_NO'] = '' 
                 
        output_list.append(json_skeleton)
        
        # <--------- Generate ITSM header data ---------------------------->
        
        # sending the data to the Server
        # self.utils.send_requests(output_list)
        
        # checking with attachment part
        self.utils.send_requests(output_list, file_name)           
        
        return
