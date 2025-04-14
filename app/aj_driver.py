import os
import tempfile
from undetected_chromedriver import Chrome, ChromeOptions

def get_driver():
    # Use a safe system-wide temp directory for user data
    temp_user_data_dir = os.path.join(tempfile.gettempdir(), "aj_chrome_profile")

    options = ChromeOptions()
    options.add_argument(f'--user-data-dir={temp_user_data_dir}')
    options.add_argument('--profile-directory=Default')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = Chrome(options=options)
    driver.get("https://web.whatsapp.com")

    return driver

