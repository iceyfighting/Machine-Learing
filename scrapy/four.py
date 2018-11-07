import scrapy
import re
from scrapy.selector import Selector
from first_scrapy.items import FirstScrapyItem
class Teacher(scrapy.Spider):
    name = "four"
    #allowed_domains=["ggglxy.scu.edu.cn"]
    i=0
    def start_requests(self):
        basic_url = "http://www.rong66.com/portal.php?mod=list&catid=4&page=%s"
        start,end =1,2
        for i in range(start,end):
            u = re.compile("%s")
            url = u.sub(str(i),basic_url)
            print(url)
            yield scrapy.http.Request(url,self.parse)
    def parse(self,response):
        item  = FirstScrapyItem()
        #一页中的所有老师信息
        for teacher in response.xpath('//*[@class="deanpiclicl deanlarge"]'):
            #print(teacher)
            href=teacher.xpath("./a/@href").extract_first()
            #print(href)
            #进入老师个人链接提取个人具体信息
            art_time = response.xpath('//*[@class="deannewtwonum"]/b/text()').extract_first()
            item['time']= re.compile("时间：(\S.*)").findall(art_time)[0]
            #print(item['time'])
            art_author =teacher.xpath('//*[@class="deanartavar"]/span/text()').extract_first()
            item['author'] = re.compile("作者:(\S.*)").findall(art_author)[0]
            art_viewc = response.xpath('//*[@class="deannewtwonum"]/span/text()').extract_first()
            item['viewc']= re.compile("阅读：(\d.*)").findall(art_viewc)[0]
            
            #print(item['viewc'])
            #print(item['author'])
            request=scrapy.http.Request(response.urljoin(href),callback=self.parse_desc)
            request.meta['item']=item
            yield request

    def parse_desc(self,response):
        item  = response.meta['item']
        #print(response.text)
        #print(item['author'])
        #获取文本的发表时间
        #art_time = response.xpath('//*[@class="shijian"]/text()').extract_first().strip()
        #获取时间的正则表达式
        #item['time'] = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}").findall(art_time)[0]
        #print(item['time'])
        #获取文本的来源
        #art_orifrom = response.xpath('//*[@class="shijian"]/text()').extract_first()
        #item['orifrom'] = re.compile("来源：(\S.*)").findall(art_orifrom)[0]
        #print(item['orifrom'])
        #获取文本的浏览数
        #item['viewc'] = response.xpath('//*[@class="wz_fbt2"]/span[4]/text()').extract_first()
        #print(item['viewc'])
        #获取文本的作者
        #item['author'] =response.xpath('//*[@id="i_art_main"]/content/p[5]/text()').extract_first()
        #print(item['author'])
        #获取文章标题
        item['title'] =response.xpath('//*[@class="ph"]/text()').extract_first()
        print(item['title'])
        #获取文章的摘要
        art_brief = response.xpath('//*[@class="s"]/div/text()').extract_first()
        #print(art_brief)
        item['brief'] = re.compile(": (\S.*)").findall(art_brief)[0]
        #print(item['brief'])
        #获取文章id
        #art_tid =response.xpath('/html/head/link[1]/@href').extract_first()
        #item['tid'] = re.compile("(\d+)$").findall(art_tid)[0]
        #print(item['tid'])
        #获取文章正文
        art_text_list=response.xpath('//*[@id="article_content"]/descendant::text()').extract()
        art_text = ""
        for text_item in art_text_list:
            text_item = text_item.strip().replace("\n","").replace("\r","")
 
            art_text = art_text+" "+text_item
        item["text"] = art_text
        #item['text']=response.xpath('//*[@id="i_art_main"]/descendant::text()').extract()
        #print(item['text'])
        
        #print("当前作者数:",i++)
        #art_text = response.xpath("//div[@class='in_content']/")
        #//*[@id="form1"]/div[2]/div[3]/div[4]/descendant::text()
        #print(art_text[0].xpath('string(.)').extract()[0].strip())
        #item['text']=response.xpath('')
        #print(art_text)
        #文章来源
        yield item