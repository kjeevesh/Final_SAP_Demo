from utils.text_to_json_util import *
from utils.sap_itsm_utils import *
import pandas as pd
from datetime import datetime
import ast
import json

class MC_SD_S002(object):
    
    def __init__(self) -> None:
        
        self.utils = Utilities()
        
        creds_fileName = "/home/SAPITSM/finalsapdemo/config/sap_cred.json"
        self.rfc_creds = self.utils.read_json_file(creds_fileName)
        
        return
    
    def s002Execute(self):
        
        exc_data = self.l1_mcsds002()
        
        s002_jsondata = self.convert_df_to_json(exc_data)
        
        print("mcsds002 json data --> ", s002_jsondata)
        
        s002_uniqueid = self.mcsds002_create_uniqueid(s002_jsondata)
        
        print("S002 unique ids --> ", s002_uniqueid)
        
        check_db = self.mcsds002_checkdb(s002_uniqueid)
        
        return
    
    def l1_mcsds002(self):
        
        # ["bukrs","belnr","gjahr","blart","bldat","budat","monat","usnam","tcode"]
        bkpf_fields = ['BUKRS', 'BELNR', 'GJAHR', 'BLART', 'BLDAT', 'BUDAT', 'MONAT', 'USNAM', 'TCODE']
        bkpf_options = []
        # ["kunnr","bukrs","belnr","gjahr"]
        bseg_fields = ['KUNNR', 'BUKRS', 'BELNR', 'GJAHR']
        bseg_options = []
        # ["augbl","auggj","augdt","kunnr","bukrs"]
        bsad_fields = ['AUGBL', 'AUGGJ', 'AUGDT', 'KUNNR', 'BUKRS']
        bsad_options = []
        
        # read the environment variable
        env_var = os.environ["Deployment"]
        
        # Check if the deployment is for dev or for prod        
        if env_var == 'DEV' :
            # set the file path            
            print("--------------------- Accessing JSON files ---------------------")
            file_path1 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_sd_s002/sd_002_bkpf.json'
            file_path2 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_sd_s002/sd_002_bseg.json'
            file_path3 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_sd_s002/sd_002_bsad.json'

            # read the data into a string
            with open(file_path1, 'r') as f1:
                data_bkpf = json.load(f1)
            with open(file_path2, 'r') as f2:
                data_bseg = json.load(f2)
            with open(file_path3, 'r') as f3:
                data_bsad = json.load(f3)
                
        elif env_var == 'PROD' :
            # get the data from SAP table            
            print("------------------------Accessing SAP server------------------------")
        
            data_bkpf = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'BKPF', bkpf_fields, bkpf_options)['DATA']        
            data_bseg = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'BSEG', bseg_fields, bseg_options)['DATA']        
            data_bsad = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'BSAD', bsad_fields, bsad_options)['DATA']

        # create a pandas DataFrame from the list of dictionaries
        for i in range(3):
            if i==0:
                bkpf=pd.json_normalize(data_bkpf)
                #rbkp = pd.DataFrame(data_rbkp)
                bkpf[["bukrs","belnr","gjahr","blart","bldat","budat","monat","usnam","tcode"]] = bkpf['WA'].str.split('|', expand=True)
                bkpf=bkpf.drop("WA",axis=1)
            elif i==1:
                bseg=pd.json_normalize(data_bseg)
                bseg[["kunnr","bukrs","belnr","gjahr"]] = bseg['WA'].str.split('|', expand=True)
                bseg=bseg.drop("WA",axis=1)
            else:
                bsad=pd.json_normalize(data_bsad)
                bsad[["augbl","auggj","augdt","kunnr","bukrs"]] = bsad['WA'].str.split('|', expand=True)
                bsad=bsad.drop("WA",axis=1)
                
        #Apply the filters
        result1=pd.merge(bseg,bsad, on=["kunnr","bukrs"], how="inner")
        #result1=result1.drop(["bukrs","belnr","gjahr"])
        result2=pd.merge(bkpf,result1, on=["bukrs","belnr","gjahr"], how="inner")
        result2 = result2[result2['tcode']=='VF01']
        result2=result2.drop("tcode",axis=1)
        # result2=result2[result2["tcode"]=="VF01"]
        # bkpf_updated=bkpf.drop("tcode",axis=1)
        #result2=result2.sort_values(by=["ebeln","usname"], ascending=True)
        result3=bkpf.drop("tcode",axis=1)
        result3 =result3[(result3['belnr'].isin(result2['augbl']))
        & (result3['gjahr'].isin(result2['auggj']))
        & (result3['bukrs'].isin(result2['bukrs']))
        ]
        #Filtering only necessary rows
        if len(result2)>0 and len(result3)>0:
            lt_output = []
            for _, ls_bkpf in result2.iterrows():
                for _, ls_bkpf_c in result3.iterrows():
                        if (ls_bkpf_c.loc["belnr"] == ls_bkpf.loc["augbl"]) & (ls_bkpf_c.loc["bukrs"] == ls_bkpf.loc["bukrs"]) & (ls_bkpf_c.loc["gjahr"] == ls_bkpf.loc["auggj"]) & (ls_bkpf_c.loc["usnam"] == ls_bkpf.loc["usnam"]):
                            ls_final = {
                            "belnr":ls_bkpf.loc["belnr"],
                            "belnr_c": ls_bkpf_c.loc["belnr"],
                            "usnam_c": ls_bkpf_c.loc["usnam"],
                            "bukrs": ls_bkpf.loc["bukrs"],
                            "gjahr": ls_bkpf.loc["gjahr"],
                            "blart": ls_bkpf.loc["blart"],
                            "bldat": ls_bkpf.loc["bldat"],
                            "budat": ls_bkpf.loc["budat"],
                            "monat": ls_bkpf.loc["monat"],
                            "usnam": ls_bkpf.loc["usnam"],
                            "kunnr": ls_bkpf.loc["kunnr"],
                            "augbl": ls_bkpf.loc["augbl"],
                            "auggj": ls_bkpf.loc["auggj"]
                            }
                            lt_output.append(ls_final)
        lt_output=pd.DataFrame(lt_output)
        lt_output=lt_output.sort_values(["belnr_c","bukrs","gjahr"], ascending=True)
        lt_output=lt_output.drop_duplicates(keep="first")
        
        print("----------05--> MC_SD_S002------------------------------------------------------")
        print("Final exceptions filtered length is > ", len(lt_output))
        
        return lt_output
    
    def convert_df_to_json(self, exception_data):
        
        # Step 1 :  Generate a dataframe variable        
        mongo_df = pd.DataFrame(exception_data)
        
        # Step 2 : convert dataframe into json
        # orient = 'records' to get an o/p of list of dictionaries.
        mongodb_data = mongo_df.to_dict(orient='records')
        
        return mongodb_data
    
    def mcsds002_create_uniqueid(self, exception_data):
        # A function to create unique ids for exception data to put in mongodb
        
        for item in exception_data:
            belnr = str(item['belnr'])
            belnr_c = str(item['belnr_c'])
            gjahr = str(item['gjahr'])
            combined_key = belnr + '_' + belnr_c + '_' + gjahr
            item['uqid'] = combined_key

        return exception_data
    
    def mcsds002_checkdb(self, exception_data):
        
        username = urllib.parse.quote_plus('SAPITSM')
        password = urllib.parse.quote_plus('Azureuser@123')

        # client = MongoClient("mongodb://sapitsm:haihello@123@20.204.119.18:27017")
        client = MongoClient('mongodb://%s:%s@127.0.0.1:27017' % (username, password))

        mydb = client["sapsample01"]

        mycol = mydb["mcsds002"]
        
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
        file_name = 'sds002_data.txt'        
        sds002_result = df.to_string(index = False)        
        self.utils.write_to_a_txt(sds002_result, file_name)
        # <----------------Attachement--------------------->
        
        # <--------- Generate ITSM header data ---------------------------->        
        # A module to send json tickets to ITSM and EKS    
        output_list = []           
        
        print("Creating JSON ticket - MC_SD_S002")     
        
        
        json_skeleton = self.utils.read_json_file('/home/SAPITSM/finalsapdemo/config/itsec001/itsec001_schema.json')            
        json_skeleton['MANDT'] = '1002'
        json_skeleton['RFC'] = '100'
        json_skeleton['REQ_NO'] = '1000000098'
        json_skeleton['ALERT_SEND_DATE'] = self.utils.current_date()
        json_skeleton['ALERT_SEND_TIME'] = '12:05:2023'
        json_skeleton['EVENT_ID'] = 'MC_SD_S002'
        json_skeleton['EVENT_DESCRIPTION'] = 'Maintain sales document and immediately clear customer obligation.'
        json_skeleton['PROGRAM_NAME'] = 'ZMC_SD_S002'
        json_skeleton['SEVERITY'] = 'HIGH'
        json_skeleton['RISK_DESCRIPTION'] = 'Maintain sales document and immediately clear customer obligation.'
        json_skeleton['EVENT_CLASS'] = 'MITIGATION CONTROL'
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
        
        # # sending the data to the Server
        self.utils.send_requests(output_list, file_name)     
        
        return
