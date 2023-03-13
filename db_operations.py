import sqlite3
from os import path
import csv
class DB:
    def __init__(self, setting_file = "pizza_default_path_setting.txt"):
        self.default_setting_file_path = setting_file
        if not path.exists(self.default_setting_file_path):
            with open("pizza_default_path_setting.txt", "a") as f:
                f.write("pizza.sqlite")
        self.default_db_path = self.__get_default_DB_path()

        #Veritabanı var mı diye kontrol ediliyor
        if not path.exists(self.default_db_path):
            self.__check_DB_health()


        self.__update_default_db_path() #bir veritabanı yolu değişme ihtimaline göre güncelleniyor
        self.conn = sqlite3.connect(self.default_db_path)
        self.curr = self.conn.cursor()


        #menu tablosu var mı kontrol ediliyor yoksa oluşturuluyor
        self.curr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='menu'")
        result = self.curr.fetchone()
        if not result:
            self.__create_menu_table()
            self.__add_menu_data()

        #orders tablosu kontrol ediliyor yoksa oluşturuluyor
        self.curr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        result = self.curr.fetchone()
        if not result:
            self.__create_orders_table()

        #menu tablosunda veri var mı kontrol ediliyor
        self.curr.execute('SELECT COUNT(*) FROM menu')
        result = self.curr.fetchone()[0]
        if result == 0:
            self.__add_menu_data()





    def __get_default_DB_path(self):
        with open(self.default_setting_file_path) as f:
            temp_db_path = f.read()
        return temp_db_path

    def __update_default_db_path(self):
        with open(self.default_setting_file_path, "w") as f:
            f.write(self.default_db_path)

    def __create_clear_DB(self,path):
        self.conn = sqlite3.connect(path)
        self.__create_menu_table()
        self.__add_menu_data()
        self.__create_orders_table()
        self.conn.commit()
        self.conn.close()


    def __check_DB_health(self):

        try:
            self.default_db_path = input("Database bulunamadı!\n"
                                        "Lütfen doğru yolu girdiğinizden emin olunuz.\n"
                                        "yeni bir DB oluşturmak için Direkt Enter'a basınız."
                                        f"tanımlı DB yolu: {self.__get_default_DB_path()}\n"
                                        "Lüfen Yolu giriniz: ")
            if self.default_db_path == "":
                temp_db_path = self.__get_default_DB_path()
                self.__create_clear_DB(temp_db_path)
                self.default_db_path = temp_db_path

        except BaseException as err:
            print(f"DB oluşturulurken bir hata oluştu!\nHata: {err}")
            self.default_db_path = self.__get_default_DB_path()
            print(f"Veritabanı default yola({self.default_db_path}) oluşturuldu.")

    def __create_menu_table(self):
        menu_table = """CREATE TABLE "menu" ("id"	INTEGER NOT NULL UNIQUE, "productId"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL UNIQUE, "description"	TEXT NOT NULL, "price"	NUMERIC NOT NULL,
         PRIMARY KEY("id" AUTOINCREMENT));"""
        self.curr.execute(menu_table)
        self.conn.commit()
        self.__add_menu_data() #oluşturulan tabloya menu giriliyor

    def __create_orders_table(self):
        orders_table = """CREATE TABLE "orders" ("id"	INTEGER NOT NULL UNIQUE, "orderReference" TEXT NOT NULL,
        "name_surname"	NUMERIC NOT NULL, "tc"	TEXT NOT NULL, "cc_number"	TEXT NOT NULL, "cc_pass"	TEXT NOT NULL,
        "description"	TEXT NOT NULL, "total_price"	NUMERIC NOT NULL, "order_time"	TEXT NOT NULL,
         PRIMARY KEY("id" AUTOINCREMENT));"""
        self.curr.execute(orders_table)
        self.conn.commit()

    def __add_menu_data(self):
        path = input("menu tablosu oluşturulacaktır.\n"
                     "Tablonun oluşturulması için menü içeriklerinin bulunduğu csv dosyasının yolunu giriniz: ")
        f = open(path, encoding="UTF-8")
        data = csv.reader(f)
        line = 0
        for i in data:
            try:
                int(i[0]) #ilk satır kolon adını verdiğinden satırı geçmek için hata verdiriyorum.
                query = "INSERT INTO menu (productId, name, description, price) VALUES (?, ?, ?, ?)"
                values = (i[1], i[2], i[3], i[4])
                self.curr.execute(query, values)

            except:
                pass
            line += 1
        self.conn.commit()
        print("Menu oluşturuldu...")
        f.close()


    def get_menu(self):
        try:
            menu = self.curr.execute("select * from menu")
        except sqlite3.OperationalError as err:
            err = str(err)
            if "no such table: menu" in err:
                self.__create_menu_table()
                self.__add_menu_data()
        return menu.fetchall()

    def get_price(self, name):
        price = self.curr.execute(f"select price from menu where name='{name}';")
        return price.fetchone()[0]

    def get_description(self, name):
        desc = self.curr.execute(f"select description from menu where name='{name}';")
        return desc.fetchone()[0]

    def save_order(self, orderReference, name_surname, tc, cc_number, cc_pass, description, total_pirice, order_time):
        query = "INSERT INTO orders (orderReference, name_surname, tc, cc_number, cc_pass, description, total_price," \
                " order_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

        values = (orderReference, name_surname, tc, cc_number, cc_pass, description, total_pirice, order_time)
        self.curr.execute(query, values)
        self.conn.commit()