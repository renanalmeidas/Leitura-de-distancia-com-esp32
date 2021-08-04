from os import name
from serial.tools.list_ports import comports
from ampy.files import Files
from ampy.pyboard import Pyboard
from time import sleep
from subprocess import run, Popen

# files = ['boot.py', 'main.py', 'extras.py', 'lista.json']
files = ['main.py']
if name == 'nt':
    tasklist = str(run(['tasklist'], capture_output=True, text=True).stdout).split('\n')
    for task in tasklist:
        if task.__len__() > 0:
            if task.split()[0] == 'putty.exe':
                Popen('powershell taskkill /IM putty.exe /f')

sleep(1)
serialPort = [port.device for port in comports() if port.vid == 4292 and port.pid == 60000][0] or 'COM3'

board = Pyboard(serialPort)

_files = Files(board)


sleep(1)
print('Parando o Script em execução no Esp32 .', end='')
board.serial.write(b'\x03')
sleep(1)
print('.', end='')
board.serial.write(b'\x03')
sleep(1)
print('.')
board.serial.write(b'\x03')
sleep(1)

print(f'Enviando {len(files)} arquivos para o Esp32')
for file in files:
    print(f'Enviado *{file}*')
    with open(file, 'rb') as f:
        _files.put(file, f.read())
        sleep(1)
print('Arquivos enviados, enviando sinal de "Soft reboot"', end='')
sleep(1)
print('..')
board.serial.write(b'\x03\x04')
sleep(1)
print('Abrindo o Putty')
Popen(f"powershell putty -serial {serialPort} -sercfg 115200,8,n,1,N")
