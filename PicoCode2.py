
# Requires valid WiFi and ThingSpeak credentials in mykeys module.
from machine import Pin, Timer, ADC
import network, time, urequests, json
import mykeys  				# Locally stored module contains WiFi and ThingSpeak keys

# Connect to WiFi network using credentials from mykeys
print("Connecting to WiFi.", end="")
wifi = network.WLAN(network.STA_IF) 			# Create WiFi network object
wifi.active(True)
wifi.connect(mykeys.SSID, mykeys.KEY) 		# Connect to specific WiFi network
while not wifi.isconnected():					# Wait until connected
    print(".", end="")
    time.sleep(0.25)
print(" Connected")

# Class to encapsulate all code associated with this application
class SmartHeaterPico:
    def __init__(self):
#         OUTPUT PINS
        self.Heating_Enabled_LED = Pin('GP19', Pin.OUT) 		# Create LED output Pin objects
        self.boilerLED  = Pin('GP18', Pin.OUT)
        self.LampLED = Pin('GP17',Pin.OUT)
        self.Lighting_Enabled_LED= Pin('GP16',Pin.OUT)
#         ANALOGUE INPUT PINS
        self.TempAdc = ADC('GP26')   				# Setup ADC0 as temperature input
        self.LightAdc = ADC('GP27')					# Setup ADC1 as light input
#         STATE VARIABLES
        self.Target_Temperature = 20
        self.Target_Light_Level = 60
        self.Is_Heating_Enabled =  True
        self.Is_Lighting_Enabled = True
#         THINGSPEAK                
        self.lastID = 0                             # Keeps track of fields already seen
        self.uploadData = {'api_key': mykeys.WRITE_KEY}
#         TIME CONTROL
        self.tmr = Timer(period=2000, callback=self.Update_System)
        self.timeSinceLastPost = 1000				# Counter to limit posting rate
        
        
        
    def Update_System(self,timer):
#         Read system Analogue Inputs
        New_Temperature = int(self.TempAdc.read_u16() / 397)			# Read temperature ADC
        New_Light_Level = int(self.LightAdc.read_u16() / 397)			# Read Light level ADC
        print(f"Current Temperature = {New_Temperature}\u00B0C | Target Temperature = {self.Target_Temperature}")   
        print(f"Current Light Level = {New_Light_Level} | Threshold Light Level= {self.Target_Light_Level}")
        if New_Temperature< self.Target_Temperature and self.Is_Heating_Enabled:
            Is_Boiler_ON=True
        else:
            Is_Boiler_ON=False
        if New_Light_Level< self.Target_Light_Level and self.Is_Lighting_Enabled:
            Is_Dark=True
        else:
            Is_Dark=False
#         Update outputs
        self.boilerLED.value(Is_Boiler_ON)
        self.LampLED.value(Is_Dark)

        
        
        
        
        response = urequests.get('https://api.thingspeak.com/channels/' +
                                mykeys.CHANNEL_ID + '/feeds.json?api_key=' +
                                mykeys.READ_KEY + '&minutes=2').json()
        print(f"{len(response['feeds'])} feeds received.")
        for feed in response['feeds']:
            if feed['entry_id'] > self.lastID:	    	# Not seen this entry yet
                self.lastID = feed['entry_id']
#                 Temperature Update
                if feed['field1'] is not None:			# Skip empty feeds
                    self.Is_Heating_Enabled = (feed['field1']== '1')
                    self.Heating_Enabled_LED.value(self.Is_Heating_Enabled)
                if feed['field4'] is not None:
                    self.Target_Temperature = int(feed['field4'] )
#                 Light Level Update        
                if feed['field5'] is not None:			# Skip empty feeds
                    self.Is_Lighting_Enabled = (feed['field5']== '1')
                    self.Lighting_Enabled_LED.value(self.Is_Lighting_Enabled)
                if feed['field8'] is not None:
                    self.Target_Light_Level=int(feed['field8'])
                print("System Updated")
        self.timeSinceLastPost = self.timeSinceLastPost + 2
          
#         Upload New DATA after a given time           
        if self.timeSinceLastPost >30:
#             Heating Data Upload
            
            self.uploadData['field2'] = '1' if Is_Boiler_ON else '0'
            self.uploadData['field3'] = New_Temperature
#             Lighting Data Upload
            self.uploadData['field7'] = '1' if Is_Dark else '0'
            self.uploadData['field6'] = New_Light_Level
            
            
            response = urequests.post('https://api.thingspeak.com/update.json',
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(self.uploadData))              
            if response.status_code == 200 and response.json() != 0:
                print("Post operation succesful")
                self.timeSinceLastPost=0
                      
            
sh = SmartHeaterPico()
