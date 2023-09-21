from typing import Optional


class RequestStatus:
    """
    Класс для состояний заявок.

    :ivar in_queue: Заявка в очереди.
    :ivar in_progress: Заявка выполняется.
    :ivar completed: Заявка выполнена.
    """
    in_queue = "В очереди"
    in_progress = "Выполняется"
    completed = "Выполнено"


def answer_text(request_id: Optional[int], name: str, department: str, status: Optional[str], description: str,
                is_request_id: bool, is_status: bool) -> str:
    """
    Функция для формирования текста с информацией о заявке.

    :param request_id: ID заявки.
    :type request_id: Optional[int]
    :param name: Имя пользователя.
    :type name: str
    :param department: Подразделение пользователя.
    :type department: str
    :param status: Статус заявки.
    :type status: Optional[str]
    :param description: Описание заявки.
    :type description: str
    :param is_request_id: Флаг, нужно ли вносить в текст ID заявки.
    :type is_request_id: bool
    :param is_status: Флаг, нужно ли вносить в текст статус заявки.
    :type is_status: bool

    :return: Текст ответа с информацией о заявке.
    :rtype: str
    """
    text = ""
    if is_request_id:
        text += f"<b>Заявка №{request_id}</b>\n\n"
    text += f"<b>Отправитель:</b> {name}\n<b>Кабинет/отделение:</b> {department}\n"
    if is_status:
        text += f"<b>Статус заявки:</b> {status}\n"
    text += f"<b>Текст заявки:</b>\n{description}"
    return text
