from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

categories_admin_cd = CallbackData("show_admin_categories", "category_name")
categories_cd = CallbackData("show_categories", "category_name")
buy_cd = CallbackData("set_buy", "product_id")
payment_cd = CallbackData("payment", "bill_id")
new_admin_cd = CallbackData("new_admin", "user_id")
change_product_cd = CallbackData("change_product", "change_type", "product_id")
completed_cd = CallbackData("yes_or_no", "result")
get_parameter_for_change_cd = CallbackData("change_product", "change_type", "product_id")

gender_cd = CallbackData("gender", "value")

product_cd = CallbackData("prod_all", "level", "category_name", "product_id", "product_price", "back")
language_cd = CallbackData("set_language", "language")
language_ch_cd = CallbackData("set_languages", "language")
rates_cd = CallbackData("rates", "rate_id", "rate_price", "using_type", "rate_name")
registration_cd = CallbackData("registration", "number")
adding_song_cd = CallbackData("adding", "number")
confirm_payment_cd = CallbackData("confirm", "username", "user_id")
search_song_cd = CallbackData("search", "call", "value", "criteria")
regions_cd = CallbackData("regions", "id", "name")
genres_cd = CallbackData("genres", "id", "name")
level_cd = CallbackData("level", "num")
statistic_months_cd = CallbackData("statistic", "month", "year")
change_status_cd = CallbackData("change_status", "status")
add_song_cd = CallbackData("add_song", "region_id", "region_name", "genre_id", "genre_name")
notes_cd = CallbackData("notes", "value")
change_song_cd = CallbackData("change_song", "row_name", "type")
change_song_btns_cd = CallbackData("change_song_btn", "value")
delete_sug_song_cd = CallbackData("delete", "id")
change_price_cd = CallbackData("change_price", "rate_id")


def make_prod_cd(level, category="0", prod_id="0", price="0", back="0"):
    return product_cd.new(level=level, category_name=category, product_id=prod_id, product_price=price, back=back)
