# Message send service

## Build container

```bash
docker compose build --no-cache
```

## Start container

```bash
docker compose up
```

## Send message

```curl
curl -X POST http://localhost:8000/api/users/1/send/ \
-H "Content-Type: application/json" \
-d '{"message": "Hello World!"}'
```

## Create user

```curl
curl -X POST http://localhost:8000/api/users/ \
-H "Content-Type: application/json" \
-d '{"email": "test@example.com", "phone": "+79001234567", "telegram_id": "1111111111"}'
```

## Get all users

```curl
curl http://localhost:8000/api/users/
```

## Get user

```curl
curl http://localhost:8000/api/users/1/
```

## Update user

### PATCH

```curl
curl -X PATCH http://localhost:8000/api/users/1/ \
-H "Content-Type: application/json" \
-d '{"telegram_id": "123456789"}'
```

### PUT

```curl
curl -X PUT http://localhost:8000/api/users/1/ \
-H "Content-Type: application/json" \
-d '{"email": "test_update@example.com", "phone": "+70000000000", "telegram_id": "000000000"}'
```

## Delete user

```curl
curl -X DELETE http://localhost:8000/api/users/1/
```