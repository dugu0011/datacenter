from ncclient import manager
import os.path
 
# path = "d:/temp/"
# filename = os.path.join(path, "config.xml")
m = manager.connect(host='192.168.159.10', port='830', username='admin', password='admin', hostkey_verify=False, device_params={'name':'csr'})
tmp = m.get_config(source='running').data_xml
print(tmp)
# f = open(filename, "w")
# f.write(tmp)
# f.close()