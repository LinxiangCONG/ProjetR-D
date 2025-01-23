from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
from flask_cors import CORS

cities = {
    "1" : {
        "city" : "normandie",
        "server" : "es1",
        "location" : (49.0677708, 0.3138532)
    },
    "2": {
        "city" : "bordeaux",
        "server": "es2",
        "location": (44.836151, -0.580816)
    },
    "3": {
        "city" : "toulouse",
        "server": "es3",
        "location": (43.604500, 1.444000)
    },
}

servers = {
    "cloudServer":{
        "720p" : "192.168.20.20",
        "1080p" : "192.168.20.20",
    },
    "es1" : {
        "720p" : "192.168.50.11",
        "1080p" : "192.168.60.11",
    },
    "es2": {
        "720p": "192.168.50.12",
        "1080p": "192.168.60.12",
    },
    "es3": {
        "720p": "192.168.50.13",
        "1080p": "192.168.60.14",
    },
}

cloud_server = "192.168.20.20"

resource = {
    "co2" : {
        "720p":{
            "co2_720p_000.ts":["cloudServer"],
            "co2_720p_001.ts":["cloudServer"],
            "co2_720p_002.ts":["cloudServer"],
            "co2_720p_003.ts":["cloudServer"],
            "co2_720p_004.ts":["cloudServer"],
            "co2_720p_005.ts":["cloudServer"],
            "co2_720p_006.ts":["cloudServer"],
            "co2_720p_007.ts":["cloudServer"],
            "co2_720p_008.ts":["cloudServer"],
            "co2_720p_009.ts":["cloudServer"],
            "co2_720p_010.ts":["cloudServer"],
            "co2_720p_011.ts":["cloudServer"],
            "co2_720p_012.ts":["cloudServer"],
            "co2_720p_013.ts":["cloudServer"],
            "co2_720p_014.ts":["cloudServer"],
            "co2_720p_015.ts":["cloudServer"],
            "co2_720p_016.ts":["cloudServer"],
            "co2_720p_017.ts":["cloudServer"],
            "co2_720p_018.ts":["cloudServer"],
            "co2_720p_019.ts":["cloudServer"],
            "co2_720p_020.ts":["cloudServer"],
            "co2_720p_021.ts":["cloudServer"],
            "co2_720p_022.ts":["cloudServer"],
            "co2_720p_023.ts":["cloudServer"]
        },
        "1080p":{
            "co2_1080p_000.ts":["cloudServer"],
            "co2_1080p_001.ts":["cloudServer"],
            "co2_1080p_002.ts":["cloudServer"],
            "co2_1080p_003.ts":["cloudServer"],
            "co2_1080p_004.ts":["cloudServer"],
            "co2_1080p_005.ts":["cloudServer"],
            "co2_1080p_006.ts":["cloudServer"],
            "co2_1080p_007.ts":["cloudServer"],
            "co2_1080p_008.ts":["cloudServer"],
            "co2_1080p_009.ts":["cloudServer"],
            "co2_1080p_010.ts":["cloudServer"],
            "co2_1080p_011.ts":["cloudServer"],
            "co2_1080p_012.ts":["cloudServer"],
            "co2_1080p_013.ts":["cloudServer"],
            "co2_1080p_014.ts":["cloudServer"],
            "co2_1080p_015.ts":["cloudServer"],
            "co2_1080p_016.ts":["cloudServer"],
            "co2_1080p_017.ts":["cloudServer"],
            "co2_1080p_018.ts":["cloudServer"],
            "co2_1080p_019.ts":["cloudServer"],
            "co2_1080p_020.ts":["cloudServer"],
            "co2_1080p_021.ts":["cloudServer"],
            "co2_1080p_022.ts":["cloudServer"],
            "co2_1080p_023.ts":["cloudServer"],
        }
    },
    "train" : {
        "720p":{
        "train_720p_000.ts":["cloudServer"],
        "train_720p_001.ts":["cloudServer"],
        "train_720p_002.ts":["cloudServer"],
        "train_720p_003.ts":["cloudServer"],
        "train_720p_004.ts":["cloudServer"],
        "train_720p_005.ts":["cloudServer"],
        "train_720p_006.ts":["cloudServer"],
        "train_720p_007.ts":["cloudServer"],
        "train_720p_008.ts":["cloudServer"],
        "train_720p_009.ts":["cloudServer"],
        "train_720p_010.ts":["cloudServer"],
        "train_720p_011.ts":["cloudServer"],
        "train_720p_012.ts":["cloudServer"],
        "train_720p_013.ts":["cloudServer"],
        "train_720p_014.ts":["cloudServer"],
        "train_720p_015.ts":["cloudServer"],
        "train_720p_016.ts":["cloudServer"],
        "train_720p_017.ts":["cloudServer"],
        "train_720p_018.ts":["cloudServer"],
        "train_720p_019.ts":["cloudServer"],
        "train_720p_020.ts":["cloudServer"],
        "train_720p_021.ts":["cloudServer"]
    },
        "1080p":{
        "train_1080p_000.ts":["cloudServer"],
        "train_1080p_001.ts":["cloudServer"],
        "train_1080p_002.ts":["cloudServer"],
        "train_1080p_003.ts":["cloudServer"],
        "train_1080p_004.ts":["cloudServer"],
        "train_1080p_005.ts":["cloudServer"],
        "train_1080p_006.ts":["cloudServer"],
        "train_1080p_007.ts":["cloudServer"],
        "train_1080p_008.ts":["cloudServer"],
        "train_1080p_009.ts":["cloudServer"],
        "train_1080p_010.ts":["cloudServer"],
        "train_1080p_011.ts":["cloudServer"],
        "train_1080p_012.ts":["cloudServer"],
        "train_1080p_013.ts":["cloudServer"],
        "train_1080p_014.ts":["cloudServer"],
        "train_1080p_015.ts":["cloudServer"],
        "train_1080p_016.ts":["cloudServer"],
        "train_1080p_017.ts":["cloudServer"],
        "train_1080p_018.ts":["cloudServer"],
        "train_1080p_019.ts":["cloudServer"],
        "train_1080p_020.ts":["cloudServer"],
        "train_1080p_021.ts":["cloudServer"]
    }
    }
}

