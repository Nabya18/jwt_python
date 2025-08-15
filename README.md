# Description:
Create a service used to shorten a link to make it short, for example: from: https://github.com/Nabya18/flask_tutorial to: http://localhost/l/a
## Minimum Criteria:
    - CRUD API 
    - Can redirect using header method when opening the link 
    - Can save to database

## Technology:
Python and Flask

## Additional:
- Best practice API naming api/v1/...
- Clean code structure
- Using clean architecture
- Implement login and JWT

---
Note: Focus on functionality and code readability
1. url_root = The URL with scheme, host, and root path. For example, https://example.com/app/.
2. jsonify() is a built-in Flask function that converts Python dictionaries and objects into JSON response objects.
3. JSON Web Token (JWT) is a compact URL-safe means of representing claims to be transferred between two parties.
4. Wraps() is a decorator that is applied to the wrapper function of a decorator. 
   It updates the wrapper function to look like wrapped function by copying attributes such as __name__, __doc__ (the docstring), etc.