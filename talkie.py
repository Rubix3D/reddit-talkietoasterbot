import praw
import time
import os
import string

def authenticate():
    print("Authenticating...")
    r = praw.Reddit('TTBot', user_agent = "TalkieToasterBot By Rubix")
    print("Authenticated as {}".format(r.user.me()))
    return r

def main():
    r = authenticate()
    comments_replied_to = get_saved_comments()
    while True:
        run_bot(r, comments_replied_to)
        time.sleep(120)

def get_saved_comments():
    if not os.path.isfile("comments.txt"):
        comments_replied_to = []
    else:
        with open("comments.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
        return comments_replied_to

def run_bot(r, comments_replied_to):

    words_to_look_for = [ {
        'id': 'toast',
        'target_text':  ['toast', 'muffin', 'teacakes', 'teacake', 'buns', 'bun', 'baguettes', 'baguette', 'bagels', 'bagel', 'crumpets', 'crumpet', 'pancakes', 'pancake', 'hot cross buns', 'flapjacks', 'flapjack', 'waffle', 'waffles', 'toaster'],
        'reply':  'Would anyone like some toast?'
    },
    {
        'id': 'talkie',
        'target_text': ['Talkie', 'talkie'],
        'reply': "Howdy Doodly doo! Talkie's the name toastings the game."
    },
    {
        'id': 'flapjack',
        'target_text': ['No Flapjacks', 'no flapjacks'],
        'reply': "So you're a waffle man eh?"
    },
    {
        'id': 'bread',
        'target_text': ['No Bread', 'no bread'],
        'reply': "But I'm a toaster! It is my raison d'etre.. I toast, therefore I am. If you didn't want toast why did you repair me?"
    },
    {
        'id': 'accident',
        'target_text': ['accident'],
        'reply': "That wasn't an accident! It was first degree toastercide."
    },
    {
        'id': 'fish',
        'target_text': ['fish'],
        'reply': "Today's fish is trout a la creme. Enjoy your meal."
    }]

    print("Grabbing Subreddit...")

    for comment in r.subreddit('RedDwarf').comments(limit=25):

        comment_text = comment.body.lower()

        for item in words_to_look_for:

            isMatch = False
            isMatch = any(string in comment_text for string in item['target_text'])

            if comment.id not in comments_replied_to and not comment.author == r.user.me() and isMatch:

                comment.reply(item['reply'] + "\n\n^^^I ^^^am ^^^a ^bot. ^^^If ^^^there ^^^are ^^^any ^^^problems ^^^please ^^^pm ^^^/u/rubixmaster5567")
                print('Replying to ' + comment.id)
                comments_replied_to.append(comment.id)

                with open("comments.txt", "a") as f:
                    f.write(comment.id + "\n")

                print("Successful Reply!")
    else:
        print("No Comments Found, Sleeping for 120 Seconds")


if __name__ == '__main__':
    while True:
        try:
            main()
        except BaseException:
            time.sleep(5)
