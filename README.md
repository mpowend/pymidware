# pymidware

A very simple middleware for customizing the shape of request and response of an external api. because not every api is implemented the same way. But clients want them the same way!  
PR requests are very welcome. this project's ideal future is making sure non-coders can manage API's effectively.

## Usage

This project mainly consists of the `api.py` file and the `endpoints` directory.  
Endpoint addresses are decided by the filename of the endpoint file. for example the file `endpoints/example.json` will configure the `/api/example` endpoint.  
The `api.py` file will load all the endpoints and create the flask app.

### Endpoints

The endpoints are configured in json format. You can see the example endpoint in the `endpoints` directory. The `url` key is the url of the external api. Currently the only supported method is `POST`. The `headers` key contains the headers you want to add to the request.  
`params` and `body` shape the request body. you can have some constants i nthe request body, but you can fill the dynamic parts by describing them in the params key. for example if I want the user to give me the `username` and `password` in the request like this:

```json
{
	"id": "myusername",
	"passwd": "mypassword"
}
```

and then pass them to the real api like this:

```json
{
	"auth": {
		"username": "myusername",
		"password": "mypassword"
	}
}
```

I set body and params like this:

```json
{
	"body": {
		"auth": {
			"username": "defaultvalue",
			"password": "anotherdefaultvalue"
		}
	},
	"params": {
		"auth.username": "id",
		"auth.password": "passwd"
	}
}
```

This way you can customize apis without having to write a single line of code.

### Errors

If the external api returns an error, you can customize the error message by adding a `errors` key to the endpoint file. The `response` key is a dictionary of response codes and their corresponding behaviour. For example if the external api returns an error with code `100` and message `Invalid username or password`, we know the correvt http code for this error is 401:unauthorized. So you can add this to the endpoint file:

```json
{
	"response": {
		"100": {
			"Message": "Invalid username or password",
			"HTTP_Code": "401"
		},
		"default": { "Message": "Unknown error", "HTTP_Code": "500" },
		"200": { "Message": "Success", "HTTP_Code": "200", "success": true }
	}
}
```

any http code that is not defined uses the default key. any http code that has the `success` key set to `true` will be considered a success and the real response will be returned to the client.
