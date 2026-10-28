# Research Report: API Documentation with Scalar

**Project number:** 11  
**Selected API:** Chuck Norris Jokes API  
**Documentation tool:** Scalar  
**Specification language:** OpenAPI 3.1.0 (YAML / JSON)

## Abstract

API documentation explains how applications communicate with HTTP services. This project demonstrates how to describe a small third-party API through a machine-readable OpenAPI document and convert it into interactive documentation using Scalar. The reference covers random joke retrieval, category listing and text search. The same OpenAPI document powers endpoint explanations, data models, and a built-in client for submitting live requests. The implementation consists of static HTML/CSS/JavaScript and locally hosted OpenAPI files; the public Chuck Norris API provides the responses.

## 1. Introduction and objectives

An API (Application Programming Interface) defines how software systems exchange requests and responses. HTTP REST-style APIs typically expose resource URLs, use methods such as `GET` or `POST`, and return data as JSON. Good documentation should clearly state each request's URL, parameters, expected response codes and response fields.

**Objectives of this project:**

- Create a structured and reusable OpenAPI description of a real public service.
- Render that description through Scalar's interactive API Reference.
- Demonstrate request building, HTTP status, and JSON response inspection with Scalar's integrated client.
- Compare API specification, UI rendering, and the actual remote backend as distinct components.

## 2. What is OpenAPI?

The **OpenAPI Specification (OAS)** is a language-neutral description format for HTTP APIs. It allows people and programs to understand API capabilities without studying the backend code. Standard OpenAPI documents can be consumed by documentation generators, code-generation tools, validators and API clients.

### 2.1 Main sections of an OpenAPI document

| Section | Purpose | Example in this project |
|---|---|---|
| `openapi` | Declares the OpenAPI specification version | `3.1.0` |
| `info` | Metadata such as API title, version, description and contact | `Chuck Norris Jokes API` |
| `servers` | Base URL(s) where the service runs | `https://api.chucknorris.io` |
| `tags` | Logical grouping for operations | `Jokes`, `Categories` |
| `paths` | URL paths, methods, parameters and responses | `/jokes/search` with `GET` |
| `components` | Reusable definitions (schemas, parameters, security schemes, etc.) | `Joke` and `JokeSearchResponse` |
| `$ref` | References reusable definitions instead of duplicating schemas | `#/components/schemas/Joke` |

OpenAPI describes a **contract**: what to send, where to send it, and what to expect back. It does not itself implement or run those endpoints.

### 2.2 Example from the project

```yaml
openapi: 3.1.0
info:
  title: Chuck Norris Jokes API
  version: 1.0.0
servers:
  - url: https://api.chucknorris.io
paths:
  /jokes/search:
    get:
      summary: Search jokes using text
      parameters:
        - name: query
          in: query
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Search completed
```

The document shows that the caller makes a GET request to `https://api.chucknorris.io/jokes/search` and includes a required `query` field in the query string. A `200` response indicates the described success case. The project adds a response schema pointing to `JokeSearchResponse`.

## 3. What is Scalar and how does it render OpenAPI?

**Scalar API Reference** is an open-source renderer that converts an OpenAPI document into readable, navigable interactive developer documentation.

In this project, the rendering flow is:

1. **Specification file:** `openapi.json` declares the API's servers, operations, parameters, and schemas.
2. **Embed:** `index.html` loads the `@scalar/api-reference` package from a public CDN.
3. **Fetch and interpret:** Scalar loads the JSON specification, interprets its structures and resolves references to reusable schemas.
4. **Generate UI:** Scalar displays grouped endpoints, HTTP methods, descriptions, query inputs, code examples, and response models.
5. **Interactive testing:** The Test Request UI uses the specification to populate the HTTP request. When the user sends it, the client contacts the remote API and displays the response.

The two key distinctions are that **OpenAPI supplies the contract** and **Scalar supplies the interface**. The third-party Chuck Norris service supplies the live data.

### 3.1 How Scalar is put together (high-level architecture)

Scalar is an open-source **Vue 3 + TypeScript monorepo**, with multiple packages. Its main relevant pieces are:

- `@scalar/api-reference`: displays the documented API and its operations.
- `@scalar/api-client`: executes and inspects API requests, with an OpenAPI-native request model.
- Shared OpenAPI utilities and types: interpret documents and support reusable schemas.
- Shared components and themes: provide interface elements and visual styling.
- Framework integrations/CDN builds: make the same reference embeddable in different applications.

In our deliverable, the CDN build provides Scalar's prepared UI code. We do not need to install or compile Scalar's source repository. Its internal packages remain in the upstream project.

## 4. Embedding Scalar: CDN and framework integration

### 4.1 CDN integration (chosen)

