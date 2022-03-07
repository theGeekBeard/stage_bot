from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    name = State()
    surname = State()
    instagram = State()
    birthday = State()
    gender = State()
    city = State()
    rate = State()


class PaymentPhoto(StatesGroup):
    photo = State()


class Product(StatesGroup):
    name = State()
    photo = State()
    price = State()
    confirm = State()


class Purchase(StatesGroup):
    Quantity = State()


class ChangeItem(StatesGroup):
    Value = State()


class Reason(StatesGroup):
    reason = State()


class SearchSong(StatesGroup):
    name = State()


class SuggestSong(StatesGroup):
    info = State()


class Year(StatesGroup):
    year = State()


class Search(StatesGroup):
    username = State()
    instagram = State()


class BanUser(StatesGroup):
    username = State()
    reason = State()


class ChangeStatus(StatesGroup):
    username = State()


class Song(StatesGroup):
    name = State()
    village = State()
    district = State()
    region = State()
    genre = State()
    notes = State()
    level = State()
    telegram_id = State()
    link = State()


class ChangeSong(StatesGroup):
    telegram_id = State()
    value = State()


class Card(StatesGroup):
    number = State()


class NewPrice(StatesGroup):
    price = State()


class Link(StatesGroup):
    link = State()


class RegionGenre(StatesGroup):
    region = State()
    genre = State()


class Operator(StatesGroup):
    username = State()
    user_id = State()


class Date(StatesGroup):
    date = State()
    date2 = State()
    first_date = State()
    second_date = State()

