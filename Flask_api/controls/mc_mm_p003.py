from utils.sap_itsm_utils import *
from utils.text_to_json_util import *

class MC_MM_P003(object):
    
    def __init__(self) -> None:
        
        self.utils = Utilities()
        
        creds_fileName = "/home/SAPITSM/finalsapdemo/config/sap_cred.json"
        self.rfc_creds = self.utils.read_json_file(creds_fileName)
    
    def p003Execute(self):
        
        exc_data = self.l1_mcmmp003()
        
        p003_jsondata = self.convert_df_to_json(exc_data)
        
        print("mcmmp003 json data --> ", p003_jsondata)
        
        p003_uniqueid = self.mcmmp003_create_uniqueid(p003_jsondata)
        
        print("uqid --> ", p003_uniqueid)
        
        check_db = self.mcmmp003_checkdb(p003_uniqueid)
        
        return
    
    def l1_mcmmp003(self):
        
        # ["banfn","bsart","werks","lgort","ernam","bnfpo","badat"]        
        eban_fields = ['BANFN', 'BSART', 'WERKS', 'LGORT', 'ERNAM', 'BNFPO', 'BADAT']
        eban_options = []
        
        # ["ebeln","banfn","bnfpo"]        
        ekpo_fields = ['EBELN', 'BANFN', 'BNFPO']
        ekpo_options = []
        
        # ["ebeln","aedat","ernam","redn","bstyp"]        
        ekko_fields = ['EBELN', 'AEDAT', 'ERNAM', 'BSTYP']
        ekko_options = []
        
        # read the environment variable
        env_var = os.environ["Deployment"]
        
        # Check if the deployment is for dev or for prod        
        if env_var == 'DEV' :
            # set the file path
            print("--------------------- Accessing JSON files ---------------------")
            
            file_path1 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_mm_p003/eban.json'
            file_path2 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_mm_p003/ekpo.json'
            file_path3 = '/home/SAPITSM/finalsapdemo/Flask_api/dummydata/mc_mm_p003/ekko.json'        

            # read the json data
            with open(file_path1, 'r') as f1:
                data_eban = json.load(f1)
            with open(file_path2, 'r') as f2:
                data_ekpo = json.load(f2)
            with open(file_path3, 'r') as f3:
                data_ekko = json.load(f3)
        
        elif env_var == 'PROD' :
            # get the data from SAP table            
            print("------------------------Accessing SAP server------------------------")
        
            data_eban = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EBAN', eban_fields, eban_options)['DATA']        
            data_ekpo = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EKPO', ekpo_fields, ekpo_options)['DATA']        
            data_ekko = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'EKKO', ekko_fields, ekko_options)['DATA']        


        # create a pandas DataFrame from the list of dictionaries
        for i in range(3):
            if i==0:
                eban=pd.json_normalize(data_eban)
                #rbkp = pd.DataFrame(data_rbkp)
                eban[["banfn","bsart","werks","lgort","ernam","bnfpo","badat"]] = eban['WA'].str.split('|', expand=True)
                eban=eban.drop("WA",axis=1)
            elif i==1:
                ekpo=pd.json_normalize(data_ekpo)
                ekpo[["ebeln","banfn","bnfpo"]] = ekpo['WA'].str.split('|', expand=True)
                ekpo=ekpo.drop("WA",axis=1)
            else:
                ekko=pd.json_normalize(data_ekko)
                ekko[["ebeln","aedat","ernam","redun","bstyp"]] = ekko['WA'].str.split('|', expand=True)
                ekko=ekko.drop("WA",axis=1)
                ekko=ekko[(ekko["aedat"]>'20220901') & (ekko['aedat']<'20220930')]
        
        result1=pd.merge(eban,ekpo, on=["banfn","bnfpo"], how="inner")
        result2 = ekko
        result2 = result2.loc[result2['ebeln'].isin(result1['ebeln'])]
        result2 = result2[result2['bstyp'] == 'F']
        lt_output = []
        
        if len(result1)>0 and len(result2)>0:
            
            for _, ls_eban in result1.iterrows():
                for _, ls_ekko in result2.iterrows():
                        if (ls_eban.loc["ebeln"] == ls_ekko.loc["ebeln"]) & (ls_eban.loc["ernam"] == ls_ekko.loc["ernam"]):
                            ls_final = {
                            "aedat":   ls_ekko.loc["aedat"],
                            "ebeln":   ls_ekko.loc["ebeln"],
                            "ernam_m": ls_ekko.loc["ernam"],
                            "banfn":   ls_eban.loc["banfn"],
                            "bsart":   ls_eban.loc["bsart"],
                            "werks":   ls_eban.loc["werks"],
                            "lgort":   ls_eban.loc["lgort"],
                            "ernam":   ls_eban.loc["ernam"]
                            }
                
                            lt_output.append(ls_final)
                            
        lt_output = pd.DataFrame(lt_output)
        
        lt_output=lt_output.sort_values(["ebeln","ernam_m"], ascending=True)
        lt_output=lt_output.drop_duplicates(keep="first")
        
        #var1=lt_output.to_excel("lt_output.xlsx",index=False)
        print("----------03--> MC_MM_P003------------------------------------------------------")
        print("Final exceptions filtered length is > ", len(lt_output))      
        
        return lt_output
    
    def convert_df_to_json(self, exception_data):
        
        # Step 1 :  Generate a dataframe variable        
        mongo_df = pd.DataFrame(exception_data)
        
        # Step 2 : convert dataframe into json
        # orient = 'records' to get an o/p of list of dictionaries.
        mongodb_data = mongo_df.to_dict(orient='records')
        
        return mongodb_data
    
    def mcmmp003_create_uniqueid(self, exception_data):
        # A function to create unique ids for exception data to put in mongodb
        
        for item in exception_data:
            banfn = str(item['banfn'])
            ebeln = str(item['ebeln'])
            ernam_m = str(item['ernam_m'])
            combined_key = banfn + '_' + ebeln + '_'  + ernam_m
            item['uqid'] = combined_key
            
        return exception_data
    
    def mcmmp003_checkdb(self, exception_data):
        
        username = urllib.parse.quote_plus('SAPITSM')
        password = urllib.parse.quote_plus('Azureuser@123')

        # client = MongoClient("mongodb://sapitsm:haihello@123@20.204.119.18:27017")
        client = MongoClient('mongodb://%s:%s@127.0.0.1:27017' % (username, password))

        mydb = client["sapsample01"]

        mycol = mydb["mcmmp003"]
        
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
        file_name = 'mmp003_data.txt'        
        sds002_result = df.to_string(index = False)        
        self.utils.write_to_a_txt(sds002_result, file_name)
        # <----------------Attachement--------------------->
        
        # <--------- Generate ITSM header data ---------------------------->
        
        # A module to send json tickets to ITSM and EKS    
        output_list = []           
        
        print("Creating JSON ticket - MC_MM_P003")     
        
        # for value in data_list:
        json_skeleton = self.utils.read_json_file('/home/SAPITSM/finalsapdemo/config/itsec001/itsec001_schema.json')            
        json_skeleton['MANDT'] = '1002'
        json_skeleton['RFC'] = '100'
        json_skeleton['REQ_NO'] = '1000000096'
        json_skeleton['ALERT_SEND_DATE'] = self.utils.current_date()
        json_skeleton['ALERT_SEND_TIME'] = '12:05:2023'
        json_skeleton['EVENT_ID'] = 'MC_MM_P033'
        json_skeleton['EVENT_DESCRIPTION'] = 'Requisition an item and create a PO from that requisition.'
        json_skeleton['PROGRAM_NAME'] = 'ZMC_MM_P033'
        json_skeleton['SEVERITY'] = 'MEDIUM'
        json_skeleton['RISK_DESCRIPTION'] = 'Requisition an item and create a PO from that requisition'
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
