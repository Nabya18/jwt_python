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
# File Structure
## models.py - Domain Models and Interfaces
1. Contains the core business entities (Url, User)
2. Abstract repository interfaces 
3. No external dependencies - pure domain logic

## services.py - Business Logic Layer
1. UrlShortenerService: URL business logic 
2. AuthService: Authentication business logic 
3. JWTService: Token management 
4. Contains all use cases and business rules

## repositories.py - Data Access Layer
1. SQLiteUrlRepository: Database implementation 
2. InMemoryAuthRepository: Simple auth storage 
3. Handles all data persistence concerns

## controllers.py - Web Controllers
1. UrlController: HTTP request handling for URLs 
2. AuthController: HTTP request handling for authentication 
3. Separates web concerns from business logic

## app.py - Application Factory
1. Flask app creation and configuration 
2. Dependency injection setup 
3. Route definitions 
4. Main entry point
---
Note: Focus on functionality and code readability
1. url_root = The URL with scheme, host, and root path. For example, https://example.com/app/.
2. jsonify() is a built-in Flask function that converts Python dictionaries and objects into JSON response objects.
3. JSON Web Token (JWT) is a compact URL-safe means of representing claims to be transferred between two parties.
4. Wraps() is a decorator that is applied to the wrapper function of a decorator. 
   It updates the wrapper function to look like wrapped function by copying attributes such as __name__, __doc__ (the docstring), etc.
5. What are GET, POST, PUT, PATCH, DELETE
   - GET method is used to retrieve data from the server. This is a read-only method for example, if we call the get method on our API, we’ll get back a list of all to-dos.
   - POST method sends data to the server and creates a new resource.  In short, this method is used to create a new data entry.
   - PUT method to update a specific resource (which comes with a specific URI)  with the request body containing the complete new version of the resource you are trying to update.
   - PATCH method, the request body only needs to contain the specific changes to the resource, specifically a set of instructions describing how that resource should be changed, and the API service will create a new version according to that instruction.
   - DELETE method is used to delete a resource specified by its URI.
6. URI vs URL
   - URL (Uniform Resource Locator) is often defined as a string of characters that is directed to an address. To locate a resource on the internet.
   - URI is additionally grouped as a locator, a name or both which suggests it can describe a URL, URN or both.
7. Comparison Between URL vs URI vs URN

| Aspect | **URI** (Uniform Resource Identifier) | **URL** (Uniform Resource Locator) | **URN** (Uniform Resource Name) |
|---|---|---|---|
| **Purpose** | General identifier for a resource. | Identifies a resource **by location** and how to **access** it. | Provides a **persistent, location-independent** identifier. |
| **Structure** | `scheme ":" hier-part [ "?" query ] [ "#" fragment ]` (umbrella format that includes URLs and URNs). | **scheme** (protocol) + **authority/host** + path; may include **query** and **fragment**. | `urn ":" NID ":" NSS` → **scheme** (`urn`), **Namespace ID**, **Namespace-Specific String**. |
| **Usage** | Overarching term covering both URLs and URNs. | Most common on the web to **directly access** pages, APIs, files, etc. | Used where **stable identifiers** matter (e.g., books, standards, archives). |
| **Examples** | `mailto:support@example.com`, `https://example.com/a?x=1#top`, `urn:isbn:0451450523` | `https://example.com/a?x=1#top`, `ftp://ftp.example.org/file.txt` | `urn:isbn:0451450523`, `urn:uuid:123e4567-e89b-12d3-a456-426614174000` |
| **Key Point** | **All URLs and URNs are URIs**, but not all URIs are URLs or URNs. | A **subset of URI** focused on **where/how** to retrieve. | A **subset of URI** focused on **what** the resource is, not where it lives. |

8. Context managers are the rescue for this issue by automatically managing resources.
9. RS256 vs HS256 in JWT
   - HS256 (HMAC with SHA-256) is a symmetric algorithm that shares one secret key between the identity provider and your application. The same key is used to sign a JWT and verify that signature.
   - RS256 (RSA Signature with SHA-256) is an asymmetric algorithm that uses a private key to sign a JWT and a public key to verify that signature.