import os.path
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

### Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg==True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "\\" + driver_path,options=options)


### open site and login
def login():
    driver=set_driver("chromedriver.exe",False)
    # Webサイトを開く
    driver.get("https://secure.indeed.com/account/login?service=draw&hl=ja&co=JP&continue=https%3A%2F%2Femployers.indeed.com%2Fp%3Ftoken%3D")
    time.sleep(30)

    # read csv file
    csv_data = pd.read_csv('test_data1.csv', encoding="shift-jis")
    count = 0
    # required data for first page.
    name = csv_data.職種名
    category =csv_data.職種カテゴリー
    company = csv_data.雇用企業名
    place = csv_data.勤務地

    # required data for second page
    job_style = csv_data.雇用形態
    salary_1 = csv_data.給与最小
    salary_2 = csv_data.給与最大
    salary_style = csv_data.給与体系
    description = csv_data.説明

    # required data for third page
    # these items are given directly　今はプログラムの中で直接渡している（下記2つ）
    # apply_email = csv_data.mada
    # apply_phone = csv_data.mada

    ### page 1 data entry
    # job title
    job_name = driver.find_element_by_id('JobTitle')
    job_name.clear()
    job_name.send_keys(name[count])
    print(name[count])

    # job category selection
    job_category = driver.find_element_by_id('japan-cmiJobCategory')
    for option in job_category.find_elements_by_tag_name('option'):
        print(option.text)
        if option.text == category[count]:
            option.click()
            print('clicked: ', category[count])
            break
        # else:
        #     option.text = category[count]

    # company name
    company_name = driver.find_element_by_id('JobCompanyName')
    company_name.clear()
    company_name.send_keys(company[count])

    # job location
    job_place = driver.find_element_by_id('cityOrPostalCode')
    job_place.clear()
    job_place.send_keys(place[count])

    time.sleep(5)

    # continue button click
    # this worked!!!
    btn_next = driver.find_element_by_xpath('//*[@id="sheet-next-button"]/span/a')
    btn_next.click()

    time.sleep(5)

    ### page 2 data entry
    # get job type(from radio buttons) ## this is not working yet and just given full time only 
    # 今は手動で渡している　※やり方分からなかった
    btn_select_job_type = driver.find_element_by_id('label-FULLTIME')
    btn_select_job_type.click()

    # salary range
    # 以下もcsvぁｒ読み込むときエラーになったので一旦手動で渡しています。
    start_salary = driver.find_element_by_id('salary1')
    start_salary.clear()
    start_salary.send_keys('300000')

    end_salary = driver.find_element_by_id('salary2')
    end_salary.clear()
    end_salary.send_keys('500000')

    # salary base- monthly, yearly....
    salary_base = driver.find_element_by_id('salaryPeriod')
    for option in salary_base.find_elements_by_tag_name('option'):
        if option.text == salary_style[count]:
            option.click()
            print(salary_style[count])
            break

    job_description = driver.find_element_by_id('description-editor-What_ifr')
    job_description.send_keys(description[count])

    #　以下は今オプショナルとして使ていない
    # job_appeal_point = driver.find_element_by_id('description-editorEMPLOYER_MESSAGE_ifr')
    # job_appeal_point.send_keys('best job ever!!')

    # job_hour = driver.find_element_by_id('description-editorSHIFT_ifr')
    # job_hour.send_keys('this is a week day job from 9am to 17pm')

    # job_place = driver.find_element_by_id('description-editorWORK_LOCATION_ifr')
    # job_place.send_keys('this is a work in saitama area.')

    # job_welfare = driver.find_element_by_id('description-editorBENEFITS_ifr')
    # job_welfare.send_keys('bonus 2 times a year.')

    # job_other_info = driver.find_element_by_id('description-editorOTHER_ifr')
    # job_other_info.send_keys('you can do remote work as well.')

    time.sleep(5)

    btn_continue = driver.find_element_by_xpath('//*[@id="sheet-next-button"]/span/a')
    btn_continue.click()

    time.sleep(5)

    ### page 3 data entry
    # email entry input field
    # 手動で渡している（email addtaess and phone number）
    apply_email = driver.find_element_by_xpath('//*[@id="emails-container"]/div/div/input')
    apply_email.clear()
    apply_email.send_keys('shimakenichi1009@gmail.com')
    # apply_email.submit()

    time.sleep(5)

    # phone number entry input field
    apply_phone = driver.find_element_by_id('input-cmiPhone')
    apply_phone.clear()
    apply_phone.send_keys('0120204210')

    time.sleep(5)

    # continue button
    btn_continue_2 = driver.find_element_by_xpath('//*[@id="sheet-next-button"]/span/a')
    btn_continue_2.click()

    time.sleep(5)

    # final confirm button
    btn_confirm = driver.find_element_by_xpath('//*[@id="confirm-button-in-preview"]')
    btn_confirm.click()

    time.sleep(5)

    # post_without_payment = driver.find_element_by_xpath('//*[@id="uniqueId1"]')
    # post_without_payment.click()

    # time.sleep(5)



### main 処理
def main():
    login()

    
if __name__ == "__main__":
    main()

