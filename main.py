# -- coding:utf-8 --
import datetime
import trusted_info_check
import db_operations
import sys
import hashlib

#String class ismini class name olarak çeviriyor
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

# Pizza'nın üst sınıfını tanımladık
class Pizza:
    def get_description(self):
        return self.__class__.__name__

    def get_cost(self):
        return self.__class__.get_price(self)


# Pizzalar için alt sınıfları oluşturuyoruz
class KlasikPizza(Pizza):
    def __init__(self):
        self.description = db.get_description(self.__class__.__name__)
        print(self.description + "\n")
    def get_price(self):
        return db.get_price(self.__class__.__name__)


class Margarita(Pizza):
    def __init__(self):
        self.description = db.get_description(self.__class__.__name__)
        print(self.description + "\n")
    def get_price(self):
        return db.get_price(self.__class__.__name__)


class TurkPizza(Pizza):
    def __init__(self):
        self.description = db.get_description(self.__class__.__name__)
        print(self.description + "\n")
    def get_price(self):
        return db.get_price(self.__class__.__name__)

class SadePizza(Pizza):
    def __init__(self):
        self.description = db.get_description(self.__class__.__name__)
        print(self.description + "\n")
    def get_price(self):
        return db.get_price(self.__class__.__name__)


# Malzemeler içi üst sınıf oluşturuldu
class Decorator(Pizza):
    def __init__(self, deco):
        self.component = deco

    def get_cost(self):
        return self.component.get_cost() + \
               Pizza.get_cost(self)

    def get_description(self):
        return self.component.get_description() + \
               ' : ' + Pizza.get_description(self)


# Malzemeler için alt sınıflar oluşturuldu
class Zeytin(Decorator):
    def __init__(self, extra):
        Decorator.__init__(self, extra)
    def get_price(self):
        return db.get_price(self.__class__.__name__)

class Mantar(Decorator):
    def __init__(self, extra):
        Decorator.__init__(self, extra)
    def get_price(self):
        return db.get_price(self.__class__.__name__)

class KeciPeyniri (Decorator):
    def __init__(self, extra):
        Decorator.__init__(self, extra)
    def get_price(self):
        return db.get_price(self.__class__.__name__)

class Et (Decorator):
    def __init__(self, extra):
        Decorator.__init__(self, extra)
    def get_price(self):
        return db.get_price(self.__class__.__name__)

class Sogan(Decorator):
    def __init__(self, extra):
        Decorator.__init__(self, extra)
    def get_price(self):
        return db.get_price(self.__class__.__name__)

class Misir (Decorator):
    def __init__(self, extra):
        Decorator.__init__(self, extra)
    def get_price(self):
        return db.get_price(self.__class__.__name__)

#veritabanından menü tablosundaki tüm değerleri çekiyor
def get_menu():
    return db.get_menu()

def print_menu(menu):
    print("*" * 10, end="")
    print("MENU".center(10),end="")
    print("*" * 10)
    print("Sipariş\t\tFiyat\t\tİsim")
    print("Numarası")
    for i in menu:
        """
        Menü veritabanından aşağıdaki gibi gelmekte. sütün isimleri:
        id, productId, name, description, price
        (4, 4, 'Sade Pizza', 'Malzemeler= Domates Sosu, Mozarella', 50)
        Burada menüyü düzgün bir şekilde yazdırıyoruz
        """
        print(f"{i[1]}\t\t{i[4]}TL\t\t{i[2]}")

def create_order_dict(menu):
    temp = {}
    for i in menu:
        temp[i[1]] = i[2]
    return temp


def main():

    menu_content = get_menu()
    print_menu(menu_content)

    siparis_dict = create_order_dict(menu_content)

    pizza_secim = int(input("Lütfen Pizzanızı Seçiniz: "))
    while pizza_secim not in range(1,5):
        print("***Hatalı Seçim Yaptınız***".center(5))
        get_menu()
        pizza_secim = int(input("Lütfen menüde bulunan bir Pizza seçiniz.: "))


    siparis = str_to_class(siparis_dict[pizza_secim])()


    while True:
        exra_secim = int(input(
            "Ekstra Malzeme İçin Malzeme Numarasını Seçiniz (Siparişinizi Onaylamak İçin '0' tuşuna basınız): "))
        if exra_secim == 0:
            break
        if exra_secim in range(11,17):
            siparis = str_to_class(siparis_dict[exra_secim])(siparis)
        else:
            print("Hatali ekstra secim yaptınız!")


    print("\n" + siparis.get_description().strip() + str(siparis.get_cost()) + "TL")
    print("\n")
    print("----------Sipariş Bilgileri----------\n")

    checks = trusted_info_check.Check()
    isim = input("Adınız: ")
    TC_kimlik = input("Kimlik Numaranız: ")
    while not checks.tc_check(TC_kimlik):
        TC_kimlik = input("Hatalı kimlik numarası!\n"
                          "Lütfen doğru TC giriniz: ")

    TC_kimlik = TC_kimlik[:3] + "*****" + TC_kimlik[-3:]
    kredi_Kart_numarasi = input("Kredi Kartı Numaranızı Giriniz: ")

    while not checks.kart_check(kredi_Kart_numarasi):
        kredi_Kart_numarasi = input("Hatalı kredi kart numarası!\n"
                          "Lütfen kart numaranızı kontrol ederek tekrar giriniz: ")

    kredi_Kart_numarasi = kredi_Kart_numarasi[:4] + "********" + kredi_Kart_numarasi[-4:]


    kart_sifresi = input("Kredi Kartı Şifresi: ")
    while not checks.kart_sifre_kontrol(kart_sifresi):
        kart_sifresi = input("Hatalı kredi kart sifresi!\n"
                          "Lütfen kart sifrenizi kontrol ederek tekrar giriniz: ")

    kart_sifresi = hashlib.sha256(kart_sifresi.encode("UTF-8")).hexdigest()

    siparis_zamani = datetime.datetime.now()
    siparis_referans = siparis_zamani.timestamp()

    #orderReference, name_surname, tc, cc_number, cc_pass, description, order_time
    desc = siparis.get_description()
    db.save_order(siparis_referans, isim, TC_kimlik, kredi_Kart_numarasi, kart_sifresi, desc, siparis.get_cost(),
                  siparis_zamani)
    print("Sipariş Onaylandı.")


if __name__ == '__main__':
    # Veri tabanı işlemleri için bir işaretçi oluşturuyoruz
    db = db_operations.DB()
    main()
    db.conn.close()
