# imported the requests library
import requests
image_url = "https://raw.githubusercontent.com/riri-314/Quinzaine/main/.github/images/out-doom.png"

# URL of the image to be downloaded is defined as image_url
r = requests.get(image_url) # create HTTP response object
print((str(r)))

# send a HTTP request to the server and save
# the HTTP response in a response object called r
with open("python_logo.png",'wb') as f:
    # Saving received content as a png file in
    # binary format
    # write the contents of the response (r.content)
    # to a new file in binary mode.
    f.write(r.content)