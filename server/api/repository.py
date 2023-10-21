import requests

access_token = ''
resource_headers = {}
base_url = "https://api.baubuddy.de/dev/index.php/v1"
color_codes = {}

def getToken():
    auth_headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
    }
    payload = {
    "username": "365",
    "password": "1"
    }
    response = requests.request("POST", "https://api.baubuddy.de/index.php/login", json=payload, headers=auth_headers)
    if response.status_code >= 300:
        pass #raise error
    global access_token
    access_token = response.json()['oauth']['access_token']
    global resource_headers
    resource_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    return True

def getResource(url):
    if access_token or getToken():
        response = requests.request("GET", url , headers=resource_headers)
        if response.status_code == 401:
            getToken()
            return getResource(url)
        else:
            return response.json()

def getActiveVehicles():
    return getResource(f"{base_url}/vehicles/select/active")

def getLabels():
    return getResource(f"{base_url}/labels")

def getColorCode(ids):
    if ids == None : return ids
    ids = str(ids).split(',')

    def get_code(id):
        c = color_codes.get(id, None)
        return c or fetchCode(id)

    def fetchCode(id):
        try:
            item =  getResource(f"{base_url}/labels/{id}")[0].get('colorCode', False)
        except Exception as e:
            item = 'error'
        if item:
            global color_codes
            color_codes[id]=item
        return item

    codes = ""
    for id in ids:
        codes += f"{get_code(id)} "
    return codes.strip()


def init():
    global color_codes
    lbs = getLabels()
    for lbl in lbs:
        c1 = lbl.get('colorCode', False)
        children = lbl.get('children', [])
        if c1:
            color_codes[str(lbl['id'])] = c1
        for child in children:
            c2 = child.get('colorCode', False)
            if c2:
                color_codes[str(child['id'])] = c2

init()