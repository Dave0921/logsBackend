Getting Started
===============
Make sure you have installed python3 on your machine and PATH.

Make sure you have the Flask and Flask-SQLAlchemy dependencies installed:

```bash
    pip install Flask
    pip install Flask-SQLAlchemy
```

Then, to run the project locally, go into the project directory and run:

```bash
    flask run
```

Documentation
===============

## Sending a log

```
POST /api/v1/log
```

* Sends and stores a user log to the backend. Note, the user must exist in the database for this request to be successful.

### Parameters:    

Headers:
    'Content-Type: application/json'

 
Example JSON data format:
```json
{
  "userId": "dDYLl2mT8",
  "sessionId": "999TGF123",
  "actions": [
    {
      "time": "2018-10-18T21:37:28-06:00",
      "type": "CLICK",
      "properties": {
        "locationX": 52,
        "locationY": 11
      }
    },
    {
      "time": "2018-10-18T21:37:30-06:00",
      "type": "VIEW",
      "properties": {
        "viewedId": "FDJKLHSLD"
      }
    },
    {
      "time": "2018-10-18T21:37:30-06:00",
      "type": "NAVIGATE",
      "properties": {
        "pageFrom": "communities",
        "pageTo": "inventory"
      }
    }
  ]
}
```

### Example Curl Command:
```bash
curl --location --request POST 'http://127.0.0.1:5000/api/v1/log' ^
--header 'Content-Type: application/json' ^
--data-raw '{
  "userId": "dDYLl",
  "sessionId": "999TGF123",
  "actions": [
    {
      "time": "2018-10-18T21:37:28-06:00",
      "type": "CLICK",
      "properties": {
        "locationX": 52,
        "locationY": 11
      }
    },
    {
      "time": "2018-10-18T21:37:30-06:00",
      "type": "VIEW",
      "properties": {
        "viewedId": "FDJKLHSLD"
      }
    },
    {
      "time": "2018-10-18T21:37:30-06:00",
      "type": "NAVIGATE",
      "properties": {
        "pageFrom": "communities",
        "pageTo": "inventory"
      }
    }
  ]
}'
```

### Responses:
#### Successful Response:
The log has been successfully sent to the backend.
```json
{
    "status": "success"
}
```

#### Error Response:
The following response may occur if the JSON data is not in the correct format as discussed above, or if the user does not exist.
```json
{
    "status": "failed"
}
```

## Retrieving Logs

```
GET /api/v1/retrieve?userId=user_id&type=log_type&start=start_time&end=end_time
```

* Retrieves logs from the backend. The logs may be filtered by any combination of user_id, log_type, start_time, or end_time.

### Parameters:
user_id: String 
* Filter the logs by user id

log_type: String
* Filters the logs by log type

start_time: date (iSO8601 format)
* Filters the logs after the start_time date (inclusive)

end_time: date (iSO8601 format)
* Filters the logs before the end_time date (inclusive)

### Responses:
#### Successful Response:
```json
{
    "logs": [
        {
            "actions": [
                {
                    "properties": {
                        "locationX": 52,
                        "locationY": 11
                    },
                    "time": "2018-10-18T21:37:28",
                    "type": "CLICK"
                },
                {
                    "properties": {
                        "locationX": 52,
                        "locationY": 11
                    },
                    "time": "2018-10-18T21:37:28",
                    "type": "CLICK"
                }
            ],
            "sessionId": "XYZ456ABC",
            "userId": "ABC123XYZ"
        },
        {
            "actions": [
                {
                    "properties": {
                        "locationX": 52,
                        "locationY": 11
                    },
                    "time": "2018-10-18T21:37:28",
                    "type": "CLICK"
                }
            ],
            "sessionId": "123FRE098",
            "userId": "dDYLl2mT8"
        }
    ],
    "status": "success"
}
```

#### Error Response:
The following response may occur if start_time and/or end_time are not correctly formated:
```json
{
    "status": "failed"
}
```

## Entering Test Users (Not for Production)

```
POST /testusers
```

* Note, logs can only be sent if the user_id corresponding to the logs exists in the database. This request enables you to add multiple user ids into the database for testing purposes (NOT TO BE USED FOR PRODUCTION).

### Parameters:

Headers:
    'Content-Type: application/json'
 
Example JSON data format:
```json
{
	"users": [
			{
				"userId": "YXGgm8DiT"
			},
			{
				"userId": "osdE0fb2a"
			},
			{
				"userId": "YCYaL3Mdq"
			}
		]
}
```

### Example Curl Command:
```bash
curl -L -X POST 'http://127.0.0.1:5000/api/v1/testusers' -H 'Content-Type: application/json' --data-raw '{"users": [{"userId": "YXGgm8DiT"},{"userId": "osdE0fb2a"},{"userId": "YCYaL3Mdq"}]}'
```

### Responses:
#### Successful Response:
The user ids have been successfully created. Note that if some or all the user ids already existed, the response will still be successful.
```json
{
    "status": "success"
}
```

#### Error Response:
The following response may occur if the JSON data is not in the correct format as discussed above.
```json
{
    "status": "failed"
}
```

Follow Up Question
===============

How do we make this solution cloud-scalable?
------

The current requirements ask for around 100 users sending logs every 5 minutes, which means a single MySQL database and single REST API for sending logs should be sufficient. However, if there were up to 10K users simultaneously sending logs at any moment and the querying of millions of data points, then we may need to change the ways we upload and retrieve logs.

In order to support many users sending log requests simultaneously, there are some options:

#### Supporting batch requests
* This allows for a faster response for multiple requests compared to making single requests multiple times.
#### Concurrent processing of batch requests
* Rather than synchronously processing every request, asynchronously enqueue the request into a queue of requests.
* Workers will dequeue requests from the queue and process them, storing the data into a database and then send responses back to the client.
#### Storing and Sharding the logs in a NoSQL database; for example Cassandra
* This allows the storage of millions or even billions of logs.
