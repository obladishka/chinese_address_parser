# Chinese Address Parsing API

A RESTful API service for parsing addresses written in Chinese. API takes Chinese address as a string and return a 
json response with address divided to different parts, such as region, area, city, street, house, building and room.

## Installation

1. Clone the repository:
```commandline
git clone https://github.com/obladishka/chinese_address_parser.git
```
2. Rename .env.sample file to .env and fill in related data
3. Initialize database:
```commandline
python manage.py data_init
```
4. Start the server:
```commandline
python manage.py runserver
```
5. To use the API go to http://localhost:8000/


## Request structure
```commandline
params = {"address": "chinese address as str"}
url = "http://localhost:8000/"
response = requests.get(url, params=params)
```

## Response structure
```commandline
print(response)
>>> {
    "region": "some_region", # China province
    "area": "some_city", # City within the province
    "city": "some_district", # District-level objects (districts, sub-distrct, towns, villages, communities, residential quarters)
    "street": "some_street", # Street-level objects (roads, streets, sections, lanes)
    "house_num": "some_number", # House number
    "house_ex": "some_building", # House-level objects (yards, towers, buildings, units)
    "unit_num": "some_room" # Unit-level objects (floors, rooms)
}
```

## Examples
```commandline
url = "http://localhost:8000/"
params = {"address": "浙江省杭州市余杭区五常街道文一西路969号1幢6楼601室"}
response = requests.get(url, params=params)
print(response)
>>> {
    "region": "Zhejiang Province",
    "area": "杭州 City",
    "city": "余杭 District, 五常 Sub-District",
    "street": "文一西 Road",
    "house_num": "969 No.",
    "house_ex": "1 Building",
    "unit_num": "6 Floor, 601 Room"
}

params = {"address": "深圳市福田区深南大道中段2005号华润大厦"}
response = requests.get(url, params=params)
print(response)
>>> {
    "region": "",
    "area": "深圳 City",
    "city": "福田 District",
    "street": "深南 Street, 中 Section",
    "house_num": "2005 No.",
    "house_ex": "华润 Plaza",
    "unit_num": ""
}

params = {"address": "北京市海淀区北三环西路甲18号院4号楼2层2022"}
response = requests.get(url, params=params)
print(response)
>>> {
    "region": "Beijing",
    "area": "",
    "city": "海淀 District",
    "street": "北三环西 Road",
    "house_num": "",
    "house_ex": "甲18 Yard, 4 Building",
    "unit_num": "2 Floor, 2022"
}

params = {"address": "湖南省邵阳市隆回县六都寨镇朝阳村5组3段"}
response = requests.get(url, params=params)
print(response)
>>> {
    "region": "Hunan Province",
    "area": "邵阳 City",
    "city": "隆回 Country, 六都寨 Town, 朝阳 Village",
    "street": "",
    "house_num": "5 Group",
    "house_ex": "3段",
    "unit_num": ""
}

params = {"address": "浙江省东阳市横店影视产业试验区C1-001"}
response = requests.get(url, params=params)
print(response)
>>> {
    "region": "Zhejiang Province",
    "area": "东阳 City",
    "city": "横店影视产业 Experimental Zone",
    "street": "",
    "house_num": "C1-001",
    "house_ex": "",
    "unit_num": ""
}
```