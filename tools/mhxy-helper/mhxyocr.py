from PIL import ImageGrab
from aip import AipOcr

APP_ID = '16272528'
API_KEY = 'r2pTFSS81fsw2GouaUdZMTdY'
SECRET_KEY = 'XIkKfNpCjtLzzQ5KIdFxMkMFWWF5iicZ'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


ii = ImageGrab.grab((440, 150, 1035, 250))
ii.save('screen/ocr.bmp')
image = get_file_content('screen/ocrmsg.bmp')

res = client.general(image)

print(res)
print(type(res))
