\# Kargo GÃ¶nderi ETL Pipeline



Bu projede, kargo gÃ¶nderi verilerinin uÃ§tan uca bir veri mÃ¼hendisliÄŸi akÄ±ÅŸÄ± iÃ§inde iÅŸlenmesini amaÃ§ladÄ±m. SÃ¼reÃ§; sentetik veri Ã¼retimi, veri keÅŸfi, temizleme, hatalÄ± kayÄ±tlarÄ±n karantinaya alÄ±nmasÄ±, PostgreSQL'e yÃ¼kleme, idempotent veri aktarÄ±mÄ± ve veri kalite kontrollerinden oluÅŸuyor.



\## Proje AkÄ±ÅŸÄ±



```text

Faker

&#x20; â†“

gonderiler\_faker.csv

&#x20; â†“

Pandas ile Veri KeÅŸfi

&#x20; â†“

Veri Temizleme

&#x20; â”œâ”€â”€ gonderiler\_temiz.csv

&#x20; â””â”€â”€ gonderiler\_karantina.csv

&#x20; â†“

SQLAlchemy

&#x20; â†“

PostgreSQL

&#x20; â†“

Idempotent Load

&#x20; â†“

Great Expectations

```



\## KullanÄ±lan Teknolojiler



\* Python

\* Pandas

\* Faker

\* Docker

\* PostgreSQL

\* SQLAlchemy

\* psycopg2

\* Great Expectations



\## Proje DosyalarÄ±



```text

kargo-etl-odevi/

â”‚

â”œâ”€â”€ docker-compose.yml

â”œâ”€â”€ generate\_data.py

â”œâ”€â”€ kesfet.py

â”œâ”€â”€ temizle.py

â”œâ”€â”€ yukle.py

â”œâ”€â”€ hata\_uret.py

â”œâ”€â”€ idempotent\_yukle.py

â”œâ”€â”€ kalite\_kontrol.py

â”‚

â”œâ”€â”€ gonderiler\_faker.csv

â”œâ”€â”€ gonderiler\_temiz.csv

â”œâ”€â”€ gonderiler\_karantina.csv

â”‚

â””â”€â”€ README.md

```



\## 1. PostgreSQL OrtamÄ±nÄ±n Docker ile KurulmasÄ±



PostgreSQL veritabanÄ±nÄ± bilgisayara doÄŸrudan kurmak yerine Docker container iÃ§erisinde Ã§alÄ±ÅŸtÄ±rdÄ±m.



Bu yapÄ± sayesinde veritabanÄ± ortamÄ± proje ile birlikte kolayca tekrar oluÅŸturulabilir hale geldi.



KullandÄ±ÄŸÄ±m temel kavramlar:



\* \*\*Image:\*\* PostgreSQL'in Ã§alÄ±ÅŸmasÄ± iÃ§in kullanÄ±lan hazÄ±r Docker ÅŸablonu.

\* \*\*Container:\*\* Image'Ä±n Ã§alÄ±ÅŸan Ã¶rneÄŸi.

\* \*\*Port Mapping:\*\* Container iÃ§erisindeki PostgreSQL portunun bilgisayardan eriÅŸilebilir hale getirilmesi.

\* \*\*Volume:\*\* Container silinse bile veritabanÄ± verilerinin kalÄ±cÄ± olmasÄ±nÄ± saÄŸlayan depolama alanÄ±.



PostgreSQL iÃ§in `postgres:16` image'Ä± kullanÄ±ldÄ± ve servis `5432` portu Ã¼zerinden Ã§alÄ±ÅŸtÄ±rÄ±ldÄ±.



\## 2. Faker ile Sentetik Veri Ãœretimi



GerÃ§ek kullanÄ±cÄ± veya ÅŸirket verisi kullanmak yerine Faker ile sentetik kargo verileri oluÅŸturdum.



```python

fake = Faker("tr\_TR")

Faker.seed(42)

random.seed(42)

```



Veri setinde ÅŸu alanlar bulunuyor:



\* `gonderi\_id`

