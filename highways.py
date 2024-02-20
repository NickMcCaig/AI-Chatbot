import requests
def getHighwayProblemByID(problem_id):
    url = f"https://secure.nottinghamshire.gov.uk/highwaysenquiriesintegrations/api/highwayProblems/{problem_id}?apiKey="
    response = requests.get(url)
    try:
        data = response.json()
        updates = data["updates"]
        return  updates[len(updates) -1 ]["statusDescription"]
    except:
        return "We dont appear to have any infomation about this report"
