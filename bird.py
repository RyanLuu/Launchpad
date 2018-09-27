import requests
import uuid
import json
import pprint

#generate guid
def guid():
	return str(uuid.uuid4()) 

#get bird auth token
def get_bird_auth(email,guid):
	#generate GUID
	data = json.dumps({'email':email})
	headers = {
		'content-type' : 'application/json',
		'Platform' : 'ios',
		'Device-id' : guid
	}

	r = requests.post('https://api.bird.co/user/login', data=data, headers=headers)
	jsonified = json.loads(r.content)


	return jsonified


#40.4237° N, 86.9212° W Purdue coordinate
temp_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBVVRIIiwidXNlcl9pZCI6ImMwZjRjZGY4LWJjZmYtNGVjYy04OTAzLWEyMzFhNjkwMmRhMCIsImRldmljZV9pZCI6IjdjYTFmYTlkLTkzMjktNGRhMS05YWJhLTc5YzVmYmM4NTE1ZSIsImV4cCI6MTU2OTYxODUwNH0.xd3RVh-kHC4xTjnL2SUdQpUq_AqjJGkbCUEE7Rpv0HE'
def get_birds(token, guid):
	location = json.dumps({
			"latitude": 40.4237,
			"longitude": -86.9212,
			"altitude": 500,
			"accuracy": 100,
			"speed": -1,
			"heading": -1
		})
	headers = {
		'Authorization': 'Bird ' +  temp_token,
		'Device-id': guid,
		'App-Version': '4.3.3',
		'Location': location
	}

	r = requests.get('https://api.bird.co/bird/nearby?latitude=40.4237&longitude=86.9212&radius=1000', headers=headers)
	return r

guid = guid()
#token = get_bird_auth('josepzcxvcdsfa310@gmail.com', guid)
birds = get_birds(temp_token, guid)

print(birds)

print(birds.content)