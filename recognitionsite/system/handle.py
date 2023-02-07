def handle(f):
    with open('photo.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
