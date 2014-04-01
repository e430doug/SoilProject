from pyfirmata import Arduino, util
import time
import datetime

# Class for handling calls to the soil sensor.  

class SoilSensorValues(object):
   
   temperature = 0.0
   humidity = 0.0
   
   def __init__(self, board):
      '''Set up the board callbacks'''
      self.board = board
      self.board.add_cmd_handler(0x04, self.handleTemperature)  # Attach temperature handler.
      self.board.add_cmd_handler(0x05, self.handleHumidity)  # Attach humidity handler.
   
      self.temperature = 0.0
      self.temperatureSentinel = False
      self.humidity = 0.0
      self.humiditySentinel = False
      
   def getTemperature(self):
      ''' Make the asynchronous call synchronous. We set a sentinal value and wait until it becomes true.  In this naive version we will wait forever.'''
      self.temperatureSentinel = False
      board.send_sysex(0x04) # Send the temperature command.
      
      while not self.temperatureSentinel:
         time.sleep(0.01) # Sleep waiting for the value to come back.
          
      return self.temperature
      
   def getHumidity(self):
      ''' Make the asynchronous call synchronous. We set a sentinal value and wait until it becomes true.  In this naive version we will wait forever.'''
      self.humiditySentinel = False
      board.send_sysex(0x05) # Send the temperature command.
      
      while not self.humiditySentinel:
         time.sleep(0.01) # Sleep waiting for the value to come back.
          
      return self.humidity     
      
   def handleTemperature(self, *data):
      strRes = util.two_byte_iter_to_str(data[2:])
      self.temperature = float(strRes)
      self.temperatureSentinel = True
      
   def handleHumidity(self, *data):
      strRes = util.two_byte_iter_to_str(data[2:])
      self.humidity = float(strRes)
      self.humiditySentinel = True
   

def simpleFunc(s):
   print '{0:c}'.format(s)
   
def ToBytes(num):
   h = int(num/100)
   if (h > 0):
      num = num - (h*100)
      
   t = int(num/10)
   if (t > 0):
      num = num - (t*10)
      
   o = int(num)
   
   return([chr(h),chr(t),chr(o)])
   
def SetPixel(pixNum, R, G, B):
   bArray = []
   bArray.append(chr(pixNum)) # The pixel number
   bArray += ToBytes(R)
   bArray += ToBytes(G)
   bArray += ToBytes(B)
   
   return bArray
   
   

board = Arduino('/dev/ttyATH0', baudrate=115200)

valuesHandler = SoilSensorValues(board)



it = util.Iterator(board)

it.start() # Start getting data


#board.send_sysex(0x03, ['\x01', '\x00', '\x00', '\x00', '\x02', '\x05', '\x05', '\x00', '\x00', '\x00'])
#board.send_sysex(0x03, SetPixel(0, 255, 0, 255))
#print 'Have sent sysex'

#time.sleep(0.5)

import plotly


py = plotly.plotly("doug.durham", "j9ym75bpyi")

                    
layout = {
   'xaxis': {'title': 'Date'},
   'yaxis': {'title': 'Temperature'},
   'yaxis2': {'title': 'Humidity', 'overlaying':'y', 'side':'right'},
   'title': 'Soil Sensor'
   }
                                                                                                           

for i in range(6000):
   dateNow = datetime.datetime.now()
   tempNow = valuesHandler.getTemperature()
   humidNow = valuesHandler.getHumidity()

   tempDict = {
   'name': 'Temperature', # the "name" of this series is the Continent
   'x': [dateNow],
   'y': [tempNow],
   'type': 'scatter',
   'mode': 'lines',
   }
                    
   humidityDict = {
   'name': 'Humidity', # the "name" of this series is the Continent
   'x': [dateNow],
   'y': [humidNow],
   'yaxis':'y2',
   'type': 'scatter',
   'mode': 'lines',
   }
                                                                    
   py.plot([tempDict, humidityDict], layout=layout,
   filename='Test Soil plot kitchen', fileopt='extend',
   world_readable=True, width=1000, height=650)
   time.sleep(60)

board.exit()
