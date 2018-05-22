# APITestingAndBackendServer

These are API comments for the Hungry API Endpoint.

Most are done using [Flask](https://github.com/pallets/flask).

Where full URLs are provided in responses they will be rendered as if service
is running on 'http://testserver/'.

## Open Endpoints

Open endpoints require no Authentication.

* [Login](Login.md) : `POST /api/login_method/`
* [Get Next Card](get_next_card.md) : `POST /api/get_next_card/`
* [Swipe Card](swipe_card.md) : `POST /api/swipe_card/`
* [Swipe Card and get ID](swipe_card_id.md) : `POST /api/swipe_andgetID/`
* [Phone Call](phone_call.md) : `POST /api/place_phoneCall/`

## Endpoints that require Authentication

None currently. 