\* `sube\_kodu`

\* `alici\_sehir`

\* `agirlik\_kg`

\* `durum`

\* `kabul\_tarihi`

\* `teslim\_tarihi`



BaÅŸlangÄ±Ã§ta 5000 temel kayÄ±t Ã¼retildi ve veri temizleme sÃ¼recini test edebilmek iÃ§in bilinÃ§li olarak problemli veriler eklendi.



Bunlar arasÄ±nda:



\* Duplicate kayÄ±tlar

\* Eksik ÅŸehir bilgileri

\* Eksik aÄŸÄ±rlÄ±k deÄŸerleri

\* Negatif veya sÄ±fÄ±r aÄŸÄ±rlÄ±klar

\* Teslim tarihinin kabul tarihinden Ã¶nce olduÄŸu kayÄ±tlar

\* FarklÄ± biÃ§imlerde yazÄ±lmÄ±ÅŸ Ä°stanbul deÄŸerleri



bulunuyor.



Son durumda ham veri seti:



```text

Toplam satÄ±r: 5050

Duplicate: 50

Eksik ÅŸehir: 26

Eksik aÄŸÄ±rlÄ±k: 12

```



\## 3. Veri KeÅŸfi



Ham veri `kesfet.py` dosyasÄ± ile Pandas kullanÄ±larak incelendi.



Kontrol edilen baÅŸlÄ±ca noktalar:



```python

df.head()

df.shape

df.info()

df.isnull().sum()

df.describe()

df.duplicated().sum()

```



Bu aÅŸamada veri setindeki eksik deÄŸerler, veri tipleri, negatif aÄŸÄ±rlÄ±klar ve tekrar eden satÄ±rlar gÃ¶rÃ¼nÃ¼r hale geldi.



Ã–rneÄŸin aÄŸÄ±rlÄ±k alanÄ±nda minimum deÄŸer:



```text

\-3.5 kg

```



olarak tespit edildi. Bu durum verinin temizleme aÅŸamasÄ±ndan geÃ§mesi gerektiÄŸini gÃ¶sterdi.



\## 4. Veri Temizleme ve Karantina



Temizleme iÅŸlemleri `temizle.py` iÃ§erisinde gerÃ§ekleÅŸtirildi.



Ä°lk olarak duplicate kayÄ±tlar kaldÄ±rÄ±ldÄ±:



```text

BaÅŸlangÄ±Ã§ satÄ±r sayÄ±sÄ±: 5050

Duplicate temizliÄŸi sonrasÄ±: 5000

```



Daha sonra veri kalite kurallarÄ±nÄ± saÄŸlamayan kayÄ±tlar doÄŸrudan silinmek yerine ayrÄ± bir karantina veri setine alÄ±ndÄ±.



SonuÃ§:



```text

Temiz veri satÄ±r sayÄ±sÄ±: 4903

Karantinaya ayrÄ±lan: 97

```



Karantina nedenleri:



| Problem                             | KayÄ±t SayÄ±sÄ± |

| ----------------------------------- | -----------: |

| GeÃ§ersiz aÄŸÄ±rlÄ±k                    |           40 |

| Eksik alÄ±cÄ± ÅŸehri                   |           25 |

| Teslim tarihi kabul tarihinden Ã¶nce |           20 |

| Eksik aÄŸÄ±rlÄ±k                       |           12 |

| \*\*Toplam\*\*                          |       \*\*97\*\* |



Karantinaya alÄ±nan kayÄ±tlar:



```text

gonderiler\_karantina.csv

```



dosyasÄ±nda saklandÄ±.



Bu yÃ¶ntem sayesinde hatalÄ± veriler kaybolmadan daha sonra incelenebilir durumda tutuldu.



\## 5. TÃ¼rkÃ§e Karakter Standardizasyonu



Veri temizleme sÄ±rasÄ±nda Ã¶zellikle TÃ¼rkÃ§e `I`, `Ä°`, `i` dÃ¶nÃ¼ÅŸÃ¼mlerinin beklenmeyen sonuÃ§lar oluÅŸturabileceÄŸini gÃ¶zlemledim.



