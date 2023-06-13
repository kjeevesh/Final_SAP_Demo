import pyrfc

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
lt_erev = conn.call(
    'RFC_READ_TABLE',
    QUERY_TABLE='EREV',
    DELIMITER='|',
    FIELDS=[{'FIELDNAME': 'BSTYP'}, {'FIELDNAME': 'EDOKN'}, {'FIELDNAME': 'FGDAT'}],
    OPTIONS=[{'TEXT': "FGDAT IN ('" + "','".join(it_date) + "') AND BSTYP = 'F'"}]
)['DATA']


i = 0
po_list = []

for values in range(len(lt_erev)):
    data_to_add = lt_erev[i]['WA']
    data_split = data_to_add.split("|")
    po_list.append(data_split)
    i = i + 1

print(len(lt_erev))

# print the data
print(lt_erev)
print(po_list)