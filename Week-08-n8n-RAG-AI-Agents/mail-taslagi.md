# Mentor / Eğitmen E-posta Taslağı

## Konu

Week 08 - n8n RAG & AI Agents: KampRota Türkiye Gezi Asistanı

## E-posta metni

Merhaba,

Bu hafta n8n üzerinde RAG ve AI Agent kavramlarını birlikte kullandığım **KampRota Türkiye Gezi Asistanı** projesini geliştirdim.

Projede kullanıcıların Türkiye'deki şehirler ve seyahat planları hakkında soru sorabildiği bir sohbet asistanı oluşturdum. Asistan; KampRota'nın sabit fiyat, tesis, rezervasyon, güvenlik ve rota belgelerini RAG yaklaşımıyla kullanıyor. Güncel hava durumu sorularında ise şehir adını koordinata çevirip Open-Meteo API üzerinden canlı veri alıyor.

Çalışmanın öne çıkan özellikleri:

- DeepSeek API ile çalışan AI Agent
- Keyword tabanlı RAG ve belge kaynak gösterimi
- Simple Memory ile takip sorularını hatırlama
- Türkiye'deki şehirler için canlı hava durumu sorgusu
- İki şehir veya rota arasında karşılaştırma modu
- Bütçe, karavan uzunluğu, evcil hayvan ve hava durumuna göre gezi planı
- HTML tabanlı rapor ve PDF'e dönüştürülebilen çıktı
- Gmail SMTP ile e-posta gönderimi için opsiyonel entegrasyon denemesi

E-posta entegrasyonunda Gmail'in normal şifreyi kabul etmediğini gördüm. Bu nedenle App Password gerektiren SMTP adımını varsayılan akıştan ayrı tuttum. Böylece API anahtarlarını ve hesap bilgilerini projeye eklemeden güvenli bir demo akışı elde ettim.

Bu projede benim için en önemli kazanım, sabit bilgi ile canlı veriyi birbirinden ayırmak oldu. Modelin her soruya tahminle cevap vermesi yerine, sabit kuralları belgelerden; güncel hava durumunu ise canlı araçlardan almasını sağladım. Ayrıca dosya çıktısı üretirken PDF zincirinin sohbet cevabını boşaltmaması için çıktı akışını ayrı ele aldım.

Proje klasörü:

https://github.com/GamzeNurAslan/shining-stars-learning-journey/tree/main/Week-08-n8n-RAG-AI-Agents

Görüş ve önerilerinizi memnuniyetle alırım.

İyi çalışmalar,

Gamze Nur Aslan
