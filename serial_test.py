import serial

try:
    ser = serial.Serial('/dev/serial0', baudrate=57600, timeout=1)
    print("Serial port is open")
    ser.write(b'\xAA\x00\x00')  # Example command; replace with a command for your sensor
    response = ser.read(10)  # Adjust read length based on command
    print(f"Response: {response}")
except serial.SerialException as e:
    print(f"Serial port error: {e}")
