from rfc_libraries import *

parser = Utilities()

# establish a connection to your SAP system
conn = pyrfc.Connection(
    ashost='10.31.101.161',
    sysnr='04',
    client='100',
    user='etd_alert',
    passwd='jan@1234'
)

lt_erev = conn.call(
    'RFC_READ_TABLE',
    QUERY_TABLE='EREV',
    DELIMITER='|',
    FIELDS=[{'FIELDNAME': 'FGUHR'}, {'FIELDNAME': 'EDOKN'}, {'FIELDNAME': 'FGDAT'}]
)['DATA']

print(lt_erev)