# Song Rating CLI

This is the CLI client of the Song Rating environment for Cider2. It communicate with
your [Song Rating API](https://github.com/chikatetsu/song-rating-server) running on
your server to rate your songs. Simply listen to your music on your Cider2 application,
and say if the current song playing is better or worse than the previous song using
the `Page Up` and `Page Down` button on your keyboard. The response of the API will
be displayed on the console running the CLI.

## Installation
### 1. Install Python
If it's not already done, install Python on your server. I use Python 3.12.

### 2. Create the Python Environment
Create your Python environment and install the required packages
([see requirements.txt](https://github.com/chikatetsu/song-rating-server/blob/main/requirements.txt)) :
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Create the .env file
Create the `.env` file containing your parameters with this format ([see example](https://github.com/chikatetsu/song-rating-server/blob/main/.env-example)) :
```dotenv
AUTH_TOKEN=song_rating_token_here
API_URL=song_rating_api_url_here
CIDER_TOKEN=cider_token_here
CIDER_PORT=10767
```
Every variables are optional, but they are most of the time needed to communicate
properly with your Song Rating API or your Cider application. Here are the default
value for every variables :
```dotenv
AUTH_TOKEN="" // If no authentication token is needed to connect to your Song Rating API
API_URL="localhost:8000" // Value by default, if you run the API with the default port locally
CIDER_TOKEN="" // If no authentication token is needed to connect to your Cider application
CIDER_PORT="10767" // The default port used by Cider
```

### 4. Running the CLI
#### Windows
```bash
source .venv/bin/activate
python main.py
```

#### Linux
Since the `keyboard` module can only be used with root permissions, I suggest you to
create a bash script with those commands and running this script in sudo mode :
```bash
source .venv/bin/activate
"$(which python)" main.py
```

## Coming soon
- [ ] Set vote up and vote down button
- [ ] Handle no vote
