from rest_framework.views import Response, APIView
from system.forms import UploadFileForm
import cv2

from system.main import RecSystem


def handle(f):
    with open('B:\server\\recognitionsite\system\scripts\photo.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class ResultAPIView(APIView):

    system = RecSystem()

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        handle(request.FILES['image'])
        image = cv2.imread("B:\server\\recognitionsite\system\scripts\photo.jpg")
        naming, cost, numbers = self.returnResult(image)
        return Response({"naming": naming,
                         "cost": cost,
                         "numbers": numbers})

    def returnResult(self, image):
        data = self.system.getResults(image)
        naming, cost, numbers = self.system.separateResults(data)
        return naming, cost, numbers

