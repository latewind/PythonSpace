#configFile.py
import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {'Name' : 'LateWind',
					  'Size' : 18
					}
config['EXTEND'] = {"COMPANY" : 'ECODE'}

with open('D:/StudyDoc/config.cfg','w') as f :
	config.write(f)

