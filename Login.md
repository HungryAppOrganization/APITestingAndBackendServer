# Login

Used to login/collect a Token for a registered User. If this is the first login, it sets up ana ccount.

**URL** : `/api/login_method/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
  "username": "[valid username]",
  "fId": "[facebook id]",
  "fToken": "[facebook auth token]",
  "eId":"[email id]",
  "pId":"[password in plain text]"
}
```

**Data example**

```json
{
  "username": "jpeurifo",
  "fId": "john_peurifoy56",
  "fToken": "ASDKSDFKWEOEWPO",
  "eId":"",
  "pId":""
}

{
  "username": "jpeurifo",
  "fId": "",
  "fToken": "",
  "eId":"test@abc.com",
  "pId":"abc1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "result": "true"
}
```

## Error Response

**Condition** : If 'username' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "non_field_errors": [
        "Unable to login with provided credentials."
    ]
}
```