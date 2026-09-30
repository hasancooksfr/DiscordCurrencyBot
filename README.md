# Currency Discord Bot
A simple discord bot handling mainly currency and banking commands.

It can be used by prefix commands, i.e. .help, .ping, .open, and slash commands, i.e. /help, /ping, /open. Default prefix set is `.` (dot)
## Commands
| Command | Description | Usage |
| ------- | -----------| ------|
| Help | Show help menu consisting of all commands | /help or .help |
| Ping | Pings the bot | /ping or .ping |
| Hello | Say hello to the bot | /hello or .hello |
| Bot Info | Get information about bot | /botinfo or .botinfo |
| Open | Used to open currency account | /help or .help |
| Balance | Used to check balance of currency account | /balance or .balance |
| Account Info | Returns information of a currency account | /info or .info |
| Transfer (Send) | Transfer Currency coins to an account of another user | /transfer or .transfer |
| Daily | Claim coins daily as daily rewards | /daily or .daily |
| Rob | Rob some coins from an user's account | /rob or .rob |
| Coinflip | A fun command to bet your coins and flip a coin, earn double if you guess right. (Can be used without betting coins) | /coinflip or .coinflip |
| Heist | Do a bank robbery (High risk, High reward) | /heist or .heist |
| Deactive | Deactive your account forever | /deactivate or .deactivate |

## Installation 
Clone the **repository**:
```
git clone https://github.com/hasancooksfr/DiscordCurrencyBot
cd DiscordCurrencyBot
```

Create a virtual environment:
```
python3 -m venv venv
```
Activate the virtual environment

Linux/MacOS:
```
source venv/bin/activate
```

Windows:
```
venv\Scripts\activate
```

Install dependencies:
```
pip install -r requirements.txt
```

## Configuration
Create a `.env ` file:
```env
BOT_TOKEN=YOUR_BOT_TOKEN
MONGO_URI=your_mongo_db_uri
```

Bot token can be obtained from [Discord Developers](https://discord.com/developers/applications/) and Mongo URI can be obtained from [MongoDB](https://www.mongodb.com/).

## Running the bot
```
python main.py
```

## Tech Stack
- Python 3.13+
- discord.py
- pymongo
- dotenv

## License
This project is licensed under the MIT License.

## Author
Hasandeep Singh
Built with Python and Discord.Py