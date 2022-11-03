# Obligatory assignment II, software security
## 1. Features
You'll note that this project misses quite a bit of polish, especially in the front end. I haven't had too much time to
work on this, so I decided to focus on the security part, and not the presentation.

### 1.1 Creating an account
A register page (basically the same as the login page) has been added where a user can register themselves if they 
haven't got an account.

### 1.2 Logging in/out
The main messaging part is only accessible for users that logged in. A user can log in with username and password, and 
they will stay logged in using a session token in their cookies.

### 1.3 Send messages
When logged in a User can start sending messages, and receive any messages send to them. To send a message the user has 
to type a valid username in the recipient field (this can also be themselves) and a message to send. When retrieving 
messages the user can only view messages sent to or by them.

### 1.4 API endpoints
If a user wishes they can use the API instead of the web-application. The API has 3 endpoints:
1. ```/new``` Accepts POST requests to create a new message. Args: recipient & message
2. ```/messages``` Accepts GET requests, retrieves a JSON object containing all messages belonging to the user
3. ```/messages/ID``` Accepts GET requests, retrieves message with id = ID. If the message does not exist or does not 
belong to the user it returns an empty object.

For all these requests authentication is required. Only basic auth headers are accepted containing username and password.
There is no API-token implementation.

## 2. Security
### 2.1 Sessions
Sessions are handled by flask, and all endpoints of the messaging service are protected by login checks. This protects 
against unauthenticated access to some degree. But since Flask manages sessions with session tokens, it is theoretically
possible for someone to guess the token of someone else and highjack their session.

### 2.2 Sql injections
All database queries where a user can input anything are made to be prepared statements, so no sql injection is possible.

### 2.3 Cross-site scripting
Cross site scripting is not possible in this implementation because of the fact that everything is html-safe escaped 
before being displayed: 
- messages get escaped before being stored in the database
- usernames when they are retrieved from the database (only in the web-application, not for the API).

### 2.4 Design
The app is split into 3 types of python files:
1. ```app.py``` Which starts and sets up the flask app.
2. Controllers, which contain all endpoints and handle requests.
3. Services, which can preform actions such as authentication or provide database access. By centralizing services we 
avoid duplicate code (or worse, multiple different implementation of the same thing).

Splitting makes the program easier to maintain, and built upon. And by splitting controllers it is easier to keep track 
of which endpoints require which authorization. This way we also have all database connections handled in a single
service, and no calls to the database are made anywhere else in the program.

### 2.5 Impersonation
There is only very limited ways to impersonate someone using this app: by choosing a username that is visually similar to 
the original (example: emma - ernma). Since usernames must be unique, and the sender is determined by the app there is
no other way of impersonation in the chat program (besides session high-jacking).

### 2.6 Logging in
All users have a unique username (enforced in the database). 
Whenever a user registers a secure random salt is generated for them and stored in the database together with the salted 
& hashed password. This way the plain text password is never stored anywhere.

### 2.7 Authorization
Whenever a user request messages from the server will identify the user and only provide them the messages 
that are either send to/by them. Since this is done serverside based on the session, the user cannot access messages of 
others.

## 3. Vulnerabilities
While the application is fairly simple I see 5 main vulnerabilities:
1. The first one was already briefly mentioned before: One could hihghjack another's session by correctly guessing, or 
obtaining their session token. While this is possible the tokens are temporary and very long, so I expect this risk to 
be minimal.
2. Since there are no rules for passwords, users might stick to simple passwords, which can be easily guessed by third 
parties.
3. While passwords are salted and hashed before being stored in the database, all messages are unencrypted. So if one 
would get a copy of the database they can see who communicated with who, and can see the contents of their messages.
4. During the logg in step a small randomized delay is added so a 'hacker' cannot know if the username they put in is 
wrong, or if only the password is wrong (so a 'hacker' cannot tell by processing time which usernames exist). However,
when sending a message the message requires a valid user to be the recipient or an error will be given. This can in turn
thus be used to see which usernames exist. The only protection to this is that the 'hacker' has to have logged into an 
account, which are very simple to make.
5. There is no protection to DoS attacks. A user can make as many requests as they want in as short amount of time as
they want, potentially hogging all the processing or network capabilities.

## 4. How to test
To start the application simply run:
`flask run`

Most features can be tested and verified by using the web application:
- Try injecting sql into any field (username, message, search) and see if something breaks
- Try to add html tags to anything that gets printed on screen: usernames, or messages.
- Try logging in with a wrong password

For the API part I highly recommend using postman to create requests. Be sure to use the Basic Auth header using 
username and password here.