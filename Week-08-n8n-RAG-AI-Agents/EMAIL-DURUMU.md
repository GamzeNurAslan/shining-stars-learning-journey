# E-posta Entegrasyonu Durumu

KampRota gezi raporunu kullanıcı tarafından verilen bir e-posta adresine göndermek için n8n'deki **Send an Email** düğümü denendi.

## Karşılaşılan hatalar

### 1. DNS / SMTP host hatası

E-posta adresi SMTP host alanına yazıldığında `getaddrinfo ENOTFOUND` hatası alındı. Doğru SMTP host şu olmalıdır:

```text
smtp.gmail.com
```

### 2. Gmail giriş hatası

Sonraki denemede Gmail şu hatayı döndürdü:

```text
535-5.7.8 Username and Password not accepted
```

Gmail, normal hesap şifresiyle SMTP erişimine izin vermediği için e-posta düğümü varsayılan workflow'dan çıkarıldı.

## Gmail ile tekrar etkinleştirme

- Google hesabında iki adımlı doğrulamayı açın.
- Google Account -> Security -> App passwords bölümünden yeni bir uygulama şifresi oluşturun.
- n8n SMTP credential değerleri:

```text
Host: smtp.gmail.com
Port: 465
SSL/TLS: açık
Username: Gmail adresi
Password: Google App Password
```

Normal Gmail şifresi kullanılmamalıdır. API anahtarı veya App Password GitHub'a, README'ye ya da workflow JSON dosyasına yazılmamalıdır.

## Tasarım kararı

E-posta gönderimi isteğe bağlı bir özellik olarak bırakıldı. Böylece kullanıcı, SMTP hesabı tanımlamadan gezi asistanını, canlı hava durumunu, karşılaştırma modunu ve rapor üretimini kullanmaya devam edebilir.

