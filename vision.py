from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import requests, uuid, json, string

subscription_key = ""
endpoint = "https://aibotservices.cognitiveservices.azure.com/"
translateendpoint = "https://api.cognitive.microsofttranslator.com"
translateKey = ""
location = "uksouth"
#https://learn.microsoft.com/en-us/samples/azure-samples/cognitive-services-rest-api-samples/cognitive-services-rest-api-samples/
def findText(image_URL):
    
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    # Get an image with text

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(image_URL,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(0.3)

    # Print the detected text, line by line
    lines = ""
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                #print(line.text)
                lines += line.text
    #print()

    # Replace with your Azure Translator Text subscription key
    # Specify the language to translate the text to

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.

    #print(translate("https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"))
    return lines
def translate(lines, frm, lnto):
    path = '/translate'
    constructed_url = translateendpoint + path

    params = {
        'api-version': '3.0',
        'from': frm,
        'to': [lnto]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': translateKey,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': lines
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']
def detectLanguage(text):
    path = '/detect'
    constructed_url = translateendpoint + path
    params = {
        'api-version': '3.0'
    }
    headers = {
        'Ocp-Apim-Subscription-Key': translateKey,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'Text': text
    }]
    request = requests.post(constructed_url,params=params, headers=headers, json=body)
    return json.loads(request.text)[0]['language']
def getLanaguages():
    path = '/languages'
    params = {
        'api-version': '3.0'
    }
    constructed_url = translateendpoint + path
    request = requests.get(url=constructed_url, params=params)
    return json.loads(request.text)
def get_language_code(name):
    path = '/languages'
    params = {
        'api-version': '3.0'
    }
    constructed_url = translateendpoint + path
    request = requests.get(url=constructed_url, params=params)
    data = request.json()
    # Loop through the list of languages and check for a match
    for code, info in data['translation'].items():
        if info['name'].lower() == name.lower():
            return code

    # If no match was found, return None
    return None
#lines = findText("https://docs.unity3d.com/Packages/com.unity.textmeshpro@3.2/manual/images/TMP_RichTextLineIndent.png")
#fromlng = detectLanguage(lines)
#print(translate(lines,fromlng,'fr'))
 