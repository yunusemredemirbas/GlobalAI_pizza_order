
class Check:

    def tc_check(self, tc):
        if len(tc) != 11 or tc[0] == "0":
            return False
        return True

    def kart_check(self, kart_no):
        if len(kart_no) != 16 or kart_no[0] == "0":
            return False
        return True

    def kart_sifre_kontrol(self, sifre):
        if len(sifre) != 4:
            return False
        return True
