from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import ssl, os, codecs, re
from csv import writer
class StockCrawler:
    url = "https://trade.vndirect.com.vn/chung-khoan/phai-sinh"
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
        self.driver.get(self.url)
        time.sleep(3)
    
    def append_list_as_row(self,file_name, list_of_elem):
    # Open file in append mode
        with open(file_name, 'a+',encoding="UTF-8" ,newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            if os.stat(file_name).st_size == 0:
                csv_writer.writerow(["Ma_HD", "Date", "Time", "TC", "Tran", "San", "Do_lech", "KL_mo", "Du_mua_gia_3", "Du_mua_KL_3", "Du_mua_gia_2", "Du_mua_KL_2","Du_mua_gia_1", "Du_mua_KL_1", "Khop_lenh_gia", "Khop_lenh_KL","Khop_lenh +/-", "Du_ban_gia_1", "Du_ban_KL_1", "Du_ban_gia_2", "Du_ban_KL_2","Du_ban_gia_3", "Du_ban_KL_3", "Tong_KL", "Gia_mo_cưa", "Gia_cao", "Gia_thap", "DTNN_mua", "DTNN_Ban"])    

            csv_writer.writerow(list_of_elem)
    def check_valid_record(self, time_str):
        time_lst = time_str.split(":")
        num = int(time_lst[0])*60 + int(time_lst[1])
        if num in range(690,780) or num in range(871, 885) or (num < 540 or num > 900):
            return False
        return True
    def check_quit(self,time_str):
        time_lst = time_str.split(":")
        num = int(time_lst[0])*60 + int(time_lst[1])
        return num >= 900


    def crawl(self):
        file_lst=['VN30F1M', 'VN30F2M','VN30F1Q','VN30F2Q']
        codex_lst = []
        HD_elements = self.driver.find_elements_by_xpath("//td[@class = 'txtl']")
        for el in HD_elements:
            code_txt = el.text[0:9]
            codex_lst.append(code_txt)
        print(codex_lst)
        while True: 
            St_Date = self.driver.find_element_by_id("clock-date").text
            St_Time = self.driver.find_element_by_id("clock-time").text
            if(self.check_quit(St_Time) == True):
                sys.exit("Time over!")
            if( self.check_valid_record(St_Time) == True):
                for i in range(0,4):
                    testl = self.driver.find_elements_by_xpath("//tr[@class='derivative-row-"+ codex_lst[i]+"']//td")
                    final_t = self.driver.find_elements_by_xpath("//tr[@class='derivative-row-"+ codex_lst[i]+"']//span[@class ='cell-1-2 has-content']")
                    print(final_t)
                    test_t = []
                    
                    for j in range(2, len(testl) - 1):
                        test_t.append(testl[j].text.replace(',',''))

                    test_t.append(final_t[0].text)
                    test_t.append(final_t[1].text)
                    test_t.insert(0,St_Time[:-2]+ "00")
                    test_t.insert(0,St_Date)
                    test_t.insert(0,codex_lst[i])

                    self.append_list_as_row("csv_files/"+file_lst[i]+".csv",test_t )
                print(St_Time)
                time.sleep(60)

stcrawl = StockCrawler()
stcrawl.crawl()