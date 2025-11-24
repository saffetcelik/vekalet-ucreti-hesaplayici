import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QComboBox, QLineEdit, QTextEdit, 
                           QPushButton, QTabWidget, QScrollArea, QTreeWidget, 
                           QTreeWidgetItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QDoubleValidator, QClipboard
import locale
import ctypes

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ModernVekaletHesaplayici(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hesaplayici = VekaletUcretiHesaplayici()
        self.son_hesaplanan_ucret = None
        
        # Icon ayarlaması
        icon_path = resource_path("money.png")
        self.app_icon = QIcon(icon_path)
        self.setWindowIcon(self.app_icon)
        
        # Windows görev çubuğu iconu için
        if sys.platform == 'win32':
            myappid = u'vekalet.hesaplama.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        self.initUI()
        
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hesapla)


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

class MaktuUcretlerWidget(QWidget):
    def __init__(self, maktu_ucretler):
        super().__init__()
        self.maktu_ucretler = maktu_ucretler
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        baslik = QLabel("2025 Yılı Maktu Vekalet Ücretleri")
        baslik.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(baslik)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Hizmet Türü", "Ücret (TL)"])
        self.tree.setAlternatingRowColors(True)
        self.tree.setColumnWidth(0, 400)
        
        for kategori, ucretler in self.maktu_ucretler.items():
            kategori_item = QTreeWidgetItem([kategori])
            kategori_item.setFont(0, QFont("Segoe UI", 10, QFont.Weight.Bold))
            
            for hizmet, ucret in ucretler.items():
                ucret_str = f"{ucret:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                hizmet_item = QTreeWidgetItem([hizmet, ucret_str])
                kategori_item.addChild(hizmet_item)
            
            self.tree.addTopLevelItem(kategori_item)
            kategori_item.setExpanded(True)
        
        layout.addWidget(self.tree)

class HakkindaWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        baslik = QLabel("Vekalet Ücreti Hesaplama Programı")
        baslik.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        aciklama = QLabel("""
        Bu program, 2025 yılı Avukatlık Asgari Ücret Tarifesi'ne göre
        vekalet ücretlerini hesaplamak için tasarlanmıştır.
                          
                Avukatlık Ücret Tarifesinde Değişiklik Olduğunda   
                      Veriler Otomatik Olarak Güncellenmez!! 
                          Bu Hususa Dikkat Ediniz.
        
        Özellikler:
        - Canlı hesaplama
        - Tüm mahkeme türleri için destek
        - Detaylı hesaplama raporu
        - Maktu ücret listesi
        - Modern ve kullanıcı dostu arayüz
        
        Sürüm: 1.0.0
        """)
        aciklama.setWordWrap(True)
        
        hazirlayanLabel = QLabel("Hazırlayan: Saffet Çelik - iletisim@saffetcelik.com.tr")
        hazirlayanLabel.setFont(QFont("Segoe UI", 10))
        hazirlayanLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(baslik)
        layout.addWidget(aciklama)
        layout.addStretch()
        layout.addWidget(hazirlayanLabel)
        self.setLayout(layout)

