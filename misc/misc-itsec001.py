def l1():
    def l1_date_filtering(self):
        
        # Get the current date and time in YYYYMMDD format
        today = datetime.now()
        
        # ["bname","usty","gltgy","gltgb"]        
        usr02_fields = ['BNAME', 'USTYP', 'GLTGV', 'GLTGB']
        usr02_options = []
        # ["bname","profile"]
        ust04_fields = ['BNAME', 'PROFILE']
        ust04_options = []
        # [["bname","fullname"]]
        user_addr_fields = ['BNAME', 'NAME_TEXTC']
        user_addr_options = []
        
        # usr02_data = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'USR02', usr02_fields, usr02_options)['DATA']
        # usr02_list = self.utils.convert_wa_to_list(usr02_data)
        usr02_list = TextToJson("dummydata/itsec001/usr02.json").text_to_json()
        usr02_list = self.utils.convert_wa_to_list(usr02_list)
        
        # ust04_data = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'UST04', ust04_fields, ust04_options)['DATA']
        # ust04_list = self.utils.convert_wa_to_list(ust04_data)
        ust04_list = TextToJson("dummydata/itsec001/ust04.json").text_to_json()
        ust04_list = self.utils.convert_wa_to_list(ust04_list)
        
        # user_addr_data = self.utils.get_rfc_read_table_for_fields(self.rfc_creds, 'USER_ADDR', user_addr_fields, user_addr_options)['DATA']
        # user_addr_list = self.utils.convert_wa_to_list(user_addr_data)
        user_addr_list = TextToJson("dummydata/itsec001/user_addr.json").text_to_json()
        user_addr_list = self.utils.convert_wa_to_list(user_addr_list)
        
        # First filtering - filter lists from ust04 for data relevant to our profiles list
        profile_names = self.profile_names
        
        filtered_profiles_perName = []
        
        for sublist in ust04_list:
            for value in profile_names:
                if value in sublist:
                    filtered_profiles_perName.append(sublist)
                    break
        
        # Second filtering - filter lists from ust02 for data based on today's date                
        filtered_profiles_perDate = []
        
        for lst in usr02_list:
            if lst[2] != '00000000' and lst[3] != '00000000':
                start_date = datetime.strptime(lst[2], '%Y%m%d')
                end_date = datetime.strptime(lst[3], '%Y%m%d')
                if start_date <= today <= end_date:
                    filtered_profiles_perDate.append(lst)
                    
        # remove duplicates from the list - Checking
        unique_list = []
        for sublist in filtered_profiles_perDate:
            if sublist not in unique_list:
                unique_list.append(sublist)
        
        # Third filtering - Merging usr02 and ust04 baased on 'bname' parameter
        filtered_perBname = []
        
        for lst1 in filtered_profiles_perName:
            for lst2 in filtered_profiles_perDate:
                if lst1[0].strip() == lst2[0].strip():
                    filtered_perBname.append(lst1 + lst2[1:])
                    break
        
        final_list = []
        
        for lst1 in filtered_perBname:
            if lst1[2] == 'A':
                final_list.append(lst1)
        
        # filtering based on bname from user_addr table
        # Third filtering - Merging usr02 and ust04 baased on 'bname' parameter
        filtered_perBname_1 = []
        
        for lst1 in final_list:
            for lst2 in user_addr_list:
                if lst1[0].strip() == lst2[0].strip():
                    filtered_perBname_1.append(lst1 + lst2[1:])
                    break
        
        print("----------02--> ITSEC_001------------------------------------------------------")
        
        # print("UST04 Before filtering > ", len(ust04_list)) # 24347
        # print("UST04 After filtering > ", len(filtered_profiles_perName)) # 1467
        
        # print("USR02 Before filtering > ", len(usr02_list)) # 1011
        # print("USR02 After filtering > ", len(unique_list)) # 23
            
        # print("Filtered based on BNAME > ", len(filtered_perBname)) # 24
        # print("Filtered by BSTYP = A > ", len(final_list)) # 20
        
        print("Final exceptions filtered length is > ",len(filtered_perBname_1)) # 20
        
        return filtered_perBname_1