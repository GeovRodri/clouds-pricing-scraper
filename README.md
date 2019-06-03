# Clouds Pricing Scraper

## Description

Scraper utilizado para pegar os valores dos principais provedores de clouds existentes.

### Instalação
```
# apt install chromium-bsu
# apt-get install -yq --no-install-recommends libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libnss3
$ pip install -r requirements.txt 
```

### Utilizando
```
$ python cli.py [all, azure, google, alibaba, oracle, aws]
```

### Iniciando API
```
$ python app.py
```

#### Exemplo de chamada para a API via POST
Body
```
{
	"select": {
		"aws": ["memory", "vcpu", "pricing.price"],
		"azure": ["RAM", "vCPU", "pricing.Pay as you go"]
	},
	"labels": ["Memoria", "CPU", "Preço"],
	"filters": [
		{"field": "CPU", "comparator": "==", "value": 4} 
	],
	"limit": 5
}
```
Retorno
```
[
    {
        "type": "i2.xlarge",
        "cloud": "aws",
        "Memoria": "30.5 GiB",
        "CPU": "4",
        "Preço": {
            "region": "South America (Sao Paulo)",
            "price": 0.02
        }
    },
    {
        "type": "m2.2xlarge",
        "cloud": "aws",
        "Memoria": "34.2 GiB",
        "CPU": "4",
        "Preço": {
            "region": "US West (Oregon)",
            "price": 0.025
        }
    },
    {
        "type": "m1.xlarge",
        "cloud": "aws",
        "Memoria": "15 GiB",
        "CPU": "4",
        "Preço": {
            "region": "US West (N. California)",
            "price": 0.05
        }
    },
    {
        "type": "B4MS",
        "cloud": "azure",
        "Memoria": "16 GiB",
        "CPU": "4",
        "Preço": {
            "region": "Germany Central",
            "price": 0.1175
        }
    },
    {
        "type": "B4MS",
        "cloud": "azure",
        "Memoria": "16 GiB",
        "CPU": "4",
        "Preço": {
            "region": "Germany Northeast",
            "price": 0.1175
        }
    }
]
```