The project uses the official HTML/JavaScript approach:

```html
<div id="app"></div>
<script type="module">
  import { createApiReference }
    from 'https://cdn.jsdelivr.net/npm/@scalar/api-reference/esm.js'

  createApiReference('#app', {
    url: './openapi.json',
    proxyUrl: 'https://proxy.scalar.com'
  })
</script>
```

The browser downloads the Scalar module from jsDelivr, reads `openapi.json` from the local server and builds the reference in the `#app` container. This needs no npm project, bundler, or backend framework.

### 4.2 Framework integration (alternative)

Scalar also provides integrations for server frameworks such as Express, Fastify, Hono, NestJS, Next.js, FastAPI and ASP.NET Core. In a larger backend, a framework typically exposes a generated OpenAPI document on one route and Scalar renders it at a documentation route (for example `/docs`). This can reduce manual syncing between implementation and documentation.

**Why CDN here?** The assignment focuses on OpenAPI and interactive documentation; a static site keeps the setup short and easy to explain.

## 5. What does Scalar's built-in API client do?

The Scalar client is an interface for making HTTP requests, similar in purpose to Postman. Based on an OpenAPI operation, it can display and configure:

- The HTTP method, server base URL and endpoint path.
- Query, path, and other request parameters.
- Applicable headers and, when relevant, request body and authentication requirements.
- The generated request and response status, response headers, and response body.

The standalone Scalar API Client also supports collections, environments and automated scripts/tests. The project needs only the built-in **Test Request** experience of the embedded API reference.

### 5.1 Demonstration workflow

**Test 1:** Select `GET /jokes/categories` and send the request. The expected successful *shape* is a JSON array of category names, not a single object.

**Test 2:** Select `GET /jokes/random`, enter `category=dev` and send. Expected successful shape: a JSON object with `id`, `value`, and metadata fields.

**Test 3:** Select `GET /jokes/search`, enter `query=computer` and send. Expected successful shape: JSON object with `total` and `result`.

For each request, the response depends on the external server and network connection. `200 OK` and example shapes are success expectations, not a claim that the app executed requests during report preparation.

## 6. API endpoints used

| HTTP method | Endpoint | Input | Expected response on success |
|---|---|---|---|
| GET | `/jokes/random` | Optional `category` | `Joke` JSON object |
| GET | `/jokes/categories` | None | JSON array of strings |
| GET | `/jokes/search` | Required `query` | `{total: integer, result: Joke[]}` |

**Security:** The selected public endpoints do not require authentication.  
**Data format:** JSON.  
**Server:** `https://api.chucknorris.io`.

There are three URL paths and three operations; the random operation has two demonstration modes (with and without the category query).

## 7. Benefits, limitations, and findings

**Benefits:**

1. **Single source of truth:** One OpenAPI specification powers the API reference and client.
2. **Consistency:** Reusable schemas prevent repetitive definitions.
3. **Low setup complexity:** CDN integration works with a static local web server.
4. **Faster testing:** Request parameters and paths are visible next to the documentation.
5. **Portability:** OpenAPI YAML/JSON can be reused with different standards-compliant tools.

**Limitations and considerations:**

- The documentation can become inaccurate if a third-party API changes while the handwritten spec does not.
- API availability and response times depend on the upstream provider.
- Browser CORS policy may prevent cross-origin HTTP requests. Scalar's hosted proxy can help, but relaying requests through a third party raises privacy considerations for confidential APIs.
- The public API returns dynamic data; example outputs are not guaranteed to repeat word for word.
- Serving a UI through the Scalar CDN requires network access; only the project's static assets are stored locally.

## 8. Conclusion

This project demonstrates how OpenAPI standardizes API descriptions and Scalar makes that description usable. The OpenAPI file defines what each endpoint accepts and returns. The Scalar API Reference presents the definition as interactive documentation, and its built-in client can generate and send requests to the public Chuck Norris API. Combining structured documentation with live testing makes APIs easier to learn, verify and integrate.

## 9. References

1. OpenAPI Initiative. *OpenAPI Specification v3.1.0.* https://spec.openapis.org/oas/v3.1.0
2. Scalar. *API Reference with HTML/JS.* https://scalar.com/products/api-references/integrations/html-js
3. Scalar. *API Reference Configuration.* https://scalar.com/products/api-references/configuration
4. Scalar. *Open-source API Client.* https://scalar.com/products/api-client
5. Scalar GitHub. *Repository architecture (AGENTS.md).* https://github.com/scalar/scalar/blob/main/AGENTS.md
6. Chuck Norris API. *Official API documentation.* https://api.chucknorris.io/

*Research checked against official online documentation on 24 October 2026.*
