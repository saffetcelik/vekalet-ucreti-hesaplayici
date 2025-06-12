# Vekalet Ücreti Hesaplama Programı

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

2024 yılı Avukatlık Asgari Ücret Tarifesi'ne göre vekalet ücretlerini hesaplayan modern ve kullanıcı dostu masaüstü uygulaması.

## 📸 Ekran Görüntüleri

![onizleme](https://github.com/user-attachments/assets/bacf4add-9afd-455c-9729-6a55c6c6a4fb)



## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Teknik Detaylar](#-teknik-detaylar)
- [Geliştirme](#-geliştirme)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-i̇letişim)

## ✨ Özellikler

### 🧮 Hesaplama Özellikleri
- **Canlı Hesaplama**: Dava değeri girilirken anlık hesaplama
- **Dilimli Hesaplama**: 2024 tarife dilimlerine göre otomatik hesaplama
- **Asgari Ücret Kontrolü**: Mahkeme türüne göre asgari ücret garantisi
- **Detaylı Rapor**: Hesaplama sürecinin adım adım gösterimi
- **Kopyalama Özelliği**: Hesaplanan ücreti tek tıkla kopyalama

### 🏛️ Desteklenen Mahkeme Türleri
- İcra Daireleri
- İcra Mahkemeleri (Takip ve Duruşmalı)
- Sulh Hukuk Mahkemeleri
- Asliye Mahkemeleri
- Tüketici Mahkemeleri
- Fikri ve Sınai Haklar Mahkemesi
- Ağır Ceza Mahkemeleri
- Çocuk Mahkemeleri
- Yargıtay İlk Derece
- İstinaf Mahkemeleri
- Danıştay İlk Derece

### 📊 Maktu Ücret Listesi
- **Yargı Yerleri**: Tüm mahkeme türleri için maktu ücretler
- **Danışmanlık Hizmetleri**: Sözlü ve yazılı danışma ücretleri
- **Sözleşmeler**: Kira, şirket ana sözleşmesi vb.
- **Üst Mahkemeler**: Yargıtay, İstinaf, Anayasa Mahkemesi

### 🎨 Kullanıcı Arayüzü
- Modern ve sezgisel tasarım
- Sekmeli yapı (Hesaplama, Maktu Ücretler, Hakkında)
- Türkçe yerelleştirme
- Responsive tasarım
- Sistem teması uyumlu

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- PyQt6

### Hızlı Kurulum

1. **Depoyu klonlayın:**
```bash
git clone https://github.com/kullaniciadi/vekalet-ucreti-hesaplayici.git
cd vekalet-ucreti-hesaplayici
```

2. **Gerekli paketleri yükleyin:**
```bash
pip install PyQt6
```

3. **Programı çalıştırın:**
```bash
python vekalet.py
```

### Alternatif Kurulum (Virtual Environment)

```bash
# Virtual environment oluşturun
python -m venv venv

# Virtual environment'ı aktifleştirin
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Gerekli paketleri yükleyin
pip install PyQt6

# Programı çalıştırın
python vekalet.py
```

### Executable Oluşturma (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=money.png vekalet.py
```

## 📖 Kullanım

### Temel Kullanım

1. **Mahkeme Türü Seçimi**: Dropdown menüden uygun mahkeme türünü seçin
2. **Dava Değeri Girişi**: Dava değerini TL cinsinden girin
3. **Otomatik Hesaplama**: Program otomatik olarak vekalet ücretini hesaplar
4. **Sonuç Görüntüleme**: Detaylı hesaplama raporu görüntülenir
5. **Kopyalama**: "Toplam Ücreti Kopyala" butonu ile sonucu kopyalayın

### Hesaplama Mantığı

Program 2024 yılı tarife dilimlerini kullanır:

| Dilim | Oran |
|-------|------|
| İlk 400.000 TL | %16 |
| İkinci 400.000 TL | %15 |
| Üçüncü 800.000 TL | %14 |
| Dördüncü 1.200.000 TL | %11 |
| Beşinci 1.600.000 TL | %8 |
| Altıncı 2.000.000 TL | %5 |
| Yedinci 2.400.000 TL | %3 |
| Sekizinci 2.800.000 TL | %2 |
| Fazlası | %1 |

### Önemli Notlar

⚠️ **DİKKAT**: Avukatlık Ücret Tarifesinde değişiklik olduğunda veriler otomatik olarak güncellenmez. Bu hususa dikkat ediniz.

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **Python 3.8+**: Ana programlama dili
- **PyQt6**: GUI framework
- **ctypes**: Windows sistem entegrasyonu
- **locale**: Türkçe yerelleştirme

### Proje Yapısı
```
vekalet-ucreti-hesaplayici/
├── vekalet.py              # Ana program dosyası
├── money.png               # Uygulama ikonu
├── README.md               # Bu dosya
└── requirements.txt        # Python bağımlılıkları
```

### Sınıf Yapısı
- `VekaletUcretiHesaplayici`: Hesaplama mantığı
- `ModernVekaletHesaplayici`: Ana uygulama penceresi
- `MaktuUcretlerWidget`: Maktu ücret listesi widget'ı
- `HakkindaWidget`: Hakkında sekmesi widget'ı

## 🛠️ Geliştirme

### Geliştirme Ortamı Kurulumu

```bash
git clone https://github.com/kullaniciadi/vekalet-ucreti-hesaplayici.git
cd vekalet-ucreti-hesaplayici
python -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Kod Yapısı

Program modüler bir yapıya sahiptir:
- Hesaplama mantığı ayrı sınıfta (`VekaletUcretiHesaplayici`)
- UI bileşenleri ayrı widget'larda
- Temiz ve okunabilir kod yapısı

### Test Etme

Program manuel test edilebilir:
1. Farklı dava değerleri ile hesaplama testi
2. Farklı mahkeme türleri ile test
3. Asgari ücret kontrolü testi
4. UI responsiveness testi

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! Katkıda bulunmak için:

1. Bu depoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

### Katkı Alanları
- 🐛 Bug düzeltmeleri
- ✨ Yeni özellikler
- 📚 Dokümantasyon iyileştirmeleri
- 🎨 UI/UX iyileştirmeleri
- 🧪 Test yazma
- 🌐 Çeviri desteği

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

**Saffet Çelik**
- 📧 Email: iletisim@saffetcelik.com.tr
- 🌐 Website: [saffetcelik.com.tr](https://saffetcelik.com.tr)

## 🙏 Teşekkürler

- PyQt6 geliştirici ekibine
- Türkiye Barolar Birliği'ne (ücret tarifesi için)
- Tüm katkıda bulunanlara

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

## 📈 Sürüm Geçmişi

### v1.0.0 (2024)
- İlk sürüm
- Temel hesaplama özellikleri
- Modern UI tasarımı
- Maktu ücret listesi
- Canlı hesaplama özelliği
