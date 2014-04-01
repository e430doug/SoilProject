from pyfirmata import Arduino, util
import time

def simpleFunc(s):
   print '{0:c}'.format(s)

board = Arduino('/dev/ttyATH0', baudrate=115200)


board.add_cmd_handler(0x01, simpleFunc)

it = util.Iterator(board)

it.start() # Start getting data


board.send_sysex(0x01)

print 'Have sent sysex'

time.sleep(0.5)

board.exit()
