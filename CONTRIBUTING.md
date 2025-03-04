# CONTRIBUTING.md


# Katkıda Bulunma Rehberi

Bu projeye katkıda bulunmayı düşündüğünüz için teşekkür ederiz! Bu rehber, projeyi çatallamanızdan (fork) birleştirme isteği (pull request) göndermenize kadar olan süreci kapsamaktadır.

## Başlangıç

1. Repoyu fork edin
2. Fork ettiğiniz repoyu yerel makinenize klonlayın
3. Yeni bir özellik dalı (branch) oluşturun: `git checkout -b ozellik/harika-ozellik`
4. Değişikliklerinizi taahhüt edin (commit): `git commit -m 'Harika özellik ekle'`
5. Dalınızı uzak repoya itin (push): `git push origin ozellik/harika-ozellik`
6. Bir Birleştirme İsteği (Pull Request) açın

## Geliştirme Ortamı

Geliştirmeye başlamadan önce, README.md dosyasındaki kurulum talimatlarını takip ettiğinizden emin olun.

## Kodlama Standartları

- PEP 8 kod stilini takip edin
- Anlamlı değişken ve fonksiyon isimleri kullanın
- Karmaşık işlevleri açıklayan yorumlar ekleyin
- Tüm yeni özellikler için docstrings ekleyin
- İngilizce ve Türkçe karışık kullanımlardan kaçının, tutarlı kalın

## Nelere Katkıda Bulunabilirsiniz

- Hata düzeltmeleri
- Yeni dosya formatı desteği
- Yeni AI sağlayıcı entegrasyonları
- Performans iyileştirmeleri
- Belgelendirme geliştirmeleri
- Kullanıcı arayüzü iyileştirmeleri
- Otomatik testler

## Önerilen Katkı Adımları

### 1. Yeni Dosya İşleyici Eklemek

Yeni bir dosya formatı desteği eklemek için:

1. `src/services/file_processing/processors/` dizininde yeni bir işleyici sınıfı oluşturun
2. `src/services/file_processing/file_processor_factory.py` dosyasını güncelleyin
3. Gerekli bağımlılıkları `requirements.txt` dosyasına ekleyin

### 2. Yeni AI Sağlayıcı Eklemek

Yeni bir AI sağlayıcı eklemek için:

1. `src/services/ai/` dizininde yeni bir servis sınıfı oluşturun
2. `src/services/ai_service_manager.py` dosyasını güncelleyin
3. `src/core/config.py` dosyasında yeni API anahtarı desteği ekleyin

### 3. Kullanıcı Arayüzü İyileştirmeleri

UI iyileştirmeleri için:

1. `src/presentation/views/` dizininde ilgili pencere dosyasını değiştirin
2. CustomTkinter widget'larını kullanarak tasarım tutarlılığını koruyun
3. İyileştirmenin ekran görüntülerini Pull Request'inizde paylaşın

## Sorunlar (Issues)

Yeni bir sorun (issue) açmadan önce:

1. Benzer bir sorunun zaten var olup olmadığını kontrol edin
2. Sorununuzu detaylı bir şekilde açıklayın (hata mesajları, ekran görüntüleri, adımlar)
3. Nasıl yeniden oluşturulacağı hakkında adımlar ekleyin

## Sürüm Numaralandırma

Bu proje [Anlamsal Sürümleme (Semantic Versioning)](https://semver.org/) kullanmaktadır.

## İletişim

Sorularınız için GitHub üzerinden [Sorun (Issue)](https://github.com/kullaniciadi/ai-metin-analizcisi/issues) açabilirsiniz.

Katılımınız için teşekkür ederiz!