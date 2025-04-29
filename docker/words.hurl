# Sanity check

# Authenticate with admin:admin credentials
POST http://localhost/api/auth
Content-Type: application/json

{
    "login": "admin",
    "password": "admin"
}

HTTP 200
[Captures]
token: jsonpath "$.token"

# POST /api/words to start a job
POST http://localhost/api/words
Authorization: Bearer {{token}}
[MultipartFormData]
text: file,words.txt;

HTTP 303
[Captures]
location: header "Location"

# Wait for the job to finish and check the result
GET http://localhost{{location}}
Authorization: Bearer {{token}}
[Options]
retry: 10
retry-interval: 500
HTTP 200
[Asserts]
jsonpath "$.count" == 3
