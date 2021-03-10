import scrapy

class JobSpider(scrapy.Spider):
    name = 'ejob'
    start_urls = ["https://www.ethiojobs.net/search-results-jobs/?action=search&listing_type[equal]=Job&keywords[all_words]="]

    def parse(self, response):
        for table in response.css('table.table-responsive.table-striped.table-hover tbody.searchResultsJobs tr'):
            yield {
                'name': table.css('td h2 a::text').get().replace('\u2014','-').strip() ,
                'link': table.css('td h2 a').attrib['href'],
            }

        next_page = 'https://www.ethiojobs.net/search-results-jobs/'+response.css('ul.pagination.pagination-blue li')[-1].css('a').attrib.get('href')
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)