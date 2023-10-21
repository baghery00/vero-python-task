from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from .repository import *
import pandas as pd
import json

@api_view(['PUT'])
@parser_classes([MultiPartParser])
def ExampleView(request):
    csv = pd.read_csv(request.FILES['file'], sep=';')
    items = getActiveVehicles()
    js = pd.DataFrame(items).sort_values(by=["editedOn"], ascending=False).drop_duplicates('kurzname')
    concat = pd.concat([js,csv]).drop_duplicates('kurzname')
    concat['colorCode'] = concat['labelIds'].apply(lambda x: getColorCode(x))
    return JsonResponse(json.loads(concat.to_json(orient="records")), safe = False)