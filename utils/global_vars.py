class RequestStatus:
    in_queue = "В очереди"
    in_progress = "Выполняется"
    completed = "Выполнено"


def answer_text(name: str, department: str, description: str) -> str:
    return f"<b>Отправитель:</b> {name}\n<b>Кабинет/отделение:</b> {department}\n<b>Текст заявки:</b>\n{description}"
