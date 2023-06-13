from utils.sap_itsm_utils import *

parser = Utilities()

# establish a connection to your SAP system
conn = pyrfc.Connection(
    ashost='10.31.101.161',
    sysnr='04',
    client='100',
    user='etd_alert',
    passwd='jan@1234'
)

# define the input parameter for the function module
it_date = ['20230205']

# execute the function module and fetch the data into a Python variable
# lt_erev = conn.call(
#     'RFC_READ_TABLE',
#     QUERY_TABLE='EREV',
#     DELIMITER='|',
#     FIELDS=[{'FIELDNAME': 'BSTYP'}, {'FIELDNAME': 'EDOKN'}, {'FIELDNAME': 'FGDAT'}, {'FIELDNAME': 'FGNAM'}]
# )['DATA']

# lt_ekko = conn.call(
#     'RFC_READ_TABLE',
#     QUERY_TABLE='EKKO',
#     DELIMITER='|',
#     FIELDS=[{'FIELDNAME': 'ERDAP'}, {'FIELDNAME': 'EBELN'}, {'FIELDNAME': 'BUKRS'}, {'FIELDNAME': 'BSTYP'}, {'FIELDNAME': 'AEDAT'}, {'FIELDNAME': 'ERNAM'}, {'FIELDNAME': 'LIFNR'}, {'FIELDNAME': 'EKORG'}, {'FIELDNAME': 'EKGRP'}, {'FIELDNAME': 'RESWK'}, {'FIELDNAME': 'KTWRT'}, {'FIELDNAME': 'FRGGR'}, {'FIELDNAME': 'FRGSX'}, {'FIELDNAME': 'FRGKE'}, {'FIELDNAME': 'LOEKZ'}],
#     OPTIONS=[{'TEXT': "AEDAT IN ('" + "','".join(it_date) + "')"}]
# )['DATA']

# lt_ekko = conn.call(
#     'RFC_READ_TABLE',
#     QUERY_TABLE='EKKO',
#     DELIMITER='|',
#     FIELDS=[{'FIELDNAME': 'EBELN'}, {'FIELDNAME': 'BUKRS'}, {'FIELDNAME': 'BSTYP'}, {'FIELDNAME': 'AEDAT'}, {'FIELDNAME': 'ERNAM'}, {'FIELDNAME': 'LIFNR'}, {'FIELDNAME': 'EKORG'}, {'FIELDNAME': 'EKGRP'}, {'FIELDNAME': 'RESWK'}, {'FIELDNAME': 'KTWRT'}, {'FIELDNAME': 'FRGGR'}, {'FIELDNAME': 'FRGSX'}, {'FIELDNAME': 'FRGKE'}, {'FIELDNAME': 'LOEKZ'}]
# )['DATA']

lt_erev_1 = conn.call(
    'RFC_READ_TABLE',
    QUERY_TABLE='RBKP',
    DELIMITER='|',
    FIELDS=[{'FIELDNAME': 'BUKRS'}, {'FIELDNAME': 'BELNR'}, {'FIELDNAME': 'GJAHR'}, {'FIELDNAME': 'BLART'}, {'FIELDNAME': 'BLDAT'},{'FIELDNAME': 'BUDAT'}, {'FIELDNAME': 'USNAM'}, {'FIELDNAME': 'RBSTAT'}]
)['DATA']

lt_erev_2 = conn.call(
    'RFC_READ_TABLE',
    QUERY_TABLE='RSEG',
    DELIMITER='|',
    FIELDS=[{'FIELDNAME': 'EBELN'}, {'FIELDNAME': 'MATNR'}, {'FIELDNAME': 'BUKRS'}, {'FIELDNAME': 'BELNR'}, {'FIELDNAME': 'GJAHR'}]
)['DATA']

lt_erev_3 = conn.call(
    'RFC_READ_TABLE',
    QUERY_TABLE='EKBE',
    DELIMITER='|',
    FIELDS=[{'FIELDNAME': 'EBELN'}, {'FIELDNAME': 'BELNR'}, {'FIELDNAME': 'GJAHR'}]
)['DATA']

lt_erev_4 = conn.call(
    'RFC_READ_TABLE',
    QUERY_TABLE='MKPF',
    DELIMITER='|',
    FIELDS=[{'FIELDNAME': 'USNAM'}, {'FIELDNAME': 'MBLNR'}, {'FIELDNAME': 'MJAHR'}]
)['DATA']

print(lt_erev_4)

# parser.write_to_a_txt(str(lt_erev_1), "rbkp.txt")
# parser.write_to_a_txt(str(lt_erev_2), "rseg.txt")
# parser.write_to_a_txt(str(lt_erev_3), "ekbe.txt")
# parser.write_to_a_txt(str(lt_erev_3), "mkpf.txt")

# print(lt_erev_1)
# print(lt_erev_2)
# print(lt_erev_3)

# parser.write_to_a_txt(str(lt_erev), "erev.txt")
# parser.write_to_a_txt(str(lt_ekko), "ekko.txt")

# py_erev = parser.convert_wa_to_list(lt_erev)
# py_ekko = parser.convert_wa_to_list(lt_ekko)

# json_skeleton = parser.read_json_file('rfc_format.json')

# out_data = py_ekko[0]

# # ['0001', '4500001665', '20230205', 'ANSHULA']

# json_skeleton[0]['MANDT'] = out_data[0]
# json_skeleton[0]['REQ_NO'] = out_data[1]
# # json_skeleton[0]['ALERT_SEND_DATE'] = out_data[2]
# json_skeleton[0]['RISK_OWNER'] = out_data[3]

# print(json_skeleton)

# r = requests.post('http://20.204.135.69:7777/Ticket/API/Create_Ticket', json = json_skeleton)
# print(f"Status Code: {r.status_code}, Response: {r.json()}")