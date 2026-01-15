import requests, json, datetime
import mykeys

class SmartSystem:
    def __init__(self):
        # Initialise states of fields
        self.actualTemperature = 20     
        self.temperatures=[]			# Stores a list of temperature readings
        self.ActualLighting = 20
        self.LightLevels=[]			# Stores a list of Light readings
        self.times= []				# Stores a list of time the temperature and light readings were taken
        self.Target_Temp = 20
        self.isHeatingEnabled = True
        self.isBoilerOn = False
        self.Threshold_Ligthing= 20
        self.Is_Lighting_Enabled= True
        self.LampOn= False
        self.lastID = 0
        self.uploadData = {'api_key': mykeys.WRITE_KEY}
        self.timeOfLastPost = datetime.datetime(1970,1,1)   # Forces first post
        
    def updateFromIoT(self):			# Allows the desktop GUI to read data from the IoT platform
        response = requests.get('https://api.thingspeak.com/channels/' +
                         mykeys.CHANNEL_ID + '/feeds.json?api_key=' +
                         mykeys.READ_KEY + '&minutes=2').json()
        print(f"{len(response['feeds'])} received.")
        for feed in response['feeds']:
            
            if feed['entry_id'] > self.lastID:	         # Not seen this entry yet
                self.lastID = feed['entry_id']
                timestamp = datetime.datetime.fromisoformat(feed['created_at'].replace('Z', ''))
                # Skip empty feeds
                if feed['field2'] is not None:				# Boiler state Field       
                    self.isBoilerOn = (feed['field2'] == '1')
                    print("Boiler State:", self.isBoilerOn)
                if feed['field3'] is not None:				# Current tempreature field
                    temperature = int(feed['field3'])
                    self.actualTemperature=temperature		# updates current temperature
                    self.temperatures.append(temperature)	# Extends the list with a new reading
                    self.times.append(timestamp)			# Extends the list with a new time stamp
                    print("Actual Temperature:",self.actualTemperature)
                if feed['field7'] is not None:				# Lamp state field
                    self.LampOn = (feed['field7'] == '1')
                    print("Lamp State:", self.LampOn)
                if feed['field6'] is not None:				# current light field
                    Light= int(feed['field6'])
                    self.LightLevels.append(Light)			# Extends the list with a new reading
                    self.ActualLighting=Light		
                    print("Actual Light Level:",self.ActualLighting)
                print('State updated')					# Show new state data        
    def postData(self):			# Upload data from the GUI back to IoT platform
        if (datetime.datetime.now() - self.timeOfLastPost).total_seconds() < 5:	# Prevent from uploading to fast
            return False            # Fail if trying to repost too soon
        
        self.uploadData['field1'] = '1' if self.isHeatingEnabled else '0'
        self.uploadData['field4'] = str(self.Target_Temp)
        self.uploadData['field5'] = '1' if self.Is_Lighting_Enabled else '0'
        self.uploadData['field8'] = str(self.Threshold_Ligthing)
        response = requests.post('https://api.thingspeak.com/update.json',
                       headers={'Content-Type': 'application/json'},
                       data=json.dumps(self.uploadData))
        if response.status_code == 200 and response.json() != 0:
            print("Post operation successful")
            self.timeOfLastPost = datetime.datetime.now()
            return True
        else:
            return False