Ã–rneÄŸin ÅŸu deÄŸerlerin aynÄ± ÅŸehri ifade etmesi gerekiyordu:



```text

ISTANBUL

Ä°STANBUL

Istanbul

istanbul

Ä°stanbul

```



Bu nedenle ÅŸehir deÄŸerleri kontrollÃ¼ bir eÅŸleme kullanÄ±larak standart hale getirildi:



```text

Ä°stanbul

```



Bu adÄ±m Ã¶zellikle TÃ¼rkÃ§e karakter iÃ§eren metinlerde yalnÄ±zca standart `lower()` kullanÄ±mÄ±nÄ±n her zaman yeterli olmayabileceÄŸini gÃ¶sterdi.



\## 6. Temiz Verinin PostgreSQL'e YÃ¼klenmesi



Temizlenen veri SQLAlchemy aracÄ±lÄ±ÄŸÄ±yla PostgreSQL'e aktarÄ±ldÄ±.



Son yÃ¼kleme sonucunda:



```text

CSV satÄ±r sayÄ±sÄ±: 4903

Benzersiz gonderi\_id: 4903

PostgreSQL satÄ±r sayÄ±sÄ±: 4903

```



elde edildi.



BÃ¶ylece temiz CSV ile veritabanÄ±ndaki kayÄ±t sayÄ±sÄ±nÄ±n aynÄ± olduÄŸu doÄŸrulandÄ±.



\## 7. Bilerek Duplicate Problemi OluÅŸturma



Pipeline'Ä±n tekrar Ã§alÄ±ÅŸtÄ±rÄ±ldÄ±ÄŸÄ±nda ne olacaÄŸÄ±nÄ± gÃ¶rmek iÃ§in veriyi PostgreSQL'e `append` yÃ¶ntemi ile iki kez yÃ¼kledim.



Ä°lk Ã§alÄ±ÅŸtÄ±rmada veritabanÄ±nda:



```text

4903

```



kayÄ±t bulunurken aynÄ± yÃ¼kleme ikinci kez yapÄ±ldÄ±ÄŸÄ±nda:



```text

9806

```



kayÄ±t oluÅŸtu.



Bu test, veri pipeline'larÄ±nda sadece kodun baÅŸarÄ±lÄ± Ã§alÄ±ÅŸmasÄ±nÄ±n yeterli olmadÄ±ÄŸÄ±nÄ± gÃ¶sterdi.



AynÄ± verinin tekrar iÅŸlenmesi veritabanÄ±nda duplicate kayÄ±t oluÅŸmasÄ±na neden olabiliyor.



Bu problemi Ã§Ã¶zmek iÃ§in idempotent bir yÃ¼kleme yaklaÅŸÄ±mÄ±na geÃ§tim.



\## 8. Idempotent Veri YÃ¼kleme



Idempotency, aynÄ± iÅŸlemin birden fazla kez Ã§alÄ±ÅŸtÄ±rÄ±lmasÄ± durumunda sistemin sonucunun deÄŸiÅŸmemesi anlamÄ±na gelir.



Bunun iÃ§in:



\* `gonderi\_id` alanÄ± primary key olarak tanÄ±mlandÄ±.

\* PostgreSQL `ON CONFLICT` yapÄ±sÄ± kullanÄ±ldÄ±.

\* AynÄ± `gonderi\_id` tekrar geldiÄŸinde yeni duplicate kayÄ±t oluÅŸturmak yerine mevcut kayÄ±t gÃ¼ncellendi.



Final Faker veri seti ile test sonucu:



\### Ä°lk Ã§alÄ±ÅŸtÄ±rma



```text

CSV satÄ±r sayÄ±sÄ±: 4903

VeritabanÄ±ndaki toplam satÄ±r: 4903

Idempotent yÃ¼kleme tamamlandÄ±.

```



\### Ä°kinci Ã§alÄ±ÅŸtÄ±rma



