import pandas as pd
import easyocr
import cv2
import numpy as np


class RecSystem:

    def __init__(self):
        self.reader = easyocr.Reader(['ru'], gpu=True)

    def getResults(self, image):
        h, w, d = image.shape
        image = image[int((h / 2) - (w / 2)):int((h / 2) + (w / 2)), :]
        image = cv2.resize(image, (512, 512))
        images = []
        images.append(image)
        results = self.reader.readtext(images[0], batch_size=512, add_margin=0.05, blocklist="!@#$^&*()[]{}<>/?';:|~`+=abcdefghijklmnopqrstuvwxyz")
        return pd.DataFrame(results, columns=['bbox', 'text', 'conf'])

    def separateResults(self, data):
        naming = []
        cost = []
        numbers = []
        for index, row in data.iterrows():
            if row['conf'] >= 0.5:
                text = row['text'].lower()
                if " " in text:
                    texts = text.split(" ")
                    for word in texts:
                        if not("цена" in word or word == "за" or word == "шт."):
                            if word.count("р") == 1 and word.count("к") == 1:
                                count_dig = 0
                                for ch in word:
                                    if ch.isdigit():
                                        count_dig += 1
                                if count_dig >= 3:
                                    word = word.replace("о", "0")
                                    word = word.replace("o", "0")
                                    cost.append(word)
                            else:
                                count_dig = 0
                                for ch in word:
                                    if ch.isdigit():
                                        count_dig += 1
                                if count_dig >= 2:
                                    numbers.append(word)
                                else:
                                    naming.append(word)
                else:
                    word = text
                    if not ("цена" in word or word == "за" or word == "шт."):
                        if word.count("р") == 1 and word.count("к") == 1:
                            count_dig = 0
                            for ch in word:
                                if ch.isdigit():
                                    count_dig += 1
                            if count_dig >= 3:
                                word = word.replace("о", "0")
                                word = word.replace("o", "0")
                                cost.append(word)
                        else:
                            count_dig = 0
                            for ch in word:
                                if ch.isdigit():
                                    count_dig += 1
                            if count_dig >= 2:
                                numbers.append(word)
                            else:
                                naming.append(word)
        return naming, cost, numbers