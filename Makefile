# Kozbeyli Konağı — kads görev kısayolları
.PHONY: help install doctor build validate presence test clean

help:        ## Bu yardımı göster
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n",$$1,$$2}'

install:     ## kads'i düzenlenebilir kur (pip install -e .)
	pip install -e .

doctor:      ## Ortam + config teşhisi
	python3 -m kads doctor

build:       ## Google + Meta + SEO dosyalarını üret (campaigns/)
	python3 -m kads build all --out campaigns

validate:    ## RSA uzunluk + bütçe + CSV doğrulama
	python3 -m kads validate

presence:    ## Dijital varlık denetimi + düzeltmeler
	python3 -m kads presence

test:        ## Testleri çalıştır
	python3 -m pytest

clean:       ## __pycache__ ve out/ temizle
	rm -rf out **/__pycache__ .pytest_cache 2>/dev/null || true
