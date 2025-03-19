import base64
import json
import logging
from dataclasses import dataclass
from config import config


@dataclass
class HTTPRequest:
    your_tel: str
    req_tel: str
    text: str
    host: str
    port: int
    path: str

    # Создаем правила для номеров и логируем их
    def __post_init__(self):
        logging.info((self.your_tel, self.req_tel, self.text))
        if (len(self.your_tel) == 11) and (len(self.req_tel) == 11):
            try:
                your_tel = int(self.your_tel)
                req_tel = int(self.req_tel)

            except ValueError as e:
                logging.error(ValueError("Неправильный номер телефона"))
                raise ValueError("Неправильный номер телефона")
        else:
            logging.error(ValueError("Номер телефона должен быть длиной 11 символов"))
            raise ValueError("Номер телефона должен быть длиной 11 символов")

    def to_bytes(self) -> bytes:
        # Добавляем тело запроса
        data = {
            "sender": self.your_tel,
            "recipient": self.req_tel,
            "message": self.text,
        }
        body = json.dumps(data)
        # Добавляем заголовки
        headers = [
            f"POST /{self.path} HTTP/1.1",
            f"Host: {self.host}:{self.port}/{self.path}/",
            "Content-Type: application/json",
            f"Content-Length: {len(body)}",
            f"Authorization: Basic {base64.b64encode(f'{config['sms_service']['username']}:{config['sms_service']['password']}'.encode()).decode()}",
            "Connection: close",
        ]
        # Собираем весь запрос
        request_parts = "\r\n".join(headers) + "\r\n\r\n" + body
        return request_parts.encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        # Декодируем байты в строку
        response_str = binary_data.decode("utf-8")
        # Разделяем заголовки и тело ответа
        headers, body = response_str.split("\r\n\r\n", 1)
        # Разделяем строку статуса и заголовки
        header_lines = headers.split("\r\n")
        headers_dict = {}
        for line in header_lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers_dict[key] = value
        return headers, body
