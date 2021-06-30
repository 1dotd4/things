# Telaire T6613/6615 UART util
import serial
from datetime import datetime

flag = 'ff'
address = 'fe'

def gen_cmd_packet(cmd, add=''):
    l = len(cmd + add) // 2
    if l > 0xff:
       raise Error('length ' + l + ' is not accepted for command ' + cmd)
    length = hex(len(cmd + add) // 2)[2:].zfill(2)
    fcmd = flag + address + length + cmd + add
    return bytes.fromhex(flag + address + length + cmd + add)

# loopback
# This commadn is used strictly for testing.
# The data_bytes (up to 16 bytes) following the \x00 command
# are echoed back in reposnse packet.
loopback_cmd = '00'

loopback_test = gen_cmd_packet(loopback_cmd, '010203')

# Read a status byte from the sensor.
# The status byte indicates whether the sensor
# is functioning, and is measuring PPM concentrations.
# The response is a single byte, <status>, of bitflags.
# (Note: bit 0 is the LSB.)
status_cmd = gen_cmd_packet('b6')
status_response_normal = 'fffa0100'
status_response_warmup = 'fffa0102'
status_response_calibr = 'fffa0104'

# Read the gas ppm as measured by the sensor.
# Response is a 2-byte binary value giving the ppm.
read_cmd = '02'
serial_reg = '01'
gas_ppm_reg = '03'
compile_date_reg = '0c'
compile_subvol_reg = '0d'
elevation_reg = '0f'

# Upon power-up, some sensor models start streaming
# gas concentration data out the UART.
# For other sensor models, data streaming occurs only
# when the command CMD_STREAM_DATA is given. In either case,
# the data stream is either two or three bytes, depending
# upon the sensor model. If any UART command is sent
# to a sensor while streaming data, the data streaming is stopped.
# In order to resume data streaming, command CMD_STREAM_DATA should be given.
# If command CMD_STREAM_DATA is given while a sensor
# is streaming data, it will stop and then restart streaming data.
stream_cmd = 'bd'
# Start streaming gas concentration data after each data collection cycle.
# Reponse:
# The response data stream is either 2 or 3 bytes, depending upon sensor model.
# If two bytes are returned, the format is <msb, lsb>.
# For models returning three bytes, the data is the actual ppm in the format <msb, mid, lsb >.
# In all formats, the data is non-negative and bounded.

def readSerial(s):
    flag   = s.read()
    addr   = s.read()
    length = s.read()
    res = b''
    for _ in range(int(length.hex())):
        res += s.read()
    return flag.hex() + addr.hex() + length.hex() + res.hex()

def convertInt(s):
    return int(s[6:], 16)

#open('/dev/ttyUSB0', 'rw') as s:
#s.send(loopback)
with serial.Serial('/dev/ttyUSB0', 19200, timeout=.1) as s:
    s.write(loopback_test)
    assert readSerial(s) == 'fffa03010203'
    s.write(status_cmd)
    assert readSerial(s) == 'fffa0100'
    s.write(gen_cmd_packet(read_cmd, gas_ppm_reg))
    print('ppm: ' + str(convertInt(readSerial(s))), flush=True)
    s.write(gen_cmd_packet(stream_cmd))
    while True:
        i = s.read(5)       
        if i != b'':
            print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                '-',
                int(datetime.now().timestamp()),
                '-',
                convertInt(i.hex()), flush=True)
