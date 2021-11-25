from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import json


def get_din_details(url, key, id):
    driver = WebDriver()
    # webdriver.Chrome(executable_path="geckodriver.exe")
    driver.get(url)
    input_field = driver.find_element(By.ID, "DIN")
    input_field.send_keys(key)
    submit = driver.find_element(By.ID, id)
    submit.submit()
    table_id = driver.find_element(By.ID, "enquireDINDetailsId")
    # return table_id.text
    return text_to_json(table_id.text, key, [])


def get_srn_details(url, key, id_1, id_2, id_3):
    driver = WebDriver()
    # webdriver.Chrome(executable_path="geckodriver.exe")
    driver.get(url)
    input_field = driver.find_element(By.ID, "srn")
    input_field.send_keys(key)
    submit = driver.find_element(By.ID, id_1)
    submit.submit()
    table_id = driver.find_element(By.ID, id_2)
    # print(table_id.text)

    url_ids = []
    form_table = driver.find_element(By.ID, id_3)
    eform = form_table.find_elements(By.TAG_NAME, "tr")

    for i in eform:
        url_info = i.find_element(By.TAG_NAME, "input").get_attribute("onclick")
        url_ids.append(url_info)

    urls = get_srn_urls(url_ids)

    for i in eform:
        cell = i.find_element(By.TAG_NAME, "td")
        cell.click()
        time.sleep(5)

    return text_to_json(table_id.text, key, urls)
    # return table_id.text


def text_to_json(text, key, urls):
    items = list(text.split('\n'))
    json_dict = {}

    if items[0] == "DIN Details":

        items = items[1:]

        for item in items:

            if item.find("DIN " + key) != -1:
                key = "DIN"
                value = item.replace('DIN ', '')
                json_dict[key] = value

            elif item.find("Director Name") != -1:
                key = "Director Name"
                value = item.replace('Director Name ', '')
                json_dict[key] = value

            if item.find("DIN Status") != -1:
                key = "DIN Status"
                value = item.replace('DIN Status', '')
                json_dict[key] = value

            elif item.find("Date of Approval") != -1:
                key = "Date of Approval"
                value = item.replace("Date of Approval (if DIN status is active) ", "")
                json_dict[key] = value

            else:
                key = "Description"
                json_dict[key] = item

    else:

        key = "Payment Status"
        value = items[0].replace("Payment Status: ", "")
        json_dict[key] = value
        json_dict["doc_urls"] = urls

    json_obj = json.dumps(json_dict)

    return json_obj


def get_srn_urls(url_info):

    base_url = "https://www.mca.gov.in/mcafoportal/displayChallanReceipt.do?srn="
    end_url = "&pltrReceipt=false"

    urls = []
    base_length = len("displayChallanReceipt('")
    id_length = 9

    for info in url_info:
        info = info[base_length:base_length+id_length]
        urls.append(base_url + str(info) + end_url)

    return urls
