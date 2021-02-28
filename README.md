**Aldi crawler**
This is a Python Scrapy Spider to craw Aldi website Grocery menu

**Requirements:**
Python 3
scrapy
protego

- Instruction

- Clone the repo: git clone https://github.com/tdnam/aldi_crawler.git
- Navigate to repo </br>
  `cd aldi_crawler` </br>
  `cd spiders` </br>

- Run spider using following command (Note: Manually delete Aldi.csv if it exists before run) </br>
  `scrapy crawl aldi -o Aldi.csv`

Output will be written to Aldi.csv file