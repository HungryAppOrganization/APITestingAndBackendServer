# Phone Call

This is used to place an automated phone call. After calling this (and succesfully delivering it), a text will be sent to the user with the details of their order. 

**URL** : `/api/place_phoneCall/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
  "username":"[valid username]",
  "ordid":"[valid order id. 15 characters, must start with ord]",
  "cname": "[customer name]",
  "cnum": "[customer phone number for text/response]",
  "ord": "[name of order item]",
  "ord_add": "[any additions or speciality items]",
  "rname":"[restaurant name]",
  "rnum":"[restaurant phone number]",
  "pinfo":"[special processing information, unused for most]"
}
```

**Data example**

```json
{
  "username":"jpeurifo",
  "ordid":"ord4htavf10zk11",
  "cname": "George",
  "cnum": "%2B18034791475",
  "ord": "curry%20chicken",
  "ord_add": "no%20cheese",
  "rname":"hello%20hungry",
  "rnum":"%2B18034791475",
  "pinfo":"1928"

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