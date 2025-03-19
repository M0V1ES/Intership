from dataclasses import dataclass
from typing import Dict


@dataclass
class HTTPResponse:
    status_code: str
    headers: Dict[str, str]
    body: str

    def to_bytes(self) -> bytes:
        # Строка статуса
        status_line = f"HTTP/1.1 {self.status_code}\r\n"
        # Заголовки
        headers_str = "\r\n".join(
            f"{key}: {value}" for key, value in self.headers.items()
        )
        # Тело ответа
        response_str = f"{status_line}{headers_str}\r\n\r\n{self.body}"
        # Преобразуем строку в байты

        return response_str.encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HTTPResponse":
        # Декодируем байты в строку
        response_str = binary_data.decode("utf-8")
        # Разделяем заголовки и тело ответа
        headers, body = response_str.split("\r", 1)
        # Разделяем строку статуса и заголовки
        header_lines = headers.split("\r\n")
        # Извлекаем код статуса и тело
        status_line = header_lines[0][9:]
        headers_dict = {}
        for line in header_lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers_dict[key] = value

        return cls(status_code=status_line, headers=headers_dict, body=body)
