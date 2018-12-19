# coding=utf-8

import time
import json
import traceback
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Qichacha(object):
    ''' 企查查操作模块 '''
    
    def __init__(self, username='', password=''):
        self._username = username
        self._password = password
        self._init_url = 'https://www.qichacha.com/'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self._init_url)

    def send_name(self, name):
        ''' 输入公司名字 '''
        time.sleep(2)
        try:
            send_name_xpath = '//input[@id="searchkey"]'
            send_name_ele = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, send_name_xpath))
            )
            send_name_ele.send_keys(u'%s'%name)
        except:
            return False

        try:
            search_btn_xpath = '//input[@id="V3_Search_bt"]'
            search_btn_ele = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, search_btn_xpath))
            )
            search_btn_ele.click()
        except:
            return False
        return True

    def get_all_company_name(self):
        ''' 获取所有的公司名字 '''
        try:
            while True:
                company_name_xpath = '//a[@class="ma_h1"]'
                companys_ele = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_all_elements_located((By.XPATH, company_name_xpath))
                )
                company_ele_list = []
                n = 0
                is_continue = False 
                for company_ele in companys_ele:
                    company_name = company_ele.text
                    if not company_name:
                        is_continue = True
                        break
                    print '%d: %s'%(n, company_name)
                    company_ele_list.append(company_ele)
                    n += 1
                if is_continue:
                    continue
                print company_ele_list
                return company_ele_list
        except:
            return [] 

    def open_company(self, ele):
        ''' 进入查询公司详情页面 '''
        time.sleep(1)
        try:
            current_handle = self.driver.current_window_handle
            print current_handle
            ele.click()
            handle_list = self.get_handle()
            if len(handle_list) >= 2:
                for h in handle_list:
                    if h != current_handle:
                        self.driver.switch_to.window(h)
        except:
            return False
        return True

    def close_page(self):
        ''' 关闭公司详情页面 '''
        self.driver.close()
        return True

    def get_handle(self):
        ''' 获取浏览器所有的句柄 '''
        handles = self.driver.window_handles
        return handles

    def back_page(self):
        ''' 返回上一页 '''
        handle_list = self.get_handle()
        print 'back_page_handle_list:', handle_list
        self.driver.switch_to_window(handle_list[0])
        self.driver.back()
        return True

    def get_detail_data(self):
        ''' 获取公司详细信息 '''
        print u'开始查询公司详情数据'
        print self.driver.title

        detail_data = {}

        # 公司名字
        title_xpath = '//div[@id="company-top"]/div/div[@class="content"]/\
            div[@class="row title jk-tip"]/h1'
        detail_data['title'] = self.response_text(title_xpath)

        # 电话号码
        phone_xpath = '//div[@id="company-top"]/div/div[@class="content"]/\
            div[3]/span[1]/span[2]/span/a'
        detail_data['phone'] = self.response_text(phone_xpath)

        # 官网
        website_xpath = '//div[@id="company-top"]/div/div[@class="content"]/\
            div[3]/span[3]/a'
        detail_data['website'] = self.response_text(website_xpath)

        # 地址 
        address_xpath = '//div[@id="company-top"]/div/div[@class="content"]/\
            div[4]/span[3]/a'
        detail_data['address_xpath'] = self.response_text(address_xpath)

        # 自身风险数
        self_risk_xpath = '//div[@class="risk-panel b-a"]/span/a[1]/span'
        detail_data['self_risk'] = self.response_text(self_risk_xpath)

        # 关联风险数
        associated_risk_xpath = '//div[@class="risk-panel b-a"]/span/a[2]/span'
        detail_data['associated_risk'] = self.response_text(associated_risk_xpath)

        # 老板
        boss_xpath = '//div[@class="boss-td"]/div[1]/div[2]/a/h2'
        detail_data['boss'] = self.response_text(boss_xpath)

        # 关联公司
        associated_company_xpath = '//a[@class="btouzi"]/span'
        detail_data['associated_company'] = self.response_text(associated_company_xpath)

        # 注册资本
        register_capital_xpath = '//section[@id="Cominfo"]/table[2]/tbody/\
            tr[1]/td[2]'
        detail_data['register_capital'] = self.response_text(register_capital_xpath)

        # 实际资本
        actual_capital_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[1]/td[4]'
        detail_data['actual_capital'] = self.response_text(actual_capital_xpath)

        # 经营状态
        management_state_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[2]/td[2]'
        detail_data['manage_state'] = self.response_text(management_state_xpath)

        # 成立日期
        establish_date_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[2]/td[4]'
        detail_data['estabish_date'] = self.response_text(establish_date_xpath)

        # 统一社会信用代码
        unified_society_credit_id_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]'
        detail_data['unified_society_credit_id'] = self.response_text(unified_society_credit_id_xpath)

        # 纳税人识别码
        taxpayer_id_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[3]/td[4]'
        detail_data['taxpayer_id'] = self.response_text(taxpayer_id_xpath)

        # 注册码 
        register_id_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[4]/td[2]'
        detail_data['register_id'] = self.response_text(register_id_xpath)

        # 组织机构代码
        organization_id_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[4]/td[4]' 
        detail_data['organization_id'] = self.response_text(organization_id_xpath)

        # 公司类型
        company_style_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[5]/td[2]'
        detail_data['company_style_xpath'] = self.response_text(company_style_xpath)

        # 所属行业
        industry_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[5]/td[4]'
        detail_data['industry'] = self.response_text(industry_xpath)

        # 核准日期
        verify_date_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[6]/td[2]'
        detail_data['verify_date'] = self.response_text(verify_date_xpath)

        # 登记机关
        register_organization_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[6]/td[4]'
        detail_data['register_organization'] = self.response_text(register_organization_xpath)

        # 所属地区
        belong_to_area_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[7]/td[2]'
        detail_data['belong_to_area'] = self.response_text(belong_to_area_xpath)

        # 曾用名
        ever_name_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[8]/td[2]'
        detail_data['ever_name'] = self.response_text(ever_name_xpath)

        # 参保人数
        join_ensure_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[8]/td[4]'
        detail_data['join_ensure'] = self.response_text(join_ensure_xpath)

        # 人员规模
        people_scale_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[9]/td[2]'
        detail_data['people_scale'] = self.response_text(people_scale_xpath)

        # 营业期限
        do_business_date_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[9]/td[4]'
        detail_data['do_business_date'] = self.response_text(do_business_date_xpath)

        # 经营范围
        business_range_xpath = '//section[@id="Cominfo"]/table[2]/tbody/tr[11]/td[2]'
        detail_data['business_range'] = self.response_text(business_range_xpath)

        return detail_data
        
    def response_text(self, data_xpath):
        ''' 返回xpath匹配的数据 '''
        try:
            current_ele = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, data_xpath))
            )
            data = (current_ele.text).encode('utf-8')

            print data
            return data
        except:
            return ''


if __name__ == '__main__':
    q = Qichacha()
    while True:
        company_name = raw_input("请输入公司名称：")
        name = u'%s'%(company_name)
        if q.send_name(name):
            company_ele_list = q.get_all_company_name()
            if len(company_ele_list) > 0:
                if q.open_company(company_ele_list[0]):
                    data = q.get_detail_data()
                    if data:
                        q.close_page()
                        q.back_page()
                        data_json = json.dumps(data, ensure_ascii=False)
                        with open('./data.json', 'ab') as f:
                            f.write(data_json + '\r')
            else:
                print u'没有查询到相关公司'
