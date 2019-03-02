json = {'ContentType': 'application/json'}
image_jpeg = {'ContentType': 'image/jpeg'}
image_git = {'ContentType': 'image/gif'}
image_png = {'ContentType': 'image/png'}
image_bmp = {'ContentType': 'image/bmp'}


def mimeType(mimeType):
    if mimeType == 'json':
        return json
    if mimeType == 'jpeg':
        return image_jpeg
    if mimeType == 'png':
        return image_png
    if mimeType == 'bmp':
        return image_bmp
    return 'unknown'
