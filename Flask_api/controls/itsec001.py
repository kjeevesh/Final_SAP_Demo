import pandas as pd
import ast
from datetime import datetime
from utils.text_to_json_util import *
from utils.sap_itsm_utils import *

class ITSEC001(object):

    def __init__(self) -> None: 
        
        self.utils = Utilities()
        
        creds_fileName = "/home/SAPITSM/finalsapdemo/config/sap_cred.json"
        self.rfc_creds = self.utils.read_json_file(creds_fileName)
        
        self.profile_names = ["SAP_ALL","SAP_NEW","S_A.SYSTEM","S_A.ADMIN","S_A.CUSTOMIZ","S_A.DEVELOP","S_A.USER","S_USER.ALL","S_ABAP_ALL","S_RZL_ADMIN"]
    
    def itsecExecute(self):
        
        exc_data = self.l1_itsec001()
        
        itsec001_jsondata = self.convert_df_to_json(exc_data)
        
        print("itsec001 json data --> ", itsec001_jsondata)
        
        itsec001_uniqueid = self.itsec001_create_uniqueid(itsec001_jsondata)
        
        print("ITSEC001 unique ids --> ", itsec001_uniqueid)
        
        check_db = self.itsec001_checkdb(itsec001_uniqueid)
        
        return
    
    def l1_itsec001(self):
        
        # Get the current date and time
        now = datetime.now()
        # Format the date and time as a string in the format 'YYYYMMDD'
        formatted_date = now.strftime('%Y%m%d')
        
        # important profiles list
        rt_profile=["SAP_ALL","SAP_NEW","S_A.SYSTEM","S_A.ADMIN","S_A.CUSTOMIZ","S_A.DEVELOP","S_A.USER","S_USER.ALL","S_ABAP_ALL","S_RZL_ADMIN"]
        
        # ["bname","usty","gltgy","gltgb"]        
        usr02_fields = ['BNAME', 'USTYP', 'GLTGV', 'GLTGB']
        usr02_options = []
        # ["bname","profile"]
        ust04_fields = ['BNAME', 'PROFILE']
        ust04_options = []
        # [["bname","fullname"]]
        user_addr_fields = ['BNAME', 'NAME_TEXTC']
        user_addr_options = []
        
        # read the environment variable
        env_var = os.environ["Deployment"]
        
        # Check if the deployment is for dev or for prod        
        if env_var == 'DEV' :
            # set the file path            
            print("--------------------- Accessing JSON files ---------------------")
            
            file_path1 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/itsec001/usr02.json'
            file_path2 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/itsec001/ust04.json'
            file_path3 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/itsec001/user_addr.json'

            # read the data into a string
            with open(file_path1, 'r') as f1:
                data_usr02 = json.load(f1)
            with open(file_path2, 'r') as f2:
                data_ust04 = json.load(f2)
            with open(file_path3, 'r') as f3:
                data_useraddr = json.load(f3)
        
        elif env_var == 'PROD' :
            # get the data from SAP table            
            print("------------------------Accessing SAP server------------------------")      
            
            data_usr02 = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'USR02', usr02_fields, usr02_options)['DATA']        
            data_ust04 = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'UST04', ust04_fields, ust04_options)['DATA']        
            data_useraddr = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'USER_ADDR', user_addr_fields, user_addr_options)['DATA']

        # create a pandas DataFrame from the list of dictionaries
        for i in range(3):
            if i==0:
                ust04 = pd.DataFrame(data_ust04)
                ust04[["bname","profile"]] = ust04['WA'].str.split('|', expand=True)
                ust04=ust04.drop("WA",axis=1)
            elif i==1:
                usr02 = pd.DataFrame(data_usr02)
                usr02[["bname","usty","gltgy","gltgb"]] = usr02['WA'].str.split('|', expand=True)
                usr02=usr02.drop("WA",axis=1)
            else:
                useraddr = pd.DataFrame(data_useraddr)
                useraddr[["bname","fullname"]] = useraddr['WA'].str.split('|', expand=True)
                useraddr=useraddr.drop("WA",axis=1)
        
        usr02= usr02[(usr02['gltgy'] <= formatted_date) & (usr02['gltgb'] >= formatted_date)]
        ust04_striped=df = ust04[ust04['profile'].isin(rt_profile)]
        
        usr42=pd.merge(ust04_striped,usr02, on='bname')
        
        # usr42_filtered contains merged df and only those rows tht have user type as A(dialog user)
        usr42_filtered=usr42[usr42['usty']=='A']     
        
        usr42_merged=pd.merge(usr42_filtered,useraddr, on='bname')
        
        usr42_merged = usr42_merged.drop_duplicates(subset='bname', keep='first')
        
        # # to find the unique names of the list
        # usr42_merged = usr42_merged['fullname'].unique()
        
        # filtering out only those rows which have gltv value as <=today and gltb >=today
        #usr42_updated = usr42_merged[(usr42_merged['gltgy'] <= formatted_date) & (usr42_merged['gltgb'] >= formatted_date)]
        print("----------02--> IT_SEC_001------------------------------------------------------")
        print("Final exceptions filtered length is > ", len(usr42_merged))
        
        # print(usr42_merged)
        return usr42_merged
    
    def convert_df_to_json(self, exception_data):
        
        # Step 1 :  Generate a dataframe variable        
        mongo_df = pd.DataFrame(exception_data)
        
        # Step 2 : convert dataframe into json
        # orient = 'records' to get an o/p of list of dictionaries.
        mongodb_data = mongo_df.to_dict(orient='records')
        
        return mongodb_data
    
    def itsec001_create_uniqueid(self, exception_data):
        # A function to create unique ids for exception data to put in mongodb        
        
        for item in exception_data:
            gltgy = str(item['gltgy'])
            bname = item['bname']
            profile = str(item['profile'])
            combined_key = gltgy + '_' + bname + '_' + profile
            item['uqid'] = combined_key
            
        return exception_data
    
    def itsec001_checkdb(self, exception_data):
        
        username = urllib.parse.quote_plus('SAPITSM')
        password = urllib.parse.quote_plus('Azureuser@123')

        # client = MongoClient("mongodb://sapitsm:haihello@123@20.204.119.18:27017")
        client = MongoClient('mongodb://%s:%s@127.0.0.1:27017' % (username, password))

        mydb = client["sapsample01"]

        mycol = mydb["itsec001"]
        
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
        # create a .txt file to send as attachment
        df = pd.DataFrame(exception_data)
        file_name = 'itsec001_data.txt'
        
        sds002_result = df.to_string(index = False)
        
        self.utils.write_to_a_txt(sds002_result, file_name)
        # <----------------Attachement--------------------->
        
        # <--------- Generate ITSM header data ---------------------------->              
        # A module to send json tickets to ITSM and EKS    
        output_list = []           
        
        print("Creating JSON ticket - ITSEC001")     
        
        # for value in data_list:
        json_skeleton = self.utils.read_json_file('/home/SAPITSM/finalsapdemo/config/itsec001/itsec001_schema.json')            
        json_skeleton['MANDT'] = '1002'
        json_skeleton['RFC'] = '100'
        json_skeleton['REQ_NO'] = '1000000095'
        json_skeleton['ALERT_SEND_DATE'] = self.utils.current_date()
        json_skeleton['ALERT_SEND_TIME'] = '12:05:2023'
        json_skeleton['EVENT_ID'] = 'ITSEC001'
        json_skeleton['EVENT_DESCRIPTION'] = 'Control will monitor privileged SAP profiles (SAP_ALL; SAP_NEW) assigned to Dialog user'
        json_skeleton['PROGRAM_NAME'] = 'ZITSEC001'
        json_skeleton['SEVERITY'] = 'CRITICAL'
        json_skeleton['RISK_DESCRIPTION'] = 'Critical Profile'
        json_skeleton['EVENT_CLASS'] = 'SECURITY'
        json_skeleton['CATEGORIES'] = 'IT SECURITY-CRITICAL PROFILE'
        json_skeleton['RISK_OWNER'] = 'ETD_ALERT'
        json_skeleton['ALERT_CLOSED_DATE'] = ''
        json_skeleton['ALERT_STATUS'] = 'SUCCESS'
        json_skeleton['STATUS'] = 'OPEN'
        json_skeleton['INCIDENT_NO'] = '' 
                 
        output_list.append(json_skeleton)
        # <--------- Generate ITSM header data ---------------------------->
        
        # sending the data to the Server
        # self.utils.send_requests(output_list)
        
        # # sending the data to the Server
        self.utils.send_requests(output_list, file_name)     
        
        return
