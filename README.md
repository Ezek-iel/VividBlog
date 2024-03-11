Vividblog  API is built using flask-restful and react with marshemello as data validation. The following endpoints are implemented. 

## Blogs

- `/api/v1/blogs (GET)`  for all blogs
- `/api/v1/blogs (POST)` adding a new blog
- `/api/v1/blogs/{blogId} (GET)` get a particular blog
- `/api/v1/blogs/{blogId} (PUT)` update a particular blog
- `/api/v1/blogs/{blogId) (DELETE)` delete a particular blog
- `/api/v1/blogs/{blogId}/comments (GET)` for all comments
- `/api/v1/blogs/{blogId}/comments (POST)` for adding a new comment
- `/api/v1/blogs/{blogId}/likes`
- `/api/v1/blogs/{blogId}/comments/{commentId} (DELETE)` for deleting a new comment
- `/api/v1/blogs/{blogId}/comments/{commentId} (GET)` for unique comment on unique blog post.
- No endpoint for updating a comment (__intentionally__)

###  `/api/v1/blogs (GET)`

##### Response
##### 200

```json
{
  "blogs": [
    {
      "id": "6acc563d-3b7e-45f2-bf9c-4b5b9e95c704",
      "title": "My First Blog Post",
      "body": "This is my first blog post. I'm so excited to share my thoughts and experiences with you all in markdown. My posts will be longer than this actually",
      "created_at": "2022-08-01T12:00:00.000Z",
      "updated_at": "2022-08-01T12:00:00.000Z",
      "created_by" : "api/v1/users/{userId}",
      "comments" : "api/v1/blogs/6acc563d-3b7e-45f2-bf9c-4b5b9e95c704/comments",
      "likes" : 23
    },
    {
      "id": "391b6b5f-d353-4e4f-bcfa-600afe5261a1",
      "title": "My Second Blog Post",
      "body": "This is my second blog post. I'm going to talk about my favorite things to do in the summer.",
      "created_at": "2022-08-02T12:00:00.000Z",
      "updated_at": "2022-08-02T12:00:00.000Z",
      "created_by": "api/v1/users/{userId}",
      "comments" : "api/v1/blogs/391b6b5f-d353-4e4f-bcfa-600afe5261a1/comments",
      "likes" : 45
    }
  ]
}  
```

##### 500

```json
500 : {
"message" : "Error on our end";
}
```

If the user implements search. (__Wants to search for a blog__)  -  `/api/v1/blogs?s=javascript`
Results will be paginated for long blog posts - `/api/v1/blogs?page=2`
For __paginated search blog posts__ - `/api/v1/blogs?s=javascript&page=4`

### `/api/v1/blogs (POST)`

<span style = "background-color:  darkblue; padding : 9px; border-radius : 15px"><b>Authentication Needed</b></span>

##### Request

```json
{
  "title": "My Post Title",
  "content": "This is the content of my post in markdown",
  "author_id": "/api/v1/users/{userId}"
}
```

**Authentication Flow:**

1. User provides credentials (e.g., username and password) during login.
2. Server validates credentials and issues a JSON Web Token (JWT) to the user.
3. JWT is included in the Authorization header of the request to create a post.
4. Server verifies the JWT and authenticates the user.
5. If authentication is successful, the post is created. 

#### Responses

##### 200

```json
"blog" : {
"url" : "/api/v1/blogs/{blogId}",
"written by" : "/api/v1/users/{userId}",
"created at" : "2022-08-02T12:00:00.000Z",
}
```

##### 500

```json
500 : {
"message" : "error on our end"
}
```

### `/api/v1/blogs/{blogID} (PUT)`

<span style = "background-color:  darkblue; padding : 9px; border-radius : 15px"><b>Authentication Needed</b></span>

#### Request

Similar to the  `/blogs (POST)`

```json
{
  "title": "My Post Title",
  "content": "This is the content of my post in markdown",
  "author_id": "/api/v1/users/{userId}"
}
```

#### Response

##### 200 

```json
"blog" : {
"url" : "/api/v1/users/{userId}",
"written by" : "/api/v1/users/{userId}",
"updated at" : "2022-08-02T12:00:00.000Z"
}
```

##### 404

```json
{
"404" : {"message" : "error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

### `/api/v1/blogs/{blogId}/get`

#### Response

##### 200

```json
{
	"blog" : 
	{
      "id": "391b6b5f-d353-4e4f-bcfa-600afe5261a1",
      "title": "My Second Blog Post",
      "body": "This is my second blog post. I'm going to talk about my favorite things to do in the summer.",
      "created_at": "2022-08-02T12:00:00.000Z",
      "updated_at": "2022-08-02T12:00:00.000Z",
      "created_by": "api/v1/users/{userId}",
      "comments" : "api/v1/blogs/391b6b5f-d353-4e4f-bcfa-600afe5261a1/comments",
      "likes" : 45
	}
 }
