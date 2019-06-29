import praw
import json
from datetime import date

def main():
    data = {}
    with open('conf.json', 'r') as json_file:
        data = json.load(json_file)
        
    reddit = praw.Reddit(client_id=data['client_id'],
                        client_secret=data['client_secret'],
                        password=data['password'],
                        username=data['username'],
                        user_agent='Save grabber')

    saved = reddit.user.me().saved(limit=None)
    
    result = ''
    for save in saved:
        if isinstance(save, praw.models.reddit.submission.Submission):
            result += f'SUBMISSION {save.id} - {save.title}'
            if save.is_self:
                result += f'SELFTEXT_HTML {save.selftext_html}'
            else:
                result += f'URL {save.url}'
        elif isinstance(save, praw.models.reddit.comment.Comment):
            result += f'COMMENT {save.id}\nBODY "{save.body}"\nBODY_HTML "{save.body_html}"'
        else:
            result += f'UNKNOWN_TYPE {type(save)}'
        result += '\n\n'

    d = date.today().strftime("%Y%m%d")

    with open(f'{d}-redditsaves-{data["username"]}.txt', 'w') as results:
        results.write(result)

if __name__ == "__main__":
    main()