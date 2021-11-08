from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
from tqdm import tqdm
from dotenv import load_dotenv
import os

new_fb_vars = ["_6s5d", "b1v8xokw"]
friend_xpath = "//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl m9osqain gpro0wi8 b1v8xokw']"

time_to_wait = 3  # Change this according to your pc and internet speed
# Some utilities:


def get_name_and_link(link):
    # Get username from mutual friends link
    # Also returns mutual friends link as sometimes the link is weird
    split = str.split(link, sep="/")
    if split[-2] == "www.facebook.com":
        # Corresponding to when user doesn't have a fb username.
        # We get their user ID instead, which is a number.
        name = str.split(split[-1], sep="=")[-2][:-3]
    elif split[-2] == "mutual_friends":
        # This means the link leads to a differently formatted mutual friends list.
        # We need to regenerate the friends list link from the user ID.
        name = str.split(split[-1], sep="=")[-1]
        link = "https://www.facebook.com/profile.php?id=" + name + "&sk=friends_mutual"
        return [name, link]  # We return the link directly
        # because we manually generated it, we know it's ok, no more to do with it.
    else:
        # This means the username is fine.
        name = split[-2]

    return [name, link]


load_dotenv()

# Part 1: Getting list of your friends

service = Service(ChromeDriverManager().install())
driver = Chrome(service=service)

driver.get("https://www.facebook.com")
input("Press enter here when you have logged in to Facebook.")
# You need to log into your account to view your mutual friends lists.

driver.get(os.getenv("FRIENDS_LIST"))

class_vars = new_fb_vars

# Load page fully...
old_no_friends = -1
while len(driver.find_elements_by_class_name(class_vars[1])) != old_no_friends:
    old_no_friends = len(driver.find_elements_by_class_name(class_vars[1]))
    # Using space key to scroll down page, to fully load
    driver.find_elements_by_class_name(class_vars[0])[0].send_keys("     ")
    time.sleep(time_to_wait)
# Page loaded!
friends = driver.find_elements_by_xpath(friend_xpath)


# Get list of mutual friend links, add it to friend_links dictionary
print("Getting the list of mutual friends...")
friend_links = {}
for friend in tqdm(friends):
    try:
        friend.click
    except:
        print("Error No Click")
    finally:
        link_to_mutuals = friend.get_attribute("href")
        name, link = get_name_and_link(link_to_mutuals)
        friend_links[name] = link

# Dumping list of names with links, saving progress in case we lose connection
with open("friend_links", "wb") as file:
    pickle.dump(friend_links, file)
print("'friend_links' saved")


# Part 2: Getting mutual friends lists
mutuals = {}

for friend in tqdm(friend_links.keys()):
    driver.get(friend_links[friend])

    # Scroll until friends all load
    old_no_friends = -1
    while len(driver.find_elements_by_class_name(class_vars[1])) != old_no_friends:
        old_no_friends = len(driver.find_elements_by_class_name(class_vars[1]))
        # Scroll using space key
        driver.find_elements_by_class_name(class_vars[0])[0].send_keys("     ")
        time.sleep(time_to_wait)

    # Grab friends
    raw_mutuals = driver.find_elements_by_xpath(friend_xpath)
    mutuals[friend] = [get_name_and_link(friend.get_attribute("href"))[
        0] for friend in raw_mutuals]

# Dumping names with list of mutual friends. We can disconnect from Facebook now.
with open("mutuals", "wb") as f:
    pickle.dump(mutuals, f)
print("'mutuals' saved")

# Part 3: Getting csv

# csv_out will be our csv string we write to file
csv_out = ""

for friend in tqdm(mutuals.keys()):
    # Append friend name, followed by their mutual friends names.
    # As long as their mutual friend is not called "www.facebook.com".
    mutuals[friend].insert(0, friend)
    csv_out += (
        " ".join(
            [
                human
                for human in mutuals[friend]
                if human != "www.facebook.com"
            ]
        )
        + "\n"
    )

# Finally, write out the csv!
with open("facebook.csv", "w") as f:
    f.write(csv_out)
print("Output saved in 'facebook.csv'")
