# Swipe Card and Get ID

This method swipes and gets the ID in a single call. 

**URL** : `/api/swipe_andGetID/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
  "username": "[valid username]",
  "cardId":"[cardId]",
  "swipeChoice":"[swipeChoice, either -1, 2, 1]"
}
```

**Data example**

```json
{
  "username": "jpeurifo",
  "cardId": 40
  "swipeChoice":1
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "card": {
          "id" : 1202
          ...see firebase documentation
    }
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