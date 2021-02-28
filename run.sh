pip install -r requirements.txt
rm Aldi.csv
scrapy crawl aldi -o Aldi.csv
python clean_up_csv.py