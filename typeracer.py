from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def print_start():
    print("Welcome to...")
    print(r"""

    ________               _____________________                          ____________________________ 
    ___  __ \_____ ___________(_)_____  /__  __/____  ______________      __|__  /_  __ \_  __ \_  __ \
    __  /_/ /  __ `/__  __ \_  /_  __  /__  /  __  / / /__  __ \  _ \     ___/_ <_  / / /  / / /  / / /
    _  _, _// /_/ /__  /_/ /  / / /_/ / _  /   _  /_/ /__  /_/ /  __/     ____/ // /_/ // /_/ // /_/ / 
    /_/ |_| \__,_/ _  .___//_/  \__,_/  /_/    _\__, / _  .___/\___/      /____/ \____/ \____/ \____/  
                /_/                         /____/  /_/                                             

    """)
    print(r"""
    Enter your desired typing speed and win! Please avoid clicking on the webpage while the script is typing.
    If your initial typing speed is 100 WPM or more, you will be flagged for cheating and asked to take a test. 
    You can simply not do the test, press the x, and try again via the command line.
    """)

def ask_speed():
    speed = float(input("Enter your desired speed (WPM): "))
    speed = 60 / (speed * 5.7)
    print("Gearing up...")
    return speed

def init_driver():
    driver = webdriver.Firefox()
    driver.get("https://play.typeracer.com/")
    time.sleep(1.5)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('i').key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
    time.sleep(1)
    return driver

def check_if_active_is_different(old_element):
    def condition(driver):
        return driver.switch_to.active_element != old_element
    return condition

def play(driver, speed):
   
    web_text = driver.execute_script("return Array.from(document.querySelectorAll('.inputPanel tr')).map(e => e.innerText);")
    type_text_list = web_text[0].split('\n', 1)
    type_text = type_text_list[0]

    og_active_element = driver.switch_to.active_element

    try:
        WebDriverWait(driver, 30).until(check_if_active_is_different(og_active_element))
    except TimeoutException:
        print("Timed out. Matchmaking canceled.")
        driver.close()

    print("Typing...")

    for char in type_text:
        driver.switch_to.active_element.send_keys(char)
        time.sleep(speed)

    # is_popup = driver.find_element(By.CLASS_NAME, "popupContent")
    # if is_popup != '':
    #     print(is_popup)


def next_race_shortcut(driver):
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('k').key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
    time.sleep(1)

def main():
    print_start()
    speed = ask_speed()
    driver = init_driver()
    while True:
        play(driver, speed)
        print("--------------------------------------------------------------------------------------")
        play_again = input("Would you like to play again? (y/n): ")
        if (play_again.lower() == 'n' or play_again.lower() == 'n'):
            break
        speed = ask_speed()
        next_race_shortcut(driver)
    driver.close()

if __name__ == "__main__":
    main()