# -*- coding:utf8 -*-

# request
#     scrapy 1.3


import scrapy


class NxuNewsSpider(scrapy.Spider):
    name = "nnspider"

    def start_requests(self):
        urls = [
            'http://www.nxu.edu.cn/xxyw.htm',
            'http://www.nxu.edu.cn/xxyw/84.htm'
        ]

        for i in range(84):
            urls.append('http://www.nxu.edu.cn/xxyw/' + str(i) + '.htm')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.title_parse)

    def title_parse(self, response):
        for i in range(15):
            title = response.css("#line_u6_" + str(i) + " > a::text") \
                .extract_first()
            href = response.css("#line_u6_" + str(i) + " > a::attr(href)") \
                .extract_first()
            text_id = href[-8:]
            text_id = text_id[:4]
            self.log('>>> title_parse')
            self.log('>>> title : %s' % title)
            self.log('>>> href : %s' % href)
            if href.find('.') < 2:
                fixed_href = 'http://www.nxu.edu.cn' + href[2:]
            else:
                fixed_href = 'http://www.nxu.edu.cn/' + href
            self.log('>>> fixed href %s' % fixed_href)

            yield scrapy.Request(url=fixed_href,
                                 callback=self.content_parse,
                                 meta={'title': title, 'text_id': text_id})

    def content_parse(self, response):
        self.log(">>> content_parse :" + response.meta['title'])
        content = response.xpath('//*[@id="artibody"]/div[2]//text()')\
            .extract()
        self.log(">>> content_parse :" + response.meta['text_id'])
        self.log(">>> content_parse :")
        print(content)

        file_content = response.meta['title'] + ''.join(content)
        file_content = file_content.encode('utf-8')

        filename = 'E:/NNSE/origin_text/%s.txt' % response.meta['text_id']
        with open(filename, 'wb+') as f:
            f.write(file_content)
