import facebook

def main():
  # Fill in the values noted in previous steps here
  cfg = {
    "page_id"      : "1771819073136795",  # Step 1
    "access_token" : "EAABr42W9We8BADGqOR9UWTmyrlZAZCNVH8UiqKLe16RZBskZACKZCpUuus9NUczSfvo7c3Jt7HUdH2G3TWhfBxHCHI8WftIsVC45RxIt26aY9TLwZAfDecLHRvnKHsSZAzqbyGZBLTmk7y5qla3ZCKrXq1ABZBI4aOz4oZD"   # Step 3
    }

  api = get_api(cfg)
  msg = "Hello, world!"
  status = api.feed

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip
  # the following if you want to post as yourself.
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

if __name__ == "__main__":
  main()