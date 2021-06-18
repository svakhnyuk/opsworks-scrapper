Target Scrapper
===============
Version 0.1

Usage
-----

### Run scrapper
To use scrapper run next commands in project directory
* `scrapy crawl target --set FEED_URI=scraped_target_products.csv --set FEED_FORMAT=csv` -run spider crawler to store
*  items into scraped_target_product.csv file
* `scrapy crawl target` - run spider crawler to store items into database MongoDB configured in scrapy.cfg in 'mongod' section
