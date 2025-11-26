class VekaletUcretiHesaplayici:
    def __init__(self):
        self.dilimler = [
            (600000, 0.16),
            (600000, 0.15),
            (1200000, 0.14),
            (1200000, 0.13),
            (1800000, 0.11),
            (2400000, 0.08),
            (3000000, 0.05),
            (3600000, 0.03),
            (4200000, 0.02),
            (float('inf'), 0.01)
        ]

        self.asgari_ucretler = {
            "İcra Daireleri": 9000,
            "İcra Mahkemeleri (Takip)": 11000,
            "İcra Mahkemeleri (Duruşmalı)": 18000,
            "Sulh Hukuk Mahkemeleri": 30000,
            "Asliye Mahkemeleri": 45000,
            "Tüketici Mahkemeleri": 22500,
            "Fikri ve Sınai Haklar Mahkemesi": 55000,
            "Ağır Ceza Mahkemeleri": 65000,
            "Çocuk Mahkemeleri": 45000,
            "Çocuk Ağır Ceza Mahkemeleri": 65000,
            "Yargıtay İlk Derece": 65000,
            "İstinaf (Duruşmasız)": 22000,
            "İstinaf (Duruşmalı)": 42000,
            "Danıştay İlk Derece (Duruşmasız)": 40000,
            "Danıştay İlk Derece (Duruşmalı)": 65000
        }

        self.maktu_ucretler_kategorili = {
            "Yargı Yerleri": {
                "İcra Dairelerinde yapılan takipler": 9000,
                "İcra Mahkemelerinde takip edilen işler": 11000,
                "İcra Mahkemelerinde takip edilen dava ve duruşmalı işler": 18000,
                "Tahliyeye ilişkin icra takipleri": 20000,
                "Sulh Hukuk Mahkemelerinde takip edilen davalar": 30000,
                "Sulh Ceza Hakimliklerinde takip edilen işler": 18000,
                "Asliye Mahkemelerinde takip edilen davalar": 45000,
                "Tüketici Mahkemelerinde takip edilen davalar": 22500,
                "Fikri Sınai Haklar Mahkemelerindeki davalar": 55000,
                "Ağır Ceza Mahkemelerinde takip edilen davalar": 65000,
                "Çocuk Mahkemelerinde takip edilen davalar": 45000
            },
            "Danışmanlık Hizmetleri": {
                "Büroda sözlü danışma (ilk bir saate kadar)": 4000,
                "Çağrı üzerine gidilen yerde sözlü danışma (ilk bir saate kadar)": 7000,
                "Yazılı danışma": 7000,
                "Her türlü dilekçe yazılması": 6000
            },
            "Sözleşmeler": {
                "Kira sözleşmesi ve benzeri": 8000,
                "Tüzük, yönetmelik, miras sözleşmesi": 32000,
                "Şirket ana sözleşmesi": 21000
            },
            "Üst Mahkemeler": {
                "Yargıtay'da ilk derece": 65000,
                "İstinaf başvuru": 22000,
                "İstinaf duruşmalı": 42000,
                "Yargıtay temyiz başvurusu": 30000,
                "Yargıtay duruşmalı temyiz": 40000,
                "Anayasa Mahkemesi bireysel başvuru": 40000,
                "Anayasa Mahkemesi duruşmalı başvuru": 80000
            }
        }

    def nispi_vekalet_ucreti_hesapla(self, dava_degeri, mahkeme_turu):
        if dava_degeri <= 0:
            return 0, []

        toplam_ucret = 0
        kalan_deger = dava_degeri
        dilim_detaylari = []

        for dilim, oran in self.dilimler:
            if kalan_deger <= 0:
                break

            if kalan_deger > dilim:
                hesaplanacak = dilim
            else:
                hesaplanacak = kalan_deger

            ucret = hesaplanacak * oran
            dilim_detaylari.append({
                'dilim': hesaplanacak,
                'oran': oran * 100,
                'ucret': ucret
            })

            toplam_ucret += ucret
            kalan_deger -= dilim

        asgari_ucret = self.asgari_ucretler.get(mahkeme_turu, 0)

        # Dava değeri kontrolü eklendi
        if toplam_ucret > dava_degeri:
            toplam_ucret = dava_degeri
        elif toplam_ucret < asgari_ucret:
            if asgari_ucret > dava_degeri:
                toplam_ucret = dava_degeri
            else:
                toplam_ucret = asgari_ucret

        return toplam_ucret, dilim_detaylari
