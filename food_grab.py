import json
from time import sleep

# ✅ for selenium version 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Opening the website on Chrome
# driver = webdriver.Chrome()
driver.get("https://food.grab.com/sg/en/restaurants")

driver.maximize_window()

# Function for append data to json file
def write_json(new_data, filename="restaurants.json"):
    with open(filename, "wr+") as file:
        file_data = json.load(file)
        file_data["restaurants"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


for i in range(15):
    # get the data from website
    data = driver.find_element("id", "__NEXT_DATA__").get_attribute("innerHTML")
    parsedData = json.loads(data)

    restaurantLists = parsedData["props"]["initialReduxState"]["pageRestaurantsV2"][
        "entities"
    ]["restaurantList"]

    # append restaurant to json file
    for key in restaurantLists:
        restaurant = {}
        restaurant["title"] = restaurantLists[key]["name"]
        restaurant["latitude"] = restaurantLists[key]["latitude"]
        restaurant["longitude"] = restaurantLists[key]["longitude"]
        write_json(restaurant)

    # catch the load more button and clicking it
    load_more = driver.find_element(
        "xpath", '//*[@id="page-content"]/div[4]/div/div/div[4]/div/button'
    )
    load_more.click()
    sleep(15)


driver.quit()

#simple selenium script, json simple code edit proxy add
