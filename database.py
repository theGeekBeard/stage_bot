class Database:

    def __init__(self, con):
        self.db = con
        self.sql = self.db.cursor()

    # Setters

    # регистрация пользователя
    async def register_new_user(self, user_id, username, status):
        with self.db:
            if not await self.get_user(user_id):
                self.sql.execute(
                    f"INSERT INTO users(user_id, username,status) VALUES({user_id}, '{username}',{status})")

    # добавление остальных полей для пользователя
    async def add_user_parameters(self, user_id, request):
        with self.db:
            self.sql.execute(f"UPDATE users SET {request} WHERE user_id={user_id}")

    async def set_card_number(self, card_number):
        with self.db:
            self.sql.execute(f"UPDATE configs SET card='{card_number}'")

    async def set_channel_link(self, link):
        with self.db:
            self.sql.execute(f"UPDATE configs SET channel='{link}'")

    async def update_user_parameters(self, user_id, parameter_name, parameter_value):
        with self.db:
            self.sql.execute(f"UPDATE users SET {parameter_name}={parameter_value} WHERE user_id={user_id}")

    async def add_suggest_song(self, info, username, display):
        with self.db:
            self.sql.execute(f"INSERT INTO proporsed_musics(info, username, display) VALUES('{info}', '{username}',"
                             f"{display})")

    async def add_song(self, rows_names, values):
        with self.db:
            self.sql.execute(f"INSERT INTO musics({rows_names}) VALUES({values})")

    async def update_song(self, request, song_id):
        with self.db:
            self.sql.execute(f"UPDATE musics SET {request} WHERE telegram_id={song_id}")

    async def delete_sug_song(self, song_id):
        with self.db:
            self.sql.execute(f"DELETE FROM proporsed_musics WHERE id = {song_id}")

    async def update_rate_price(self, rate_id, price):
        with self.db:
            self.sql.execute(f"UPDATE rates SET price={price} WHERE id={rate_id}")

    async def add_region(self, region):
        with self.db:
            self.sql.execute(f"INSERT INTO regions(name) VALUES('{region}')")

    async def add_genre(self, genre):
        with self.db:
            self.sql.execute(f"INSERT INTO genres(name) VALUES('{genre}')")

    async def add_operator(self, username, user_id):
        with self.db:
            self.sql.execute(f"INSERT INTO admins(username, user_id) VALUES('{username}', {user_id})")

    # Getters

    # достаем пользователя из базы данных
    async def get_user(self, user_id):
        self.sql.execute(f"SELECT * FROM users WHERE user_id={user_id}")
        return self.sql.fetchone()

    async def get_config_value(self, parameter_name):
        with self.db:
            self.sql.execute(f"SELECT {parameter_name} FROM configs")
            return self.sql.fetchone()[0]

    async def get_rates(self):
        with self.db:
            self.sql.execute(f"SELECT * FROM rates ORDER BY id ASC")
            return self.sql.fetchall()

    async def get_rate_info(self, rate_id):
        with self.db:
            self.sql.execute(f"SELECT * FROM rates WHERE id={rate_id} ORDER BY id ASC")
            return self.sql.fetchone()

    async def get_rates_info(self, user_id):
        with self.db:
            self.sql.execute(
                f"SELECT rates.price, rates.term, rates.name, users.rate_id FROM rates INNER JOIN users ON rates.id = "
                f"users.rate_id "
                f"WHERE users.user_id = {user_id} ORDER BY rates.id ASC")
            return self.sql.fetchone()

    async def get_card_number(self):
        with self.db:
            self.sql.execute("SELECT card FROM configs")
            return self.sql.fetchone()[0]

    async def get_channel_link(self):
        with self.db:
            self.sql.execute("SELECT channel FROM configs")
            return self.sql.fetchone()[0]

    async def get_users(self):
        with self.db:
            self.sql.execute(
                "SELECT user_id, subscription_date, name, username FROM users WHERE status=2 OR status=3 or status=5")
            return self.sql.fetchall()

    async def check_tariff(self, user_id, rate_id):
        with self.db:
            self.sql.execute(
                f"SELECT rate_id FROM users WHERE user_id={user_id} AND rate_id={rate_id}"
            )
            return self.sql.fetchone()

    async def get_user_status(self, user_id):
        with self.db:
            self.sql.execute(f"SELECT status FROM users WHERE user_id={user_id}")
            return self.sql.fetchone()[0]

    async def get_song(self, title=None, request=None):
        with self.db:
            if not title is None:
                self.sql.execute(f"SELECT musics.title, musics.village, musics.district, regions.name, genres.name, "
                                 f"musics.notes, "
                                 f"musics.level, musics.link FROM musics INNER JOIN regions ON "
                                 f"musics.region_id=regions.id "
                                 f"INNER JOIN genres ON musics.genre_id=genres.id WHERE musics.title='{title}' "
                                 f"AND activity=true")
            else:
                self.sql.execute(f"SELECT musics.title, musics.village, musics.district, regions.name, genres.name, "
                                 f"musics.notes, "
                                 f"musics.level, musics.link, musics.telegram_id, musics.activity "
                                 f"FROM musics INNER JOIN regions ON musics.region_id=regions.id "
                                 f"INNER JOIN genres ON musics.genre_id=genres.id WHERE {request} "
                                 f"AND activity=true")

            return self.sql.fetchall()

    async def get_regions(self):
        with self.db:
            self.sql.execute("SELECT * FROM regions ORDER BY name")
            return self.sql.fetchall()

    async def get_genres(self):
        with self.db:
            self.sql.execute("SELECT * FROM genres")
            return self.sql.fetchall()

    async def get_admins(self, user_id):
        with self.db:
            self.sql.execute(f"SELECT * FROM admins WHERE user_id = {user_id}")
            return self.sql.fetchall()

    async def get_users_with_status(self, status):
        with self.db:
            self.sql.execute(f"SELECT username FROM users WHERE status = {status}")
            return self.sql.fetchall()

    async def get_count_users(self, request):
        with self.db:
            self.sql.execute(f"SELECT COUNT(user_id) FROM users WHERE {request}")
            return self.sql.fetchone()[0]

    async def get_user_with_data(self, row_name, data):
        with self.db:
            self.sql.execute(f"SELECT users.username, rates.name, rates.price, users.subscription_date,"
                             f"users.payment_date, users.name, users.surname, users.instagram, users.birthday, "
                             f"users.city, users.status, users.registration_date, users.deleteauto_date, "
                             f"users.cancel_date, users.ban_date, users.recovery_date, users.reason_cancel,"
                             f"reason_delete, user_id FROM users INNER JOIN rates ON "
                             f"rates.id=users.rate_id "
                             f"WHERE users.{row_name} = '{data}'")
            return self.sql.fetchone()

    async def get_non_users(self, request):
        with self.db:
            self.sql.execute(f"SELECT user_id, username FROM users WHERE {request}")
            return self.sql.fetchall()

    async def get_overdue_users(self):
        with self.db:
            self.sql.execute(f"SELECT username, subscription_date, payment_date FROM users")
            return self.sql.fetchall()

    async def get_song_with_id(self, telegram_id):
        with self.db:
            self.sql.execute(f"SELECT * FROM musics WHERE telegram_id = {telegram_id}")
            return self.sql.fetchone()

    async def get_suggest_song(self):
        with self.db:
            self.sql.execute(f"SELECT * FROM proporsed_musics WHERE display = true")
            return self.sql.fetchall()

    async def get_all_admins(self):
        with self.db:
            self.sql.execute(f"SELECT user_id FROM admins")
            return self.sql.fetchall()

    async def check_user(self, user_id):
        with self.db:
            self.sql.execute(f"SELECT status FROM users WHERE user_id={user_id}")
            return self.sql.fetchone()

    async def get_sub_date(self, user_id):
        with self.db:
            self.sql.execute(f"SELECT subscription_date FROM users WHERE user_id={user_id}")
            return self.sql.fetchone()[0]

    async def get_payment_amount(self, date1, date2):
        self.sql.execute(f"SELECT COUNT(payment_amount), SUM(payment_amount) FROM users WHERE "
                         f"to_char(payment_date,'yyyy-mm-dd') "
                         f"BETWEEN '{date1}' AND '{date2}'")
        return self.sql.fetchone()

    async def get_count_user_with_link(self, date1, date2):
        self.sql.execute(f"SELECT COUNT(user_id) FROM users WHERE link=1 AND (status = 1 OR status = 2 "
                         f"OR status = 3 OR status = 5 OR status = 11) AND to_char(payment_date,'yyyy-mm-dd') "
                         f"BETWEEN '{date1}' AND '{date2}'")
        return self.sql.fetchone()
