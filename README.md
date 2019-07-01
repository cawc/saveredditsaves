# saveredditsaves
## Description
Saves a backup of your saved reddit posts to a file. The file will be JSON-formatted and contains your saved text submissions, link submissions and comments.

Data kept:
- id
- author
- content (link, HTML-formatted text, ...)

## Usage
Add a config file `conf.json` before running. Format:
```json
{
    "client_id": "CLIENT ID",
    "client_secret": "CLIENT SECRET",
    "password": "PASSWORD",
    "username": "USERNAME"
}
```
To find this information, see https://www.reddit.com/prefs/apps/ (you have to be logged in to see this page)