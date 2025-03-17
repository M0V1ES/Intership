import base64
import json
from dataclasses import dataclass
from config import config


@dataclass
class HTTPRequest:
    your_tel: int
    req_tel: int
    text: str
    host: str
    port: int

    def to_bytes(self) -> bytes:
        data = {
            "sender": self.your_tel,
            "receiver": self.req_tel,
            "message": self.text,
        }
        body = json.dumps(data)
        # Добавляем заголовки
        headers = [
            f"POST / HTTP/1.1",
            f"Host: {self.host}:{self.port}",
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
        # Извлекаем заголовки
        headers_dict = {}
        for line in header_lines[1:]:
            if ": " in line:  # Проверяем, что строка содержит заголовок
                key, value = line.split(": ", 1)
                headers_dict[key] = value
        return headers, body
