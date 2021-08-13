import requests

#your reddit username/password
reddit_username = 'xxx'
reddit_password = 'xxx'

#we need a basic reddit app
#tutorial https://alpscode.com/blog/how-to-use-reddit-api/
#but the basics are below
#https://www.reddit.com/prefs/apps/ > "create an app" button at the bottom
# > make a "personal use script" > name it, "http://localhost" for redirect uri
# > then put the id and secret here
app_id = 'xxx'
app_secret = 'xxx'

#this bit gets your app an access token based on your reddit login and app data
base_url = 'https://www.reddit.com/'
data = {'grant_type': 'password', 'username': reddit_username, 'password': reddit_password}
auth = requests.auth.HTTPBasicAuth(app_id, app_secret)
r = requests.post(base_url + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': 'SimpleSavedScraper by /u/hoppingmad9'},
		  auth=auth)
d = r.json()

token = 'bearer ' + d['access_token']

#we can now send requests to the api
base_url = 'https://oauth.reddit.com'

#create new headers with the token
headers = {'Authorization': token, 'User-Agent': 'SimpleSavedScraper by /u/hoppingmad9'}
#check they work with a simple request to "me" api
response = requests.get(base_url + '/api/v1/me', headers=headers)

#if it worked it will print your username
if response.status_code == 200:
    print(response.json()['name'])

#set the number of posts to get per request (100 is fine)
posts = 100
#dicts to store the info in
post_subreddit_breakdown = {}
post_type_breakdown = {'t1': 0, 't3': 0}
#params to get the info
payload = {'limit': posts, 'after': ''}

while True:
    #the request
    response = requests.get(base_url + '/user/hoppingmad99/saved', headers=headers, params=payload)
    # status_code 200 is a success
    if response.status_code == 200:
        #set the new "after" post so that the api gets the next "set" of posts
        new_after = response.json()['data']['after']
        print(new_after)
        payload['after'] = new_after
        #check how many posts we got back and loop over them
        posts_retreived = response.json()['data']['dist']
        for x in range(posts_retreived):
            #post type, t1 is comment, t3 is link(and posts)
            post_type = response.json()['data']['children'][x]['kind']
            #subreddit the post/comment was in
            post_subreddit = response.json()['data']['children'][x]['data']['subreddit']
            #check if that sub is in our dict
            if post_subreddit in post_subreddit_breakdown:
                #if it is increment the subreddit count
                post_subreddit_breakdown[post_subreddit]['count'] += 1
            else:
                #if not then set up the subreddit count and the link/comment counts
                post_subreddit_breakdown[post_subreddit] = {}
                post_subreddit_breakdown[post_subreddit]['count'] = 1
                post_subreddit_breakdown[post_subreddit]['t1'] = 0
                post_subreddit_breakdown[post_subreddit]['t3'] = 0
            #now increment the type count for the subreddit
            post_subreddit_breakdown[post_subreddit][post_type] += 1
            #and the overall type count
            post_type_breakdown[post_type] += 1
        #if the next "after" post is None then we're finished
        if new_after == None:
            break;

#print the overall breakdown
print(post_type_breakdown)
#sort the subreddit breakdown by saves, most to least
sorted_breakdown = sorted(post_subreddit_breakdown.items(), key=lambda x:x[1]['count'], reverse=True)
#print the subreddits
for x in sorted_breakdown:
    print(x)