```text

CSV satÄ±r sayÄ±sÄ±: 4903

VeritabanÄ±ndaki toplam satÄ±r: 4903

Idempotent yÃ¼kleme tamamlandÄ±.

```



Yani:



```text

4903 â†’ 4903

```



Veri iki kez iÅŸlense bile duplicate oluÅŸmadÄ±.



\## 9. Veri Kalite Kontrolleri



Son aÅŸamada Great Expectations kullanÄ±larak temiz veri Ã¼zerinde otomatik kontroller gerÃ§ekleÅŸtirildi.



Kontrol edilen kurallar:



\* SatÄ±r sayÄ±sÄ±nÄ±n beklenen deÄŸerle eÅŸleÅŸmesi

\* `gonderi\_id` deÄŸerlerinin boÅŸ olmamasÄ±

\* `sube\_kodu` deÄŸerlerinin boÅŸ olmamasÄ±

\* `alici\_sehir` deÄŸerlerinin boÅŸ olmamasÄ±

\* `agirlik\_kg` deÄŸerlerinin boÅŸ olmamasÄ±

\* AÄŸÄ±rlÄ±k deÄŸerlerinin pozitif olmasÄ±



Final sonuÃ§:



```text

\[PASS] Satir sayisi 4903 olmali

\[PASS] gonderi\_id bos olmamali

\[PASS] sube\_kodu bos olmamali

\[PASS] alici\_sehir bos olmamali

\[PASS] agirlik\_kg bos olmamali

\[PASS] agirlik\_kg pozitif olmali



Tum veri kalite kontrolleri basarili.

```



\## KarÅŸÄ±laÅŸtÄ±ÄŸÄ±m Hatalar ve Ã–ÄŸrendiklerim



\### PostgreSQL baÄŸlantÄ±sÄ±nÄ±n reddedilmesi



Pipeline'Ä± tekrar Ã§alÄ±ÅŸtÄ±rÄ±rken ÅŸu hatayla karÅŸÄ±laÅŸtÄ±m:



```text

connection to server at "localhost", port 5432 failed:

Connection refused

```



Ä°lk olarak Python veya SQLAlchemy kodunda problem olduÄŸunu dÃ¼ÅŸÃ¼ndÃ¼m ancak `docker ps` Ã§Ä±ktÄ±sÄ±nÄ± kontrol ettiÄŸimde PostgreSQL container'Ä±nÄ±n Ã§alÄ±ÅŸmadÄ±ÄŸÄ±nÄ± fark ettim.



```bash

docker compose up -d

```



ile container'Ä± yeniden baÅŸlattÄ±ktan sonra baÄŸlantÄ± baÅŸarÄ±lÄ± ÅŸekilde kuruldu.



Bu hata bana bir pipeline probleminde yalnÄ±zca uygulama kodunu deÄŸil, baÄŸlÄ± olduÄŸu servislerin durumunu da kontrol etmenin Ã¶nemli olduÄŸunu gÃ¶sterdi.



\### YanlÄ±ÅŸ kaynak CSV kullanÄ±lmasÄ±



Faker ile yeni veri oluÅŸturduktan sonra keÅŸif scriptinin bir sÃ¼re eski `gonderiler.csv` dosyasÄ±nÄ± okumaya devam ettiÄŸini fark ettim.



Duplicate ve null deÄŸer sayÄ±larÄ±nÄ±n beklediÄŸim sonuÃ§larla uyuÅŸmamasÄ± sayesinde problemi tespit ettim.



Kaynak:



```python

gonderiler.csv

```



yerine:



```python

gonderiler\_faker.csv

```



olarak deÄŸiÅŸtirildi.



Bu durum pipeline'Ä±n farklÄ± aÅŸamalarÄ±nÄ±n aynÄ± veri kaynaÄŸÄ± ile Ã§alÄ±ÅŸtÄ±ÄŸÄ±nÄ±n doÄŸrulanmasÄ±nÄ±n Ã¶nemli olduÄŸunu gÃ¶sterdi.



\### `read\_csv()` kullanÄ±m hatasÄ±



