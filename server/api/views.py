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
    #Request the resources located at https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active
    js = pd.DataFrame(items).sort_values(by=["editedOn"], ascending=False).drop_duplicates('kurzname')

    #Store both of them (the API Response + request body) in an appropriate data structure and make sure the result is distinct
    df = pd.concat([js,csv]).drop_duplicates('kurzname')

    #Filter out any resources that do not have a value set for hu field
    df = df[df['hu'].notna()]

    #For each labelId in the vehicle's JSON array labelIds resolve its colorCode using https://api.baubuddy.de/dev/index.php/v1/labels/{labelId}
    df['colorCode'] = df['labelIds'].apply(lambda x: getColorCode(x))

    #return data-structure in JSON format
    return JsonResponse(json.loads(df.to_json(orient="records")), safe = False)