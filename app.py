from fastapi import FastAPI
import uvicorn
import easyocr
import os
from fastapi import FastAPI, UploadFile
from typing import List

app = FastAPI()
reader = easyocr.Reader(['vi', 'en'])
# keywords = ['bài đăng']
KEYWORDS = ['Dấu trang']
# keywords = ['Được quảng bá', 'Quảng cáo']


@app.post("/process_keywords")
def process_keywords(keywords: List[str]):
    global KEYWORDS
    KEYWORDS = keywords
    print(("New keywords", KEYWORDS))
    return {"message": "Keywords processed successfully"}


@app.post('/upload')
async def upload_iamge(image: UploadFile):
    global KEYWORDS
    found = False
    with open(f"images/{image.filename}", "wb") as f:
        contents = await image.read()
        f.write(contents)

    result = reader.readtext(f"images/{image.filename}")

    text_contents = [annotation[1] for annotation in result]

    # print(text_contents)

    # for text_content in text_contents:
    #     print(text_content)

    for string in text_contents:
        # Iterate over each item in list1
        for item in KEYWORDS:
            # Check if the item is present in the current string
            if item.lower() in string.lower():
                print(f"{item} found in {string}")
                found = True

    return {"filename": image.filename, "found": found}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
