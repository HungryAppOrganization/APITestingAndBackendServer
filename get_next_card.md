# Get Next Card

This finds what the next card should be (it assumes the backend does a caching system to store it)

**URL** : `/api/get_next_card/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
  "username": "[valid username]",
}
```

**Data example**

```json
{
  "username": "jpeurifo"
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