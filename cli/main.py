import argparse
import socket
from HTTPResponse import HTTPResponse
from HTTPRequest import HTTPRequest
from config import config
import logging

parser = argparse.ArgumentParser(description="CLI-приложение для отправки SMS в API")
parser.add_argument("your_tel", type=str, help="Введите ваш телефон")
parser.add_argument("req_tel", type=str, help="Введите телефон для отправки SMS")
parser.add_argument("text", type=str, help="Введите сообщение для отправки")
args = parser.parse_args()


def send_message(request: HTTPRequest) -> HTTPResponse:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((request.host, int(request.port)))
        s.sendall(request.to_bytes())
        return HTTPResponse.from_bytes(s.recv(4096))


logging.basicConfig(
    level=logging.INFO,
    filename="logfile.log",
    filemode="a",
    encoding="UTF-8",
)

HOST, PORT = str(config["sms_service"]["url"][:-1]).split("://")[1].split(":")
req = HTTPRequest(args.your_tel, args.req_tel, args.text, HOST, int(PORT))
logging.info((args.your_tel, args.req_tel, args.text))

try:

    res = send_message(req)
    logging.info(res.status_code)
    print(res.status_code)

except ConnectionRefusedError as e:
    logging.error("Address not found")
    print(e)
