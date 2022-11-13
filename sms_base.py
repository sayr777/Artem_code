import socket
import pyotp
import os
# import dotenv
# dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
# dotenv.load_dotenv(dotenv_path)

# SERV_HOST = os.environ.get('SERV_HOST')    # имя сервера
# SERV_PORT = os.environ.get('SERV_PORT')    # порт

# Генерация OTP
def generate_OTP ():
    totp = pyotp.TOTP('base32secret3232')
    return totp.now()[-4:]

# Отправить otp и получить ответ от сервера
def rec_otp (PHONE_NUM):
    # СоздаемTCP/IP сокет
    otp_sms = generate_OTP()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Подключаем сокет к порту, через который прослушивается сервер
    server_address = ('86.62.74.178', 8001)
    print('Подключено к {} порт {}'.format(*server_address))
    sock.connect(server_address)
    try:
        # Отправка данных
        message = ",".join([PHONE_NUM,otp_sms])
        print(f'Отправляется: {message}')
        sock.sendall((message).encode())
        # Смотрим ответ
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f'Получено: {data.decode()}')
    finally:
        print('Закрываем сокет')
        sock.close()
    return data.decode()[-4:]

