# src/core/prompts.py

class AnalysisPrompts:
    """Analiz tipleri için prompt şablonları"""
    
    ANALYSIS_PROMPTS = {
        "Özet": """Aşağıdaki metni kapsamlı bir şekilde özetleyin.

Özetleme Kuralları:
1. Ana fikirleri koruyun
2. Gereksiz detayları çıkarın
3. Kronolojik sırayı koruyun
4. Profesyonel bir dil kullanın
5. Paragraflar halinde yazın

Özetlenecek metin:
""",
        
        "Soru-Cevap Üretimi": """Aşağıdaki metni analiz et, (fine tunning metoduyla) eğiteceğimiz yapay zekamızı en iyi şekilde eğitebileceğim şekilde, **özetlenmiş** olarak, **tekrarsız** bir şekilde **farklı** soru-cevap çiftleri üret.
    **Önemli Not:** Aynı soru-cevap çiftlerini tekrar etme!

    JSON formatında çıktı üret:
    {{
    "soru-cevaplar": [
        {{
        "soru": "örnek soru",
        "cevap": "örnek cevap"
        }}
    ]
    }}
    Analiz edilecek metin:
    """,
        
        "Anahtar Noktalar": """Aşağıdaki metinden temel noktaları çıkarın.

Sunum Formatı:
1. Her önemli nokta yeni bir paragrafta olmalı
2. Önem sırasına göre sıralanmalı
3. Her nokta kısa bir başlıkla başlamalı
4. Başlıkların altına detaylı açıklamalar eklenmeli

İncelenecek metin:
""",
        
        "Çeviri": """Aşağıdaki metni İngilizce'ye çevirin.

Çeviri Kuralları:
1. Anlamı eksiksiz aktarın
2. Doğal bir İngilizce kullanın
3. Teknik terimleri parantez içinde orijinal halleriyle belirtin
4. Kültürel referansları dipnot olarak açıklayın
5. Paragraf yapısını koruyun

Çevrilecek metin:
""",
        
        "Analiz": """Aşağıdaki metni detaylı bir şekilde analiz edin.

Analiz Rapor Formatı:
1. Giriş
2. Ana Temalar
3. Kullanılan Argümanlar ve Örnekler
4. Yazarın Bakış Açısı
5. Güçlü ve Zayıf Yönler
6. Sonuç ve Değerlendirme

Analiz edilecek metin:
""",
        
        "Teknik Analiz": """Metni teknik açıdan analiz edin.

Teknik Rapor Formatı:
1. Teknik Özet
2. Kullanılan Teknolojiler
3. Teknik Terimler Sözlüğü
4. Uygulama Adımları
5. Teknik Gereksinimler
6. Potansiyel Sorunlar ve Çözüm Önerileri
7. Teknik Değerlendirme

İncelenecek metin:
""",
        
        "Özet Rapor": """Metinden profesyonel bir özet rapor hazırlayın.

Rapor Formatı:
1. Yönetici Özeti 
2. Ana Bulgular
3. Detaylı Analiz
   a. Mevcut Durum
   b. Bulgular
   c. Değerlendirme
4. Sonuçlar
5. Öneriler ve Aksiyon Adımları

İncelenecek metin:
"""
    }

    DEFAULT_PROMPT = """Aşağıdaki metni detaylı bir şekilde analiz edin.

Analiz Kuralları:
1. Ana konuyu belirtin
2. Önemli noktaları vurgulayın
3. Metni bölümlere ayırın
4. Her bölümü ayrı ayrı değerlendirin
5. Genel bir sonuç yazın

Analiz edilecek metin:
"""

    @classmethod
    def get_prompt(cls, analysis_type: str, custom_analysis_repo=None) -> str:
        """Get prompt template for analysis type"""
        # Standart analiz türlerini kontrol et
        if analysis_type in cls.ANALYSIS_PROMPTS:
            return cls.ANALYSIS_PROMPTS[analysis_type]
        
        # Özel analiz türlerini kontrol et
        if custom_analysis_repo:
            try:
                custom_type = custom_analysis_repo.get_by_name(analysis_type)
                if custom_type:
                    return custom_type.prompt_template
            except Exception as e:
                print(f"Özel analiz türü alınırken hata: {str(e)}")
        
        # Hiçbir türde bulunamazsa varsayılan prompt'u döndür
        return cls.DEFAULT_PROMPT