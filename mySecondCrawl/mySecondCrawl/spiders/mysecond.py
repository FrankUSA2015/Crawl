# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
from mySecondCrawl.items import commintItem
import traceback#处理异常的

class MysecondSpider(scrapy.Spider):
    name = 'mysecond'
    allowed_domains = ['github.com']
    # file1 = open(r'', 'r')#每次需要修改的地方
    # start_urls = json.load(file1)
    start_urls = ["https://github.com/ushahidi/Ushahidi_Web/commit/e0e2b66?diff=split","https://github.com/Dolibarr/dolibarr/commit/63820ab37537fdff842539425b2bf2881f0d8e91?diff=split","https://github.com/sefrengo-cms/sefrengo-1.x/commit/0b1edd4b22a47743eff7cfaf884ba2a4e06e15eb?diff=split","https://github.com/boxug/trape/commit/628149159ba25adbfc29a3ae1d4b10c7eb936dd3?diff=split","https://github.com/rails/rails/commit/8a39f411dc3c806422785b1f4d5c7c9d58e4bf85?diff=split"]#验证try是否写对
    #start_urls = ['https://github.com/wgm/cerb/commit/12de87ff9961a4f3ad2946c8f47dd0c260607144?diff=split']
    #start_urls =['https://github.com/revive-adserver/revive-adserver/commit/ecbe822b48ef4ff61c2c6357c0c94199a81946f4?diff=split']
    #start_urls = ["https://github.com/semplon/GeniXCMS/commit/d885eb20006099262c0278932b9f8aca3c1ac97f?diff=split"]

    def merage(self,needList):
        temporary = []
        code = {}
        n = 0
        listNum = len(needList)
        while listNum:
            for dat1 in needList:
                dat1["flage"] = 0
            code = needList[0]
            n = n + 1
            del needList[0]
            if len(needList) != 0:
                for dat2 in needList:
                    if code['addNum'] == 1 and code['detelNum'] == 1:  # 判断code是否是一行
                        if dat2['addNum'] == 1 and dat2['detelNum'] == 1:
                            if code['relatePrePosition'] - dat2['relatePrePosition'] == 1:
                                code['detelCodeContent'] = dat2['detelCodeContent'] + code['detelCodeContent']
                                code['addCodeContent'] = dat2['addCodeContent'] + code['addCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['addNum'] = code['addNum'] + 1
                                code['relatePrePosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                            elif dat2['relatePrePosition'] - code['relatePrePosition'] == 1:
                                code['detelCodeContent'] = code['detelCodeContent'] + dat2['detelCodeContent']
                                code['addCodeContent'] = code['addCodeContent'] + dat2['addCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['addNum'] = code['addNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                        elif dat2['addNum'] == 0 and dat2['detelNum'] == 1:
                            if dat2['relatePrePosition'] - code['relatePrePosition'] == 1:
                                code['detelCodeContent'] = code['detelCodeContent'] + dat2['detelCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                        elif dat2['detelNum'] == 0 and dat2['addNum'] == 1:
                            if dat2['relatePrePosition'] - code['relatePrePosition'] == 1:
                                code['addCodeContent'] = code['addCodeContent'] + dat2['addCodeContent']
                                code['addNum'] = code['addNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1

                    elif code['detelNum'] >= 1 and code['addNum'] == 0:
                        if dat2['addNum'] == 0 and dat2['detelNum'] == 1:
                            if dat2['relatePrePosition'] - code['relateNextPosition'] == 1:
                                code['detelCodeContent'] = code['detelCodeContent'] + dat2['detelCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1

                    elif code['detelNum'] == 0 and code['addNum'] >= 1:
                        if dat2['addNum'] == 1 and dat2['detelNum'] == 0:
                            if dat2['relatePrePosition'] - code['relateNextPosition'] == 1:
                                code['addCodeContent'] = code['addCodeContent'] + dat2['addCodeContent']
                                code['addNum'] = code['addNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1

                    elif code['detelNum'] > 1 and code['addNum'] > 1 and code['detelNum'] > code['addNum']:
                        if dat2['addNum'] == 1 and dat2['detelNum'] == 1:
                            if code['relatePrePosition'] - dat2['relatePrePosition'] == 1:
                                code['detelCodeContent'] = dat2['detelCodeContent'] + code['detelCodeContent']
                                code['addCodeContent'] = dat2['addCodeContent'] + code['addCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['addNum'] = code['addNum'] + 1
                                code['relatePrePosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                        elif dat2['addNum'] == 0 and dat2['detelNum'] == 1:
                            if dat2['relatePrePosition'] - code['relateNextPosition'] == 1:
                                code['detelCodeContent'] = code['detelCodeContent'] + dat2['detelCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                    elif code['detelNum'] > 1 and code['addNum'] > 1 and code['addNum'] > code['detelNum']:
                        if dat2['addNum'] == 1 and dat2['detelNum'] == 1:
                            if code['relatePrePosition'] - dat2['relatePrePosition'] == 1:
                                code['detelCodeContent'] = dat2['detelCodeContent'] + code['detelCodeContent']
                                code['addCodeContent'] = dat2['addCodeContent'] + code['addCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['addNum'] = code['addNum'] + 1
                                code['relatePrePosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                        elif dat2['addNum'] == 1 and dat2['detelNum'] == 0:
                            if dat2['relatePrePosition'] - code['relateNextPosition'] == 1:
                                code['addCodeContent'] = code['addCodeContent'] + dat2['addCodeContent']
                                code['addNum'] = code['addNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1

                    elif code['detelNum'] > 1 and code['addNum'] > 1 and code['addNum'] == code['detelNum']:
                        if dat2['addNum'] == 1 and dat2['detelNum'] == 1:
                            if code['relatePrePosition'] - dat2['relatePrePosition'] == 1:
                                code['detelCodeContent'] = dat2['detelCodeContent'] + code['detelCodeContent']
                                code['addCodeContent'] = dat2['addCodeContent'] + code['addCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['addNum'] = code['addNum'] + 1
                                code['relatePrePosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                            elif dat2['relatePrePosition'] - code['relateNextPosition'] == 1:
                                code['detelCodeContent'] = code['detelCodeContent'] + dat2['detelCodeContent']
                                code['addCodeContent'] = code['addCodeContent'] + dat2['addCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['addNum'] = code['addNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                        elif dat2['addNum'] == 0 and dat2['detelNum'] == 1:
                            if dat2['relatePrePosition'] - code['relateNextPosition'] == 1:
                                code['detelCodeContent'] = code['detelCodeContent'] + dat2['detelCodeContent']
                                code['detelNum'] = code['detelNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1
                        elif dat2['detelNum'] == 0 and dat2['addNum'] == 1:
                            if dat2['relatePrePosition'] - code['relateNextPosition'] == 1:
                                code['addCodeContent'] = code['addCodeContent'] + dat2['addCodeContent']
                                code['addNum'] = code['addNum'] + 1
                                code['relateNextPosition'] = dat2['relatePrePosition']
                                dat2["flage"] = 1

            temporary.append(code)
            if len(needList):
                reList = []
                for dat3 in needList:
                    reList.append(dat3)
                for dat4 in needList:
                    if dat4["flage"] == 1:
                        reList.remove(dat4)
                needList = reList
            listNum = len(needList)
        return temporary

    def merageCodeFunction(self,function, code):  # 合并函数名字和代码,
        functionList = []
        for dat1 in code:  # 提取出每段代码,找到每个函数对应的代码
            dat1['funposit'] = '0'
            for dat2 in function:  # 提取出每个函数
                if int(dat1['relatePrePosition']) >= int(dat2['relatePosition']):
                    if int(dat1['funposit']) <= int(dat2['relatePosition']):
                        dat1['funposit'] = dat2['relatePosition']
        for dat3 in function:  # 把函数和代码进行组合
            funCodelist = []
            funCodelist1 = []
            for dat4 in code:
                if dat4['funposit'] == dat3['relatePosition']:  # 找到是这个函数对应的代码
                    funCodelist.append(dat4)
            for dat5 in funCodelist:  # 对找到的代码进行提取只要增加的或者是减少的代码
                codefix = {}
                codefix['deletCode'] = dat5['detelCodeContent']
                codefix['addCode'] = dat5['addCodeContent']
                funCodelist1.append(codefix)
            dat3['codelist'] = funCodelist1
            del dat3['relatePosition']
            functionList.append(dat3)

        return functionList

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        #print(response.text)
        commint = commintItem()
        error_list = []
        try:
            commint["commint_title"]=response.xpath('//p[@class="commit-title"]/text()').extract()[0].strip()#获得正常的文字并且去空格
            if len(response.xpath('//div[@class="commit-desc"]/pre/text()').extract())!= 0:
                commint["commint_desc"]=response.xpath('//div[@class="commit-desc"]/pre/text()').extract()[0]
            else:
                commint["commint_desc"] = "NULL"
            commint["commint_url"] = response.url.rstrip("?diff=split")
            doc_list=[]
            n=0

            for dat6 in soup.select('div.file-header.file-header--expandable.js-file-header'):#找到每个文件
                posit=0
                n=n+1
                dat1 =dat6.parent
                extrDoc= dat6#取文件名
                commitDoc ={}
                commitFuncList =[]
                commitDoc['docName']=extrDoc['data-path']
                print(commitDoc['docName'])
                temporaryFuncton = []
                temporaryAddDetelCode = []
                function_code1 = dat1.select('tbody')#提取函数和代码所在的框架j也就是tbody
                if len(function_code1):#判断是否找到
                    function_code=function_code1[0]
                    for dat2 in function_code.select('tr'):#获得每一行的加与减
                        posit=posit+1
                        if len(dat2.select('td.blob-code.blob-code-inner.blob-code-hunk')):
                            dat6=dat2.select('td.blob-code.blob-code-inner.blob-code-hunk')[0]
                            if dat6.parent['data-position'] != "":
                                funct = {}
                                funct['functionName'] = dat6.string
                                # funct['position'] = dat6.parent['data-position']
                                funct['relatePosition']=posit
                                print(dat6.string)
                                temporaryFuncton.append(funct)

                        if len(dat2.select('td.code-review.blob-code.blob-code-deletion'))!=0 or len(dat2.select('td.code-review.blob-code.blob-code-addition'))!=0:
                            codeAddDetel={}
                            if len(dat2.select('td.code-review.blob-code.blob-code-deletion'))!=0 :
                                dat3=dat2.select('td.code-review.blob-code.blob-code-deletion>span')[0]
                                codeAddDetel['detelCodeContent']=dat3.text
                                # codeAddDetel['detelCodePrePosition']=dat3['data-position']
                                # codeAddDetel['detelCodeNextPosition']= dat3['data-position']
                                codeAddDetel['detelNum'] = 1
                            else:
                                codeAddDetel['detelCodeContent'] = ""
                                # codeAddDetel['detelCodePrePosition'] = ""
                                # codeAddDetel['detelCodeNextPosition'] = ""
                                codeAddDetel['detelNum'] = 0
                            if len(dat2.select('td.code-review.blob-code.blob-code-addition'))!=0:
                                dat4=dat2.select('td.code-review.blob-code.blob-code-addition>span')[0]
                                codeAddDetel['addCodeContent']=dat4.text
                                # codeAddDetel['addCodePrePosition']=dat4['data-position']
                                # codeAddDetel['addCodeNextPosition']=dat4['data-position']
                                codeAddDetel['addNum'] = 1
                            else:
                                codeAddDetel['addCodeContent'] = ""
                                # codeAddDetel['addCodePrePosition'] = ""
                                # codeAddDetel['addCodeNextPosition'] = ""
                                codeAddDetel['addNum'] = 0
                            codeAddDetel['relatePrePosition']=posit
                            codeAddDetel['relateNextPosition']=posit
                            temporaryAddDetelCode.append(codeAddDetel)
                else:
                    error_list.append(commitDoc['docName'])

                if len(temporaryAddDetelCode):
                    temporaryAddDetelCode = self.merage(temporaryAddDetelCode)#合并代码
                if len(temporaryFuncton):#把代码和函数名合并
                    commitFuncList = self.merageCodeFunction(temporaryFuncton,temporaryAddDetelCode)

                    # n = n + 1
                    # print(str(n))
                    # file1 = open(r'E:\date\crawl_commint\text' + str(n) + '.json', 'w')
                    # json.dump(temporaryAddDetelCode, file1, indent=1)
                    # file1.close()
                    # file2 = open(r'E:\date\function_text\text_' + str(n) + '.json', 'w')
                    # json.dump(temporaryFuncton, file2, indent=1)
                    # file2.close()
                    # print("完成函数名：" + str(n))
                # print("完成：" + str(n))
                # n = n + 1
                # file1 = open(r'E:\date\crawl_commint\text' + str(n) + '.json', 'w')
                # json.dump(temporaryAddDetelCode, file1, indent=1)

                commitDoc['funclist']=commitFuncList
                doc_list.append(commitDoc)

            commint["possible_error_doc"] = error_list
            commint["commint_doc"] = doc_list # 这里对应的是一个列表
            yield commint
        except Exception as e:
            print("出现bug了！")
            str1=response.url.rstrip("?diff=split").replace('/','_').replace('https:__github.com','').lstrip()
            ff = open(r'', 'a')
            ff.write(response.url+'\n')
            traceback.print_exc(file=ff)  # 错误存储
            ff.close()

