import base64
import sys
import PIL
import numpy as np
from io import BytesIO

class Images:
    def __init__(self):
        self.path = 'storage/cards/'
    
    def joinImages(self, names):
        images = [f"{self.path}{file}.png" for file in names]
        print(images)

        imgs = [PIL.Image.open(i) for i in images]

        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

        buffered = BytesIO()
        # save that beautiful picture
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save(buffered, format="PNG")

        img_str = base64.b64encode(buffered.getvalue())
        return img_str

image = Images()