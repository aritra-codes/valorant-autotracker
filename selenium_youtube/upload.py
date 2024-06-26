import threading
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import selenium_youtube.constants as c

def input_to_field(field: WebElement, text: str) -> None:
    field.clear()
    field.send_keys(text)

def upload_video(firefox_profile_path: str, path: str, title: str, description: str="", visibility: c.Visibility=c.Visibility.private, background: bool=False) -> str:
    options = Options()
    options.profile = FirefoxProfile(firefox_profile_path)

    if background:
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    try:
        # Goes to the YouTube upload url
        driver.get("https://youtube.com/upload/")

        # Inputs the video to upload
        video_upload = driver.find_element(*c.VIDEO_UPLOAD_LOCATOR)
        video_upload.send_keys(os.path.abspath(path))

        # Waits for the title field to load (and as a result the rest of the page)
        WebDriverWait(driver, c.TIMEOUT).until(EC.visibility_of_element_located(c.TITLE_FIELD_LOCATOR))

        # Inputs the title, description (and not-for-kids option)
        input_to_field(driver.find_element(*c.TITLE_FIELD_LOCATOR), title)
        input_to_field(driver.find_element(*c.DESCRIPTION_FIELD_LOCATOR), description)
        driver.find_element(*c.NOT_FOR_KIDS_RADIO_LOCATOR).click()

        # Presses the next button 3 times
        for _ in range(3):
            driver.find_element(*c.NEXT_BUTTON_LOCATOR).click()

        # Inputs the desired visibility option
        driver.find_element(*c.VISIBILITY_RADIO_LOCATOR(visibility)).click()

        # Copies the video link
        link_anchor = driver.find_element(*c.LINK_ANCHOR_LOCATOR)
        WebDriverWait(driver, c.TIMEOUT).until(lambda _: link_anchor.get_attribute("href") != "")
        link = link_anchor.get_attribute("href")

        # Finishing up is done in a thread, so video link can be outputted in advance
        def finish():
            try:
                # Waits for the video to be uploaded
                upload_progress = driver.find_element(*c.UPLOAD_PROGRESS_LOCATOR)
                while upload_progress.get_attribute("innerHTML").startswith("Uploading"):
                    time.sleep(c.UPLOAD_POLL_FREQUENCY)

                # Waits for the save button to be not disabled, then clicks it
                WebDriverWait(driver, c.TIMEOUT).until(EC.text_to_be_present_in_element_attribute(c.SAVE_BUTTON_LOCATOR, "aria-disabled", "false"))
                driver.find_element(*c.SAVE_BUTTON_LOCATOR).click()

                # Waits for the save button to disappear (and as a result the rest of the page), so all changes are saved
                WebDriverWait(driver, c.TIMEOUT).until(EC.invisibility_of_element_located(c.SAVE_BUTTON_LOCATOR))

                print(f"Finished uploading video '{title}'.")
            except Exception:
                print(f"An error has occured, your upload for the video '{title}' may have been affected.")
            finally:
                driver.quit()
        thread = threading.Thread(target=finish).start()

        return link
    except Exception:
        driver.quit()

        raise