```

### `/api/v1/blogs/{blogId}/comments/{commentId} (DELETE)`

#### Response

##### 200

```json
{
"200" : {"message" : "operation succesful"}
}
```

##### 404

```json
{
"404" : "error not found"
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

##### 404

```json
{
"404" : "error not found"
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

### `/api/v1/blogs/{blogId} (DELETE)`

<span style = "background-color:  darkblue; padding : 9px; border-radius : 15px"><b>Authentication Needed</b></span>

#### Response 

##### 200

```json
{
"200" : {"message" : "operation succesful"}
}
```

##### 404

```json
{
"404" : {"message" : "error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

### `/api/v1/blogs/{blogId}/comments (GET)`

#### Response

##### 200

```json
{"blog" : "/api/v1/blog/{blogid}",
"comments" : [
		{
	"message" : "A brand new comment",
	"author" : "/api/v1/users/{userID}",
	"blog" : "/api/v1/blogs/{blogId}",
	"created_at" : "2022-08-02T12:00:00.000Z"		
		},
		{
	"message" : "Another brand new comment",
	"author" : "/api/v1/users/{userID}",
	"blog" : "/api/v1/blogs/{blogId}",
	"created_at" : "2022-08-02T12:00:00.000Z"		
		}
	]
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

### `/api/v1/blogs/{blogId}/comments (POST)`

<span style = "background-color:  darkblue; padding : 9px; border-radius : 15px"><b>Authentication Needed</b></span>
#### Request

```json
{
"comment" :
	{
	"blog" : "/api/v1/blogs/{blogid}",
	"message" : "A very helpful message",
	"author" : "/api/v1/user/{userid}",
	}
}
```

#### Response

##### 200

```json
{
"200" : {"message" : "operation succesful"}
}
```

##### 500

```json
{
"404" : {"message" : "error on our end"}
}
```

### `/api/v1/blog/{blogId}/like(POST)`

<span style = "background-color:  darkblue; padding : 9px; border-radius : 15px"><b>Authentication Needed</b></span>

#### Request

```json
{
"blog" : "{blogid}",
"author" : "{userId}"
}
```

#### Response

##### 200

```json
{
"200" : {"message" : "operation succesful"}
}
```

##### 404

```json
{
"404" : {"message":"error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

## Users

`/api/v1/users/{userId} GET`  Get user details
`/api/v1/users POST` Create a user
`/api/v1/users/{userId} PUT` Update user details
`/api/v1/users/{userId}/followers GET` Get a list of the user's followers
`/api/v1/users GET` Get all users
`/api/v1/users/{userId}/follow POST` Follow a user
`/api/v1/users/{userId}/blogs/ GET` Get all blogs that a user wrote

### `/api/v1/users/{userId} GET`

#### Response


#### 200

```json
{
"user" : {
	"id" : "{userID}",
	"username" : "John Doe",
	"email" : "johndoe@email.com"
	"avatar_url" : "https://www.gravatar.com/url",
	"joined": "{some date}"
	"last_online": "{some time}"
	"blogs" : "/api/v1/users/{userID}/blogs"
	}
}
```

##### 404

```json
{
"404" : {"message" : "error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```


### `/api/v1/users POST`

#### Request

```json
{
"username" : "Kong Kung"
"email" : "kongking@gmail.com"
"password" : "password"
}
```

#### Response

##### 200

```json
{
"200" : {"message" : "operation succesful"}
}
```
##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

### `/api/v1/users/{userId} (PUT)`

#### Request

```json
{
"username" : "Kong Kung"
"email" : "kongking@gmail.com"
"password" : "password"
}
```

##### 200

```json
{
"200" : {"message" : "operation succesful"}
}
```

##### 404

```json
{
"404" : {"message":"error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

### `/api/v1/users/{userId}/followers (GET)`

#### Response

##### 200

```json
{
    "user": "/api/v1/user/{userid}}",
    "followers": [
        {
            "userid": "{someid}",
            "username": "John Roe",
            "full_details": "/api/v1/user/{userid}"
        },

        {
            "userid": "{someid}",
            "username": "John Toe",
            "full_details": "/api/v1/user/{userid}"
        }
    ]
}
```

##### 404

```json
{
"404" : {"message":"error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```

### `/api/v1/users GET`

#### Response

##### 200

```json
{

     "users":
     [
      {
        "user": {
                "id": "{userID}",
                "username": "John Doe",
                "email": "johndoe@email.com",
                "avatar_url": "https://www.gravatar.com/url",
                "joined": "{some date}",
                "last_online": "{some time}",
                "blogs": "/api/v1/users/{userID}/blogs"
            }
    },
  
    {
        "user": {
                "id": "{userID}",
                "username": "John Doe",
                "email": "johndoe@email.com",
                "avatar_url": "https://www.gravatar.com/url",
                "joined": "{some date}",
                "last_online": "{some time}",
                "blogs": "/api/v1/users/{userID}/blogs"
            }
    }
    ]
}
```

##### 404

```json
{
"404" : {"message":"error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```


### `/api/v1/users/{userId}/follow (POST)`

<span style = "background-color:  darkblue; padding : 9px; border-radius : 15px"><b>Authentication Needed</b></span>

##### 200

```json
{
"200" : {"message" : "operation succesful"}
}
```

##### 404

```json
{
"404" : {"message":"error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```


### `/api/v1/users/{userId}/blogs/ GET`

##### 200

```json
{
     "users":
     [
      {
        "blog": {
                "title" : "A Blog",
                "likes" : 23,
                "comments" : 45,
                "blogID" : "/api/v1/blogs/{blogId}"
            }
    },

    {
        "blog": {
            "title" : "A Blog",
            "likes" : 23,
            "comments" : 45,
            "blogID" : "/api/v1/blogs/{blogId}"
        }
    }
    
    ]
}
```

##### 404

```json
{
"404" : {"message":"error not found"}
}
```

##### 500

```json
{
"500" : {"message" : "error on our end"}
}
```