geolocator = Nominatim(user_agent="geoapi")

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# 获取最近的closed server
def closedServer():
    global min_city, min_es
    city = "paris"
    location = geolocator.geocode(city)
    if location:
        city_ll = (location.latitude, location.longitude)
        min_ds = 100000000
        for key, value in cities.items():
            print(value.get("location"))
            distance = haversine(city_ll, value.get("location") , unit=Unit.KILOMETERS)
            if distance < min_ds:
                print("distance : ", distance, "; min_ds : ", min_ds)
                min_ds = distance
                min_city = value.get("city")
                min_es = value.get("server")

    return  min_es

# 获取缺失的部分
def get_missing_chunk(videoName, serverName):
    video = resource[videoName]
    video720 = video["720p"]
    video1080p = video["1080p"]
    missing_chunk = []

    for key, item in video720.items():
        if serverName not in item:
            missing_chunk.append(key)

    for key, item in video1080p.items():
        if serverName not in item:
            missing_chunk.append(key)

    print(resource) 
    return missing_chunk


# 获取可播放的 server ip
def getIP(videoName, quality):

    closed_server = closedServer()
    missing_chunk = get_missing_chunk(videoName, closed_server)
    if len(missing_chunk) == 0:
        return servers[closed_server][quality]
    else:
        for i in servers.keys():
            if len(get_missing_chunk(videoName, i)) == 0:
                return servers[i][quality]


@app.route('/information', methods=['POST'])
def information():
    data = request.get_json()
    filename = data['filename']

    closed_server = closedServer()
    missing_chunk = get_missing_chunk(filename, closed_server)

    video = resource[filename]
    video720 = video["720p"]
    video1080p = video["1080p"]
    for key, item in video720.items():
        if closed_server not in item:
            item.append(closed_server)
    for key, item in video1080p.items():
        if closed_server not in item:
            item.append(closed_server)

    return jsonify({"closed_server": closed_server, "missing_chunk": missing_chunk}), 200


@app.route('/IP', methods=['POST'])
def disponibleIP():
    data = request.get_json()
    filename = data['filename']
    quality = data['quality']
    ip = getIP(filename, quality)
    return jsonify({"ip": ip}), 200


if __name__ == '__main__':
    app.run(host='192.168.181.151', port=5000)
