import praw
import json
import argparse
import urllib
from datetime import date

IMAGE_FORMATS = ['.gif', '.jpg', '.png', '.bmp']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--download', help='Download images from submissions', choices=['none', 'all', 'sfw', 'nsfw'], default='none')
    args = parser.parse_args()

    data = {}
    with open('conf.json', 'r') as json_file:
        data = json.load(json_file)
        
    reddit = praw.Reddit(client_id=data['client_id'],
                        client_secret=data['client_secret'],
                        password=data['password'],
                        username=data['username'],
                        user_agent='Save grabber')

    saved = reddit.user.me().saved(limit=None)

    result = {'linksubmissions': [], 'textsubmissions': [], 'comments': []}

    for save in saved:
        if isinstance(save, praw.models.reddit.submission.Submission):
            if save.is_self:
                result['textsubmissions'].append(parse_text_submission(save))
            else:
                if args.download != 'none':
                    result['linksubmissions'].append(parse_link_submission_download_images(save, args.download))
                else:
                    result['linksubmissions'].append(parse_link_submission(save))
        elif isinstance(save, praw.models.reddit.comment.Comment):
            result['comments'].append(parse_comment(save))
        else:
            print(f'UNKNOWN_TYPE {type(save)}')

    result_json = json.dumps(result)

    d = date.today().strftime("%Y%m%d")

    with open(f'{d}-redditsaves-{data["username"]}.json', 'w') as results:
        results.write(result_json)

    print('Done!')

def parse_comment(comment):
    res = parse(comment)

    res['body'] = comment.body_html

    return res

def parse_text_submission(submission):
    res = parse_submission(submission)

    res['selftext'] = submission.selftext_html

    return res


def parse_link_submission_download_images(submission, mode):
    res = parse_link_submission(submission)

    if res['url'].endswith(tuple(IMAGE_FORMATS)):
        if (mode == 'sfw' and res['nsfw']) or (mode == 'nsfw' and not res['nsfw']):
            return res
        filename = f'{res["id"]}.{res["url"].split(".")[-1]}'
        print(f'Downloading {filename}...')
        urllib.request.urlretrieve(res['url'], filename)
        print(f'Downloaded {filename}')
        res['file'] = filename
    return res

def parse_link_submission(submission):
    res = parse_submission(submission)

    res['url'] = submission.url

    return res

def parse_submission(submission):
    res = parse(submission)

    res['title'] = submission.title
    res['subreddit'] = submission.subreddit_name_prefixed

    return res

def parse(save):
    res = {}

    res['id'] = save.id
    res['nsfw'] = bool(save.over_18)
    try:
        res['author'] = save.author.name
    except AttributeError:
        print(f'{save.id} has no author, replacing with [deleted]')
        res['author'] = '[deleted]'

    return res

if __name__ == "__main__":
    main()