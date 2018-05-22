# Swipe Card

This records a user swipe.

**URL** : `/api/swipe_card/`

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
    "success": True
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