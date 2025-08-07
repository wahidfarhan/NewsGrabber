import requests

PAGE_ACCESS_TOKEN = 'EAAabmyMcwzYBPEg6NdUQaBENleZBf5ATfDaMAXgRVk66L1CryYNCNMFtdvbDZCKjelQHYEzyKnMDZBOJsprOCHhjLpale0oTG8n6RwY0KPjfjMf2CSFTnQ5tNqpu1oqTUbcYpsEulzPP9FKhjaXuzXKSkMZCmJhPBQ5sngmQhyc2m2OCPDdXbNcvjHoIZBDtZCYVRUdkCcpbqfLNCr1QuwKVr6ccT0uDs9cLyf2O0D'
PAGE_ID = '599649106574283'
message = '📢 Hello from Python! Successful post to the Gonitron page! ✅'

# Recommended: Specify version
url = f'https://graph.facebook.com/v19.0/{PAGE_ID}/feed'

payload = {
    'message': message,
    'access_token': PAGE_ACCESS_TOKEN
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    print('✅ Post successful!')
    print('🔗 Post ID:', response.json().get('id'))
else:
    print('❌ Failed to post')
    print('Status Code:', response.status_code)
    print('Response:', response.text)
