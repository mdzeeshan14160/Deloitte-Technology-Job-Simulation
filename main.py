import json
import unittest
import datetime
with open("./data-1.json","r",encoding="utf-8") as f1:
    jsonData1=json.load(f1)
with open("./data-2.json","r",encoding="utf-8")as f2:
    jsonData2=json.load(f2)
with open("./data-result.json","r",encoding="utf-8")as res:
    dataresult=json.load(res)
def convertFromFormat1(jsonObject):
    locationParts = jsonObject["location"   ].split("/")
    result={
        "deviceID":jsonObject["deviceID"],
        "deviceType":jsonObject["deviceType"],
        "timestamp":jsonObject["timestamp"],
        "location":{
            "country":locationParts[0],
            "city":locationParts[1],
            "area":locationParts[2],
            "factory":locationParts[3],
            "section":locationParts[4]
        },
        "data":{
            "status":jsonObject["operationStatus"],
            "temperature":jsonObject["temp"]
        }
        }
    return result
def main(jsonObject):
    result={}
    if(jsonObject.get("device")==None):
        result=convertFromFormat1(jsonObject)
    else:
        result=convertFromFormat2(jsonObject)
    return result
def convertFromFormat2(jsonObject):
    data=datetime.datetime.strptime(jsonObject["timestamp"],"%Y-%m-%dT%H:%M:%S.%fZ")
    difference = (data - datetime.datetime(1970, 1, 1)).total_seconds()
    milliseconds=difference*1000
    timestamp = round(milliseconds)
    result = {
    "deviceID": jsonObject["device"]["id"],
    "deviceType": jsonObject["device"]["type"],
    "timestamp": timestamp,
    "location": {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"],
        "factory": jsonObject["factory"],
        "section": jsonObject["section"]
    },
    "data": {
        "status": jsonObject["data"]["status"],
        "temperature": jsonObject["data"]["temperature"]
    }
    }
    return result
class TestSolution(unittest.TestCase):
    def test_sanity(self):
        result = json.loads(json.dumps(dataresult))
        self.assertEqual(result, dataresult) 
    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, dataresult, "Converting from Type 1 failed")
    def test_dataType2(self):
        result=main(jsonData2)
        self.assertEqual(result,dataresult,"Converting from Type 2 failed")
if __name__ == '__main__':
    unittest.main()