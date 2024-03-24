from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.common.exceptions import NoSuchElementException

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

def ask_speed_time():
    time = '0'
    while time not in ['15', '30', '60', '120']:
        time = input("Enter how long you would like to type for in seconds (15, 30, 60, 120): ")

    speed = float(input("Enter your desired speed (WPM): "))
    speed = 60 / speed
    return speed, time


def get_words(driver):

    try: 
        active_element = driver.find_element(By.CLASS_NAME, 'word.active')
    except NoSuchElementException:
        driver.close()

    result = driver.execute_script("""
        var activeElement = arguments[0];
        var nextElements = [];
        nextElements.push(activeElement.innerText);
        var sibling = activeElement.nextElementSibling;
        while (sibling) {
            nextElements.push(sibling.innerText);
            sibling = sibling.nextElementSibling;
        }
        return nextElements;
        """, active_element)

    return result

def play_monkey_type(speed, test_time):    
    newDriver = webdriver.Firefox()
    newDriver.get('https://monkeytype.com/')
    time.sleep(1.5)
    rejectAll = newDriver.find_element(By.CLASS_NAME, 'rejectAll')
    rejectAll.click();
    time_XPATH = "//div[@timeconfig = '" + test_time + "']"
    time_config = newDriver.find_element(By.XPATH, time_XPATH).click()

    time.sleep(1.5)

    actions = ActionChains(newDriver)

    while newDriver.find_element(By.ID, 'typingTest'):
        result = get_words(newDriver)
        for word in result:
            actions.send_keys(word).send_keys(Keys.SPACE).perform()
            time.sleep(speed)
    time.sleep(15)
    newDriver.close()


def main():
    print_start()
    speed_time = ask_speed_time()
    play_monkey_type(speed_time[0], speed_time[1])

if __name__ == "__main__":
    main()