import facebook
import requests
import json


def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(json.dumps(post))


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'EAABr42W9We8BADGqOR9UWTmyrlZAZCNVH8UiqKLe16RZBskZACKZCpUuus9NUczSfvo7c3Jt7HUdH2G3TWhfBxHCHI8WftIsVC45RxIt26aY9TLwZAfDecLHRvnKHsSZAzqbyGZBLTmk7y5qla3ZCKrXq1ABZBI4aOz4oZD'
# Look at Bill Gates's profile for this example by using his Facebook id.
user = 'luisgerardo.marcos'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts')

# Wrap this block in a while loop so we can keep paginating requests until
# finished.
while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        [some_action(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break