import serial.tools.list_ports
from datetime import datetime
import csv
import os

# Memeriksa dan mencetak direktori kerja saat ini
print(f"Current working directory: {os.getcwd()}")

# Memeriksa dan mencetak daftar port yang tersedia
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []
for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 115200
serialInst.port = portVar

try:
    serialInst.open()
    print(f"Opened port {portVar}")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

# Membuka file CSV untuk menulis data
file_path = 'outputkaki.csv'
try:
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Data'])  # Menulis header CSV
        print("CSV file created and header written.")

        while True:
            if serialInst.in_waiting:
                packet = serialInst.readline()
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Timestamp format
                try:
                    data = packet.decode('utf-8').rstrip('\n')
                except UnicodeDecodeError:
                    try:
                        data = packet.decode('latin-1').rstrip('\n')
                    except UnicodeDecodeError as e:
                        data = f"Failed to decode: {e}"
                print(f"{timestamp} - {data}")
                writer.writerow([timestamp, data])  # Menulis data ke file CSV
                file.flush()  # Ensure data is written to the file
                print("Data written to CSV.")
except Exception as e:
    print(f"Error writing to CSV: {e}")

print(f"File path: {os.path.abspath(file_path)}")

