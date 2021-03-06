# Coursera Video Downloader v1.0

from selenium import webdriver
import requests
import sys


# Example course_url - https://www.coursera.org/learn/convolutional-neural-networks/home/week/1
if len(sys.argv) != 2:
    print('Usage: cvd.py <course_url>')
    exit(1)


browser = webdriver.Firefox()
browser.implicitly_wait(60)
browser.get(sys.argv[1])


# Login
username = browser.find_element_by_id("emailInput-input")
password = browser.find_element_by_id("passwordInput-input")
login    = browser.find_element_by_xpath("//button[contains(@class, 'Button_1fxeab1-o_O-primary_cv02ee-o_O-md_28awn8 w-100')]")
username.send_keys("...")            # your coursera username here
password.send_keys("...")            # your coursera password here
login.click()


# Prepare a list of all the video hyperlinks
video_urls = []
video_names = []

link_objs = browser.find_elements_by_class_name('rc-ItemLink.nostyle')

for link in link_objs:
    link_url  = link.get_attribute("href")
    link_name = link_url.split('/')[-1]
    link_type = link_url.split('/')[-3]

    if link_type == "lecture":
        video_urls.append(link_url)
        video_names.append(link_name)


# Download videos
resolution_selected = False

for i, (video_url, video_name) in enumerate(zip(video_urls, video_names)):
    browser.get(video_url)
    
    if not resolution_selected:
        x = input("Please select video resolution and then press Enter...")
        resolution_selected = True
        browser.get(video_url)

    download_url = browser.find_element_by_id('c-video_html5_api').get_attribute("src")

    response = requests.get(download_url, stream = True)
    handle = open(str(i + 1) + "-" + video_name + ".mp4", "wb")

    for chunk in response.iter_content(chunk_size = 1 * 1024 * 1024):
        if chunk:
            handle.write(chunk)

    handle.close()


browser.close()
