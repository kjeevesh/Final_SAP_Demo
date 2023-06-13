import pandas as pd
import ast
from datetime import datetime 
from utils.text_to_json_util import *
from utils.sap_itsm_utils import *
import json

class MC_MM_P006(object):
    
    def __init__(self) -> None:
        
        self.utils = Utilities()
        
        creds_fileName = "/home/SAPITSM/finalsapdemo/config/sap_cred.json"
        self.rfc_creds = self.utils.read_json_file(creds_fileName)
        
        return
    
    def p006Execute(self):
        
        exc_data = self.l1_mcmmp006()
        
        p006_jsondata = self.convert_df_to_json(exc_data)
        
        print("mcmmp006 json data --> ", p006_jsondata)
        
        p006_uniqueid = self.mcmmp006_create_uniqueid(p006_jsondata)
        
        print("P006 unique ids --> ", p006_uniqueid)
        
        check_db = self.mcmmp006_checkdb(p006_uniqueid)
        
        return
    
    def l1_mcmmp006(self):
               
        rbkp_fields = ['BUKRS', 'BELNR', 'GJAHR', 'BLART', 'BLDAT', 'BUDAT', 'USNAM', 'RBSTAT']
        rbkp_options = []
        
        rseg_fields = ['EBELN', 'MATNR', 'BUKRS', 'BELNR', 'GJAHR']
        rseg_options = []
        
        ekbe_fields = ['EBELN', 'BELNR', 'GJAHR']
        ekbe_options = []
        
        mkpf_fields = ['USNAM', 'MBLNR', 'MJAHR']
        mkpf_options = []
        
        # read the environment variable
        env_var = os.environ["Deployment"]
        
        # Check if the deployment is for dev or for prod        
        if env_var == 'DEV' :
            # set the file path            
            print("--------------------- Accessing JSON files ---------------------")
        
            file_path1 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_mm_p006/rbkp.json'
            file_path2 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_mm_p006/rseg.json'
            file_path3 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_mm_p006/ekbe.json'
            file_path4 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_mm_p006/mkpf.json'

            # read the data into a string
            with open(file_path1, 'r') as f1:
                data_rbkp = json.load(f1)
            with open(file_path2, 'r') as f2:
                data_rseg = json.load(f2)
            with open(file_path3, 'r') as f3:
                data_ekbe = json.load(f3)
            with open(file_path4, 'r') as f4:
                data_mkpf = json.load(f4)
        
        elif env_var == 'PROD' :
            # get the data from SAP table            
            print("------------------------Accessing SAP server------------------------")
        
            data_rbkp = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'RBKP', rbkp_fields, rbkp_options)['DATA']        
            data_rseg = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'RSEG', rseg_fields, rseg_options)['DATA']        
            data_ekbe = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EKBE', ekbe_fields, ekbe_options)['DATA']        
            data_mkpf = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'MKPF', mkpf_fields, mkpf_options)['DATA']        


        # create a pandas DataFrame from the list of dictionaries
        for i in range(4):
            if i==0:
                rbkp=pd.json_normalize(data_rbkp)
                #rbkp = pd.DataFrame(data_rbkp)
                rbkp[["bukrs","belnr","gjahr","blart","bldat","budat","usnam","rbstat"]] = rbkp['WA'].str.split('|', expand=True)
                rbkp=rbkp.drop("WA",axis=1)
                rbkp = rbkp[(rbkp["budat"]>'20220901') & (rbkp['budat']<'20220930')]
            elif i==1:
                rseg=pd.json_normalize(data_rseg)
                rseg[["ebeln","matnr","bukrs","belnr","gjahr"]] = rseg['WA'].str.split('|', expand=True)
                rseg=rseg.drop("WA",axis=1)
            elif i==2:
                ekbe=pd.json_normalize(data_ekbe)
                ekbe[["ebeln","belnr","gjahr"]] = ekbe['WA'].str.split('|', expand=True)
                ekbe=ekbe.drop("WA",axis=1)
            else:
                mkpf=pd.json_normalize(data_mkpf)
                mkpf[["usname","mblnr","mjahr"]] = mkpf['WA'].str.split('|', expand=True)
                mkpf=mkpf.drop("WA",axis=1) 
                
        # display the DataFrame
        #print(dfaddr)
        
        result1=pd.merge(rbkp,rseg, on=["bukrs","belnr","gjahr"], how="inner")
        #result1=result1.drop(["bukrs","belnr","gjahr"])
        result1=result1[(result1["blart"]=="RE") & (result1["rbstat"]=="5")]
        result1=result1.drop("rbstat",axis=1)
        result2=pd.merge(ekbe,mkpf, left_on=["belnr","gjahr"],right_on=["mblnr","mjahr"], how="inner")
        result2=result2.drop(["mblnr","mjahr"],axis=1)
        result2 = result2.loc[result2['ebeln'].isin(result1['ebeln'])]
        result1=result1.sort_values(by=["ebeln","usnam"], ascending=True)
        result2=result2.sort_values(by=["ebeln","usname"], ascending=True)
    
        if len(result1)>0 and len(result2)>0:
            lt_output = []
            for _, ls_rbkp in result1.iterrows():
                for _, ls_ekbe in result2.iterrows():
                        if (ls_ekbe.loc["ebeln"] == ls_rbkp.loc["ebeln"]) & (ls_ekbe.loc["usname"] == ls_rbkp.loc["usnam"]):
                            ls_final = {
                            
                            "mblnr": ls_ekbe.loc["belnr"],
                            "mjahr": ls_ekbe.loc["gjahr"],
                            "usnam_m": ls_ekbe.loc["usname"],
                            "bukrs": ls_rbkp.loc["bukrs"],
                            "belnr": ls_rbkp.loc["belnr"],
                            "gjahr": ls_rbkp.loc["gjahr"],
                            "blart": ls_rbkp.loc["blart"],
                            "bldat": ls_rbkp.loc["bldat"],
                            "budat": ls_rbkp.loc["budat"],
                            "usnam": ls_rbkp.loc["usnam"],
                            "matnr": ls_rbkp.loc["matnr"],
                            "ebeln": ls_rbkp.loc["ebeln"]
                            }
                
                            lt_output.append(ls_final)
                            
        lt_output=pd.DataFrame(lt_output)
        lt_output=lt_output.sort_values(["ebeln","usnam"], ascending=True)
        lt_output=lt_output.drop_duplicates(keep="first")
        lt_output=lt_output.drop_duplicates(subset="belnr")
        
        print("----------04--> MC_MM_P006------------------------------------------------------")
        print("Final exceptions filtered length is > ", len(lt_output))
        
        return lt_output
    
    def convert_df_to_json(self, exception_data):
        
        # Step 1 :  Generate a dataframe variable        
        mongo_df = pd.DataFrame(exception_data)
        
        # Step 2 : convert dataframe into json
        # orient = 'records' to get an o/p of list of dictionaries.
        mongodb_data = mongo_df.to_dict(orient='records')
        
        return mongodb_data
    
    def mcmmp006_create_uniqueid(self, exception_data):
        # A function to create unique ids for exception data to put in mongodb
        
        for item in exception_data:
            transaction_id = str(item['mblnr'])
            document_number = str(item['ebeln'])
            material_document = str(item['belnr'])
            combined_key = transaction_id + '_'  + document_number + '_' + material_document
            item['uqid'] = combined_key
            
        return exception_data
    
    def mcmmp006_checkdb(self, exception_data):
        
        username = urllib.parse.quote_plus('SAPITSM')
        password = urllib.parse.quote_plus('Azureuser@123')

        # client = MongoClient("mongodb://sapitsm:haihello@123@20.204.119.18:27017")
        client = MongoClient('mongodb://%s:%s@127.0.0.1:27017' % (username, password))

        mydb = client["sapsample01"]

        mycol = mydb["mcmmp006"]
        
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
        file_name = 'mmp006_data.txt'        
        sds002_result = df.to_string(index = False)        
        self.utils.write_to_a_txt(sds002_result, file_name)
        # <----------------Attachement--------------------->
        
        # <--------- Generate ITSM header data ---------------------------->
        
        # A module to send json tickets to ITSM and EKS    
        output_list = []           
        
        print("Creating JSON ticket - MC_MM_P006")     
        
        # for value in data_list:
        json_skeleton = self.utils.read_json_file('/home/SAPITSM/finalsapdemo/config/itsec001/itsec001_schema.json')            
        json_skeleton['MANDT'] = '1002'
        json_skeleton['RFC'] = '100'
        json_skeleton['REQ_NO'] = '1000000097'
        json_skeleton['ALERT_SEND_DATE'] = self.utils.current_date()
        json_skeleton['ALERT_SEND_TIME'] = '12:05:2023'
        json_skeleton['EVENT_ID'] = 'MC_MM_P006'
        json_skeleton['EVENT_DESCRIPTION'] = 'Hide inventory by not fully receiving order but invoicing.'
        json_skeleton['PROGRAM_NAME'] = 'ZMC_MM_P006'
        json_skeleton['SEVERITY'] = 'HIGH'
        json_skeleton['RISK_DESCRIPTION'] = 'Hide inventory by not fully receiving order but invoicing.'
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
