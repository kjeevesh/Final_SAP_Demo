def itsec001_main(self):
        # Get the current date and time
        today = datetime.now
        # Format the date and time as a string in the format 'YYYYMMDD'
        formatted_date = today.strftime('%Y%m%d')
        rt_profile=["SAP_ALL","SAP_NEW","S_A.SYSTEM","S_A.ADMIN","S_A.CUSTOMIZ","S_A.DEVELOP","S_A.USER","S_USER.ALL","S_ABAP_ALL","S_RZL_ADMIN"]
        # Read data from txt files ust04.xlsx,usr02.xlsx, user_addr.xlsx
        #ust04=pd.read_excel("ust04.xlsx")
        #usr02=pd.read_excel("usr02.xlsx")
        #user_addr=pd.read_excel("user_addr.xlsx")

        # set the file path
        file_path1 = 'dummydata/itsec001/usr02.txt'
        file_path2 = 'dummydata/itsec001/ust04.txt'
        file_path3 = 'dummydata/itsec001/user_addr.txt'

        # read the data into a string
        with open(file_path1, 'r') as f1:
            data_02 = f1.read()
        with open(file_path2, 'r') as f2:
            data_04 = f2.read()
        with open(file_path3, 'r') as f3:
            data_addr = f3.read()

        # convert the string to a list of dictionaries
        data_usr02 = ast.literal_eval(data_02)
        data_ust04 = ast.literal_eval(data_04)
        data_useraddr = ast.literal_eval(data_addr)

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
        # display the DataFrame
        #print(dfaddr)
        #print(usr02.head())
        # start date and end date
        usr02= usr02[(usr02['gltgy'] <= formatted_date) & (usr02['gltgb'] >= formatted_date)]
        print("Len of usr02 > ", len(usr02))
        ust04_striped=df = ust04[ust04['profile'].isin(rt_profile)]
        print("Len of ust04 > ", len(ust04_striped))
        #print(ust04triped.tail())
        usr42=pd.merge(ust04_striped,usr02, on='bname')
        usr42_filtered=usr42[usr42['usty']=='A']
        # usr42_filtered contains merged df and only those rows tht have user type as A(dialog user)
        usr42_merged=pd.merge(usr42_filtered,useraddr, on='bname')
        # filtering out only those rows which have gltv value as <=today and gltb >=today
        #usr42_updated = usr42_merged[(usr42_merged['gltgy'] <= formatted_date) & (usr42_merged['gltgb'] >= formatted_date)]
        print(len(usr42_merged))
        print(usr42_merged)