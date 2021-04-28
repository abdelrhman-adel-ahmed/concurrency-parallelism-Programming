import concurrent.futures
import time

import requests

img_urls = ["https://images.unsplash.com/photo-1517783887476-66ca3d04b132"]


t1 = time.perf_counter()


def download_image(img_url):
    binary_img = requests.get(img_url).content
    img_name = img_url.split("/")[3]
    img_name = f"{img_name}.jpg"
    with open(img_name, "wb") as img:
        img.write(binary_img)
        print(f"{img_name} has been downloaded ..")
    return "done"


# use threading ,now each image will get downloaded in diffrent thread
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(download_image, img_urls)
    for result in results:
        print(result)

t2 = time.perf_counter()

print(f"it takes {t2-t1} sec")
