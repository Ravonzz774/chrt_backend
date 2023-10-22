# chrt_backend

#Регистрация
-----------
Endpoint: `/api/register`
Method: `POST`
Пример запроса:
```javascript
fetch("/api/register", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    username: "example_user",
    password: "example_password",
  }),
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```


#Аутентификация
--------------
Endpoint: `/api/login`
Method: `POST`
Пример запроса:
```javascript
fetch("/api/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    username: "example_user",
    password: "example_password",
  }),
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```


#Выход
-----
Endpoint: `/api/logout`
Method: `POST`
Пример запроса:
```javascript
fetch("/api/logout", {
  method: "POST",
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```

#Профиль пользователя
--------------------
Endpoint: `/api/profile`
Method: `GET`
Пример запроса:
```javascript
fetch("/api/profile", {
  method: "GET",
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```


#Выбор групп
-----------
Endpoint: `/api/groups`
Method: `POST`
Пример запроса:
```javascript
fetch("/api/groups", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    groups: ["1260", "1261"],
  }),
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```


#Мои группы
----------
Endpoint: `/api/my_groups`
Method: `GET`
Пример запроса:
```javascript
fetch("/api/my_groups", {
  method: "GET",
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```


#Удаление групп
-------------
Endpoint: `/api/delete_groups`
Method: `POST`
Пример запроса:
```javascript
fetch("/api/delete_groups", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    groups: ["1261"],
  }),
})
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```
