import os.path
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException


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


### login function.
def login(driver_data):
    driver = set_driver(driver_data,False)
    # Webサイトを開く
    driver.get("https://secure.indeed.com/account/login?service=draw&hl=ja&co=JP&continue=https%3A%2F%2Femployers.indeed.com%2Fp%3Ftoken%3D")
    return driver


### csv reader function.
def scrape_data():
    # calling login function.
    driver = login('chromedriver.exe')
    # get the title of the top page(login page).
    title = driver.title

    # read csv file of job detail
    csv_data = pd.read_csv('test_data1.csv', encoding="shift-jis")
    count = 0  # counter for rows in csv file(initial row 0).

    # csv data for receiving email and phone number to call from the job seeker.
    recruiter_detail = pd.read_csv('sample.csv')
    first_row = 0
    email = recruiter_detail.email_address
    phone = recruiter_detail.phone_number

    try:
        wait = WebDriverWait(driver, 600)
        wait.until_not(expected_conditions.title_is(title))

        # added from here(count the number of rows in csv file).
        get_row_column = csv_data.shape
        row_count = get_row_column[0]  # counter for rows.
        print(row_count)

        while count < row_count:
            # required data for first page.
            name = csv_data.職種名
            category =csv_data.職種カテゴリー
            company = csv_data.雇用企業名
            place = csv_data.勤務地

            # required data for second page
            job_style = csv_data.雇用形態
            salary_start = csv_data.給与最小
            salary_end = csv_data.給与最大
            salary_style = csv_data.給与体系
            description = csv_data.説明

            ### ----------page 1 data entry----------
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
            btn_next = driver.find_element_by_xpath('//*[@id="sheet-next-button"]/span/a')
            btn_next.click()
            time.sleep(5)

            ### ----------page 2 data entry----------
            # get job type(from radio buttons).
            if job_style[count] == '正社員':
                btn_select_job_type = driver.find_element_by_id('label-FULLTIME')
                btn_select_job_type.click()
            elif job_style[count] == 'アルバイト．パート':
                btn_select_job_type = driver.find_element_by_id('label-PARTTIME')
                btn_select_job_type.click()
            elif job_style[count] == '派遣社員':
                btn_select_job_type = driver.find_element_by_id('label-TEMPORARY')
                btn_select_job_type.click()
            elif job_style[count] == '契約社員':
                btn_select_job_type = driver.find_element_by_id('label-CONTRACT')
                btn_select_job_type.click()
            elif job_style[count] == 'インターン':
                btn_select_job_type = driver.find_element_by_id('label-INTERNSHIP')
                btn_select_job_type.click()
            elif job_style[count] == '業務委託':
                btn_select_job_type = driver.find_element_by_id('label-COMMISSION')
                btn_select_job_type.click()
            elif job_style[count] == 'ボランティア':
                btn_select_job_type = driver.find_element_by_id('label-VOLUNTEER')
                btn_select_job_type.click()
            elif job_style[count] == '新卒':
                btn_select_job_type = driver.find_element_by_id('label-NEW_GRAD')
                btn_select_job_type.click()
            elif job_style[count] == '請負':
                btn_select_job_type = driver.find_element_by_id('label-SUBCONTRACT')
                btn_select_job_type.click()
            elif job_style[count] == '嘱託社員':
                btn_select_job_type = driver.find_element_by_id('label-CUSTOM_1')
                btn_select_job_type.click()

            # salary range
            start_salary = driver.find_element_by_id('salary1')
            start_salary.clear()
            salary_num1 = int(salary_start[count])  # converting into int before submitting data
            start_salary.send_keys(salary_num1)

            end_salary = driver.find_element_by_id('salary2')
            end_salary.clear()
            salary_num2 = int(salary_end[count])  # converting into int before submitting data
            end_salary.send_keys(salary_num2)

            # salary base- monthly, yearly....
            salary_base = driver.find_element_by_id('salaryPeriod')
            for option in salary_base.find_elements_by_tag_name('option'):
                if option.text == salary_style[count]:
                    option.click()
                    print(salary_style[count])
                    break

            job_description = driver.find_element_by_id('description-editorJOB_DESCRIPTION_ifr')
            job_description.send_keys(description[count])
            time.sleep(5)

            # continue button
            btn_continue = driver.find_element_by_xpath('//*[@id="sheet-next-button"]/span/a')
            btn_continue.click()
            time.sleep(5)

            ### page 3 data entry
            # email entry input field
            recruiter_email = driver.find_element_by_xpath('//*[@id="emails-container"]/div/div/input')
            recruiter_email.clear()
            recruiter_email.send_keys(str(email[first_row]))
            time.sleep(5)
            # phone number entry input field
            recruiter_phone = driver.find_element_by_id('input-cmiPhone')
            recruiter_phone.clear()
            recruiter_phone.send_keys(str(phone[first_row]))
            time.sleep(5)

            # continue button
            btn_continue_2 = driver.find_element_by_xpath('//*[@id="sheet-next-button"]/span/a')
            btn_continue_2.click()
            time.sleep(5)

            # final confirm button
            btn_confirm = driver.find_element_by_xpath('//*[@id="confirm-button-in-preview"]')
            btn_confirm.click()
            time.sleep(10)

            # driver.findElement(By.linkText('有料オプションを利用せずに求人を掲載')).click()
            driver.find_element_by_link_text('有料オプションを利用せずに求人を掲載').click()
            time.sleep(5)

            back_to_upload_recruit = driver.find_element_by_xpath('//*[@id="postJobButton"]')
            back_to_upload_recruit.click()
            time.sleep(5)
            # increment for the row number in csv file.
            count += 1
        # print("completed posts: " + count)    
    
    except TimeoutException as e:
        print('You got timeout error.')
        driver.close()


### main 処理
def main():
    scrape_data()


if __name__ == "__main__":
    main()

