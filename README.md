# Facebook friend network

Facebook friend network forked from [here](https://github.com/JupiLogy/facebook-friend-network).
## Requirements:
- Chrome browser
- Selenium
- TQDM
- DotEnv
- Webdriver Manager
- Gephi, unless you have some other plan for drawing your graph

Install command: `pip install Selenium python-dotenv tqdm webdriver-manager`

## How to use:

### Getting data:
1. Check you have all the requirements installed.
2. Change the Facebook link in `.env` to your username:
```env
FRIENDS_LIST="https://www.facebook.com/yourUsername/friends"
```
3. Run facebook.py.
4. Log in to Facebook in the pop up window, then go back to the terminal and press enter.

### Constructing Graph Using Gephi
1. Once it has finished, open Gephi and click `new project`.
2. Go to `Data Laboratory`, then `edges`. Now, `import spreadsheet`. Select `facebook.csv`.
3. Go to `Overview`. Choose the layout and press play.
4. Just kinda play around with Gephi until you get something you like :) you can even colour nodes.

### Saving Graph
1. Go to `preview` to make sure you like how it looks.
2. `File > Export >` whatever filetype you want.
3. Finally you can go to an image editor to draw labels and stuff.

## More info:
Currently does not detect facebook friends who do not have usernames.
For example, `www.facebook.com/user_name` is detected, but `www.facebook.com/profile.php?id=123456789` is not.

Also ignores friends who have no mutual friends, and those whose accounts are deactivated.

Waits a few seconds before going to different profiles.
This makes it slow, but if we go too fast, Facebook will give a temporary ban.

I have tried to reduce the risk of getting a temporary ban, but I can't guarantee anything.
If you get banned, it is not my responsibility.