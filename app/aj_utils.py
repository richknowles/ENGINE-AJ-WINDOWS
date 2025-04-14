import time
import random
from selenium.webdriver.common.action_chains import ActionChains

def human_delay(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def simulate_mouse_scroll(driver):
    from selenium.webdriver.common.action_chains import ActionChains
    import random

    actions = ActionChains(driver)
    try:
        # safer offset, avoids going out of bounds
        actions.move_by_offset(random.randint(-3, 3), random.randint(-3, 3)).perform()
    except:
        pass  # Prevent crash if move goes out of bounds
