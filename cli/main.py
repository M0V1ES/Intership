import argparse
import socket
from HTTPResponse import HTTPResponse
from HTTPRequest import HTTPRequest
from config import config
import logging

# Создаем параметры для командной строки
parser = argparse.ArgumentParser(description="CLI-приложение для отправки SMS в API")
parser.add_argument("your_tel", type=str, help="Введите ваш телефон")
parser.add_argument("req_tel", type=str, help="Введите телефон для отправки SMS")
parser.add_argument("text", type=str, help="Введите сообщение для отправки")
args = parser.parse_args()


# Отправляем сообщение и принимаем ответ
def send_message(request: HTTPRequest) -> HTTPResponse:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((request.host, int(request.port)))
        s.sendall(request.to_bytes())
        return HTTPResponse.from_bytes(s.recv(4096))


# Создаем параметры для логирования, а также файл
logging.basicConfig(
    level=logging.INFO,
    filename="logfile.log",
    filemode="a",
    encoding="UTF-8",
)
# Из конфига находим хост, порт и путь
HOST, PORT = str(config["sms_service"]["url"]).split("://")[1].split(":")
PATH = PORT.split("/")[1]
PORT = PORT.split("/")[0]
req = HTTPRequest(args.your_tel, args.req_tel, args.text, HOST, int(PORT), PATH)

try:
    res = send_message(req)
    logging.info(res.status_code)
    print(res.status_code)
except ConnectionRefusedError as e:
    logging.error("Address not found")
    print(e)
