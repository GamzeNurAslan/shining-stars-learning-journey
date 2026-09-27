# Yayınlama ve gözlemlenebilirlik planı

## Cloudflare

İlk sürüm yerel JSON dosyası kullanır. Cloudflare'a geçerken `StateStore` katmanı bir Cloudflare storage binding'i ile değiştirilmelidir. Zamanlayıcı için `ends_at` değeri saklanır; her istek geldiğinde kalan süre `ends_at - şimdi` olarak hesaplanır. Böylece arka planda sürekli çalışan bir process gerekmeyebilir.

Cloudflare Python Workers tarafında `WorkerEntrypoint` ve `pywrangler` akışı bulunuyor. HTTP katmanı eklendiğinde agent çekirdeği aynı kalabilir. [Cloudflare Python Workers](https://developers.cloudflare.com/workers/languages/python/)

## Laminar

Laminar ile `FocusAgent.run`, LLM çağrısı ve her tool çağrısı ayrı trace olarak izlenebilir. Böylece agent'ın neden `plan_day` veya `timer_status` seçtiğini sunumda göstermek mümkün olur. [Laminar agent observability](https://laminar.sh/article/agent-observability)