class ModernVekaletHesaplayici(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hesaplayici = VekaletUcretiHesaplayici()
        self.son_hesaplanan_ucret = None
        self.initUI()
        
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hesapla)
        
    def initUI(self):
        self.setWindowTitle('Vekalet Ücreti Hesaplama')
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        tabs = QTabWidget()
        hesaplama_tab = QWidget()
        maktu_tab = MaktuUcretlerWidget(self.hesaplayici.maktu_ucretler_kategorili)
        hakkinda_tab = HakkindaWidget()
        
        tabs.addTab(hesaplama_tab, "Hesaplama")
        tabs.addTab(maktu_tab, "Maktu Ücretler")
        tabs.addTab(hakkinda_tab, "Hakkında")
        
        hesaplama_layout = QVBoxLayout(hesaplama_tab)
        
        # Mahkeme türü seçimi
        mahkeme_layout = QHBoxLayout()
        mahkeme_label = QLabel("Mahkeme Türü:")
        self.mahkeme_combo = QComboBox()
        self.mahkeme_combo.addItems(self.hesaplayici.asgari_ucretler.keys())
        self.mahkeme_combo.setCurrentText("Asliye Mahkemeleri")
        mahkeme_layout.addWidget(mahkeme_label)
        mahkeme_layout.addWidget(self.mahkeme_combo)
        
        # Dava değeri girişi
        dava_layout = QHBoxLayout()
        dava_label = QLabel("Dava Değeri (TL):")
        self.dava_input = QLineEdit()
        self.dava_input.setValidator(QDoubleValidator(0.99, 999999999.99, 2))
        dava_layout.addWidget(dava_label)
        dava_layout.addWidget(self.dava_input)
        
        # Sonuç alanı
        self.sonuc_text = QTextEdit()
        self.sonuc_text.setReadOnly(True)
        
        # Kopyalama butonu
        self.kopya_buton = QPushButton("Toplam Ücreti Kopyala")
        self.kopya_buton.setEnabled(False)
        self.kopya_buton.clicked.connect(self.ucreti_kopyala)
        
        hesaplama_layout.addLayout(mahkeme_layout)
        hesaplama_layout.addLayout(dava_layout)
        hesaplama_layout.addWidget(self.sonuc_text)
        hesaplama_layout.addWidget(self.kopya_buton)
        
        layout.addWidget(tabs)
        
        self.dava_input.textChanged.connect(self.canli_hesaplama)
        self.mahkeme_combo.currentTextChanged.connect(self.canli_hesaplama)
        
    def para_formatla(self, deger):
        return f"{deger:,.2f}TL".replace(",", "X").replace(".", ",").replace("X", ".")
        
    def canli_hesaplama(self):
        self.timer.stop()
        self.timer.start(300)
        
    def ucreti_kopyala(self):
        if self.son_hesaplanan_ucret is not None:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.para_formatla(self.son_hesaplanan_ucret))
        
    def hesapla(self):
        try:
            dava_degeri_text = self.dava_input.text().replace(".", "").replace(",", ".")
            if not dava_degeri_text:
                self.sonuc_text.clear()
                self.kopya_buton.setEnabled(False)
                self.son_hesaplanan_ucret = None
                return
                
            dava_degeri = float(dava_degeri_text)
            mahkeme_turu = self.mahkeme_combo.currentText()
            
            ucret, detaylar = self.hesaplayici.nispi_vekalet_ucreti_hesapla(dava_degeri, mahkeme_turu)
            self.son_hesaplanan_ucret = ucret
            self.kopya_buton.setEnabled(True)
            
            sonuc_text = f"<h3>VEKALET ÜCRETİ HESAPLAMA SONUCU</h3>"
            sonuc_text += "<hr>"
            sonuc_text += f"<p><b>Mahkeme Türü:</b> {mahkeme_turu}</p>"
            sonuc_text += f"<p><b>Dava Değeri:</b> {self.para_formatla(dava_degeri)}</p>"
            sonuc_text += f"<p><b>Asgari Ücret:</b> {self.para_formatla(self.hesaplayici.asgari_ucretler[mahkeme_turu])}</p>"
            
            sonuc_text += "<h4>Hesaplama Detayları:</h4>"
            sonuc_text += """
                <table width='100%' cellpadding='5' style='border-collapse: collapse; border: 1px solid currentColor;'>
                <tr>
                    <th style='border: 1px solid currentColor; padding: 8px; text-align: left;'>Dilim</th>
                    <th style='border: 1px solid currentColor; padding: 8px; text-align: center;'>Oran</th>
                    <th style='border: 1px solid currentColor; padding: 8px; text-align: right;'>Ücret</th>
                </tr>
            """
            
            for detay in detaylar:
                sonuc_text += "<tr>"
                sonuc_text += f"<td style='border: 1px solid currentColor; padding: 8px;'>{self.para_formatla(detay['dilim'])}</td>"
                sonuc_text += f"<td style='border: 1px solid currentColor; padding: 8px; text-align: center;'>%{detay['oran']:.1f}</td>"
                sonuc_text += f"<td style='border: 1px solid currentColor; padding: 8px; text-align: right;'>{self.para_formatla(detay['ucret'])}</td>"
                sonuc_text += "</tr>"
            
            sonuc_text += "</table>"
            sonuc_text += "<hr>"
            sonuc_text += f"<h3 style='text-align: right;'>Toplam Vekalet Ücreti: {self.para_formatla(ucret)}</h3>"
            
            self.sonuc_text.setHtml(sonuc_text)
            
        except ValueError:
            self.sonuc_text.setHtml("""
                <div style='border: 1px solid currentColor; padding: 15px; border-radius: 4px;'>
                    <h4 style='margin-top: 0;'>Hata</h4>
                    <p>Lütfen geçerli bir dava değeri giriniz.</p>
                </div>
            """)
            self.kopya_buton.setEnabled(False)
            self.son_hesaplanan_ucret = None
        except Exception as e:
            self.sonuc_text.setHtml(f"""
                <div style='border: 1px solid currentColor; padding: 15px; border-radius: 4px;'>
                    <h4 style='margin-top: 0;'>Hata</h4>
                    <p>Bir hata oluştu: {str(e)}</p>
                </div>
            """)
            self.kopya_buton.setEnabled(False)
            self.son_hesaplanan_ucret = None

def main():
    app = QApplication(sys.argv)
    
    # Uygulama iconu ayarı
    icon_path = resource_path("money.png")
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)
    
    # Sistemin varsayılan font ailesi
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Fusion stili kullanarak sistem temasına uyum sağlama
    app.setStyle("Fusion")
    
    ex = ModernVekaletHesaplayici()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()