Kaynak dosyayÄ± deÄŸiÅŸtirirken yanlÄ±ÅŸlÄ±kla ÅŸu yapÄ±yÄ± oluÅŸturdum:



```python

df = pd.read\_csv(df = pd.read\_csv(...))

```



ve:



```text

TypeError: read\_csv() got an unexpected keyword argument 'df'

```



hatasÄ±nÄ± aldÄ±m.



SatÄ±rÄ± tek bir `pd.read\_csv()` Ã§aÄŸrÄ±sÄ± olacak ÅŸekilde dÃ¼zelttikten sonra iÅŸlem baÅŸarÄ±yla devam etti.



\### Duplicate veri problemi



`append` ile Ã§alÄ±ÅŸan yÃ¼kleme iÅŸleminin iki kez Ã§alÄ±ÅŸtÄ±rÄ±lmasÄ± kayÄ±t sayÄ±sÄ±nÄ± iki katÄ±na Ã§Ä±kardÄ±.



Bu problem primary key ve `ON CONFLICT` yaklaÅŸÄ±mÄ± ile Ã§Ã¶zÃ¼ldÃ¼.



BÃ¶ylece pipeline tekrar Ã§alÄ±ÅŸtÄ±rÄ±labilir ve gÃ¼venli hale getirildi.



\### Eksik veriyi doÄŸrudan silmemek



Eksik veya mantÄ±ksal olarak hatalÄ± kayÄ±tlarÄ± doÄŸrudan silmek yerine nedenleri ile birlikte karantina dosyasÄ±na aktarmanÄ±n daha doÄŸru bir yaklaÅŸÄ±m olduÄŸunu gÃ¶rdÃ¼m.



Bu sayede hem temiz veri seti oluÅŸturuldu hem de problemli kayÄ±tlarÄ±n izlenebilirliÄŸi korundu.



\## Projeyi Ã‡alÄ±ÅŸtÄ±rma



Docker servislerini baÅŸlatmak iÃ§in:



```bash

docker compose up -d

```



Sanal ortamÄ± aktifleÅŸtirmek iÃ§in:



```powershell

.venv\\Scripts\\activate

```



Sentetik veri Ã¼retmek iÃ§in:



```bash

python generate\_data.py

```



Veriyi keÅŸfetmek iÃ§in:



```bash

python kesfet.py

```



Veriyi temizlemek iÃ§in:



```bash

python temizle.py

```



PostgreSQL'e yÃ¼klemek iÃ§in:



```bash

python yukle.py

```



Idempotent yÃ¼klemeyi Ã§alÄ±ÅŸtÄ±rmak iÃ§in:



```bash

python idempotent\_yukle.py

```



Veri kalite kontrollerini Ã§alÄ±ÅŸtÄ±rmak iÃ§in:



```bash

python kalite\_kontrol.py

```



\## SonuÃ§



Bu projede yalnÄ±zca bir CSV dosyasÄ±nÄ± temizlemek yerine kÃ¼Ã§Ã¼k Ã¶lÃ§ekli bir veri pipeline'Ä±nÄ± uÃ§tan uca oluÅŸturdum.



Ham verinin Ã¼retiminden baÅŸlayarak veri keÅŸfi, temizleme, karantina yaklaÅŸÄ±mÄ±, PostgreSQL entegrasyonu, duplicate problemi, idempotent yÃ¼kleme ve otomatik veri kalite kontrollerini uygulamalÄ± olarak deneyimledim.



En Ã¶nemli Ã§Ä±karÄ±mlarÄ±mdan biri, veri mÃ¼hendisliÄŸinde baÅŸarÄ±lÄ± bir pipeline'Ä±n yalnÄ±zca â€œÃ§alÄ±ÅŸanâ€ deÄŸil; \*\*tekrar Ã§alÄ±ÅŸtÄ±rÄ±labilir, kontrol edilebilir ve hatalara karÅŸÄ± gÃ¼venilir\*\* olmasÄ± gerektiÄŸi oldu.



