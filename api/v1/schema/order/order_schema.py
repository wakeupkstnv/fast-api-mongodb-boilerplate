from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

'''

user_id
"20045"
fio
"Қуатбек Жансая Қуатбекқызы"
address
"Астана қаласы, Астана, ЖК Манхэттен 4, улица Айтеке би 14, квартира 51"
phone
"87786198008"
check_link
"https://bub-gift-bot.s3.us-east-1.amazonaws.com/checks/AgADu2AAAhPj4Es…"
timestamp
"2025-01-06 18:24:34"
count_of_orders
2
username
"N/A"
chat_id
"6723267806"
language
null

'''

class Order(BaseModel):
    user_id: str
    fio: str
    address: str
    phone: str
    check_link: str
    timestamp: str
    count_of_orders: Optional[str | int] = None
    username: str



class OrderInDB(Order):
    id: str 
