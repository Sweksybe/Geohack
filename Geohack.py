import json
import subprocess
import time
import webbrowser

import pyperclip
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from seleniumwire.utils import decode as sw_decode

#change the openchrome path

subprocess.Popen(['python', 'path_to_openchrome.py'])

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9123")
#Change chrome driver path accordingly
sw_options = {
    'port': 12345
}
#cmd: chrome.exe --remote-debugging-port=9123 --proxy-server=localhost:12345
chrome_driver = "C:\\Users\\Gebruiker\\Documents\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options,seleniumwire_options=sw_options)
print(driver.title)
previous = []

coords = ""


def interceptor(request):
    if "lat" in str(request.body):
        splitcoords = coords.split(",")
        print("split1" + splitcoords[0])
        print("split2" + splitcoords[1])
        existing_payload = json.loads(request.body.decode('utf-8'))

        # Modify the payload - example: changing a key's value
        if 'lat' in existing_payload:
            existing_payload["lat"] = float(splitcoords[0])
            existing_payload["lng"] = float(splitcoords[1])

        request.headers['Content-Type'] = 'application/json'
        request.headers['X-Client'] = 'web'

        # Encode the modified payload back to JSON
        request.body = json.dumps(existing_payload).encode('utf-8')
        print("coords:" + coords)
        print(request.body)
x = 0
while True:
    for request in driver.requests:
        if "GeoPhotoService.GetMetadata" in request.url:
            if request.response:
                data = sw_decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                data = data.decode("utf8")
                input_string = data[:1700]
                start_index = input_string.find('Google"]]]]')
                if data[:1700].find('Google"]]]]') != -1:
                    # Find the first "end" after "start"
                    first_end_index = input_string.find("],[", start_index)
                    if first_end_index != -1:
                        # Find the second "end" after the first "end"
                        second_end_index = input_string.find("],[", first_end_index + len("],["))
                        if second_end_index != -1:
                            # Find the third "end" after the second "end"
                            third_end_index = input_string.find("],[", second_end_index + len("],["))
                            if third_end_index != -1:
                                # Extract the substring between "start" and the third "end"
                                result = input_string[start_index + len('Google"]]]]'):third_end_index]
                                if str(result) in previous:
                                    continue
                                else:
                                    print(result[19:])
                                    resultcoord = result[19:]
                                    coords = resultcoord
                                    splitcoords = coords.split(",")
                                    print("split1" + splitcoords[0])
                                    latitude = splitcoords[0]
                                    print("split2" + splitcoords[1])
                                    longitude = splitcoords[1]
                                    if x == 0:
                                        webbrowser.open(f'https://www.google.com/maps/search/{latitude},{longitude}/@{latitude},14z?entry=ttu')
                                        x = 1
                                    elif x != 0:
                                        time.sleep(45)
                                        x = 0
                                    pyperclip.copy(resultcoord)
                                    previous.append(str(result))
                            else:
                                print("The third 'end' not found in the string.")
                        else:
                            print("The second 'end' not found in the string.")
                    else:
                        print("The first 'end' not found in the string.")
                else:
                    print("The 'start' not found in the string.")
                time.sleep(2)
    continue
