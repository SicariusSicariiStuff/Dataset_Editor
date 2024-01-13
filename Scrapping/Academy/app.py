import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import unicodedata

# Function to remove nikud
def remove_nikud(word):
    return ''.join(char for char in unicodedata.normalize('NFD', word) if unicodedata.category(char) != 'Mn')

# Get the current working directory
current_directory = os.getcwd()

# Read shoresh values from "database.txt"
with open("database.txt", "r", encoding="utf-8") as file:
    shoresh_values = [line.strip() for line in file.readlines() if line.strip()]

# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode (without opening a browser window)
options.add_argument("--start-maximized")  # Maximize the window (since headless can't be minimized)
options.add_argument("--disable-infobars")  # Disable infobars
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--disable-dev-shm-usage")  # Disable dev-shm-usage for headless mode
options.add_argument("--no-sandbox")  # Disable sandbox for headless mode

# Create the "scrapped_pages" directory if it doesn't exist
scrapped_pages_dir = os.path.join(current_directory, "scrapped_pages")
os.makedirs(scrapped_pages_dir, exist_ok=True)

# Calculate the total number of iterations for tqdm
total_iterations = len(shoresh_values) * 7

# Initialize tqdm outside the loop
progress_bar = tqdm(total=total_iterations, desc="Processing", unit="page")

# Iterate through shoresh values
for shoresh in shoresh_values:
    # Iterate through specified binyan values
    for binyan in range(0, 61, 10):
        url = f"https://hebrew-academy.org.il/%d7%9c%d7%95%d7%97%d7%95%d7%aa-%d7%a0%d7%98%d7%99%d7%99%d7%aa-%d7%94%d7%a4%d7%95%d7%a2%d7%9c/?action=netiot&shoresh={shoresh}&binyan={binyan}"

        try:
            # Set up Selenium WebDriver
            driver = webdriver.Chrome(options=options)

            # Minimize the browser window
            driver.minimize_window()

            # Load the webpage
            driver.get(url)

            # Wait for a few seconds to allow dynamic content to load (you can adjust the wait time accordingly)
            time.sleep(1)

            # Click the button with id 'ktiv-male-button'
            button = driver.find_element(By.ID, 'ktiv-male-button')
            button.click()

            # Wait for a few seconds to allow the content to be updated (you can adjust the wait time accordingly)
            time.sleep(1)

            # Get the page source after dynamic content has loaded
            page_source = driver.page_source

            # Save the entire webpage in the "scrapped_pages" directory
            file_path = os.path.join(scrapped_pages_dir, f"page_saved_{remove_nikud(shoresh)}_{binyan}.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(page_source)

            # Update tqdm progress bar
            progress_bar.update(1)

        except Exception as e:
            # Log the error and continue to the next iteration
            tqdm.write(f"Error processing {url}: {str(e)}")
            progress_bar.update(1)

        finally:
            # Close the WebDriver, whether an exception occurred or not
            driver.quit()

# Close the tqdm progress bar
progress_bar.close()

# End of the script
print("All pages have been saved in the 'scrapped_pages' directory.")
