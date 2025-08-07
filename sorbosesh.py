import requests

def post_to_facebook_page(message, image_url, page_access_token, page_id):
    # First, upload photo
    photo_url = f"https://graph.facebook.com/{page_id}/photos"
    payload = {
        "url": image_url,
        "caption": message,
        "access_token": page_access_token
    }

    response = requests.post(photo_url, data=payload)
    print(response.json())

# Replace with your values
page_access_token = "EAAKIfps6LWoBPH6C9b4amwZC8I7Cmsn2nnEqmrl1MAG5QWb1llY4ITs8GlSYZAxZA8aZAAGMtxARsclSKqSbMmzZAjjVwcBTMvmpwnIuM6Gtm3IwZAVClhi889TyeGur6hLojewT1Db0QuPrRxU8D67zcU5i5CMz16gt1sMMsdi4dBkZCmM4gS5Y6K504Ci6u8AZCSdJyhlCa9NmcMyZCn70j8xvl84aJ123kHFnhQ1cf6QZDZD"
page_id = "YOUR_PAGE_ID"
message = "আজকের প্রধান শিরোনাম!"
image_url = "https://cdn.jugantor.com/assets/news_photos/2025/07/27/Untitled-1-68862104e08dc.jpg"

post_to_facebook_page(message, image_url, page_access_token, page_id)
