# Project 11 — Presentation and Live Demo Script

**Target speaking time:** approximately 4–5 minutes (plus any network delay).

## 1. Introduction (30 seconds)

“Good morning. Our project is **API Documentation with Scalar**. The idea is to document a public REST API using the **OpenAPI Specification**, render it into an interactive documentation page with **Scalar**, and demonstrate sending a real API request directly from the documentation. We've selected the public Chuck Norris Jokes API because it is easy to explore and doesn't need an API key.”

**Show:** the project's landing page.

## 2. OpenAPI explained (45 seconds)

“OpenAPI is a standard way of describing an HTTP API in YAML or JSON. It tells us where an API is hosted, which endpoints are available, which request parameters are accepted, and the shape of the responses. Our OpenAPI file has sections including `info`, `servers`, `paths`, and `components`. For example, `/jokes/search` needs a required `query` parameter. We also define a reusable Joke schema instead of copying the same response fields to every endpoint.”

**Show:** `openapi.yaml`, point at `servers`, `paths`, and `components.schemas`.

## 3. How Scalar works (45 seconds)

“Scalar is the API documentation tool. We load its JavaScript module through a CDN in our HTML page and point it to `openapi.json`. Scalar reads the specification and automatically renders the endpoints, parameters, descriptions, and response models. Scalar is not the backend; the real backend is still the remote Chuck Norris API. The reference also includes an API client so we can test the documented operations.”

**Show:** scroll to Live API reference, open an endpoint and show the generated docs.

## 4. Client demo (90 seconds)

“First, I'll demonstrate the categories endpoint. I select **GET /jokes/categories**, click **Test Request**, and then **Send Request**. We should receive a successful HTTP response and a JSON array of category strings. You can see these categories were not hard-coded into the documentation UI — they came from the actual API response.”

“Now I choose **GET /jokes/random**, enter `dev` as the category, and send it again. This time the result is one JSON object, with fields such as `id` and `value`. Finally, we can search by providing a keyword such as `computer` in the required `query` field of **GET /jokes/search**. The response includes `total` and the matching `result` array.”

**Show:** Scalar API client request URL / query controls and live response JSON. If a request fails, explain the HTTP status and mention internet, upstream availability or browser CORS rather than pretending success.

## 5. Architecture and conclusion (45 seconds)

“The architecture is simple: we write the contract in OpenAPI, Scalar transforms it into interactive documentation, and its embedded client sends requests to the remote API. Scalar itself is an open-source Vue and TypeScript project, and its reference and API-client packages share OpenAPI functionality. The main benefit is that documentation and testing are available in one place. We can also embed Scalar in larger backend frameworks rather than loading it through a CDN.”

“That's our demonstration of API Documentation with Scalar. Thank you.”

## Recommended evidence screenshots

1. Landing page with title, OpenAPI 3.1, Scalar and API summary.
2. Sidebar showing the three API operations.
3. Test Request / Send Request interface for `/jokes/categories`.
4. Response status and JSON result for `/jokes/categories`.
5. Search request with `query=computer` and returned result.

## Common viva questions

**Q: What is the difference between OpenAPI and Scalar?**  
A: OpenAPI is the machine-readable contract; Scalar is a tool that renders and uses that contract.

**Q: Does Scalar create our REST API?**  
A: No. It documents and tests an API that is actually provided by a backend.

**Q: Why use `$ref`?**  
A: To reuse models consistently. One `Joke` schema is referenced by multiple responses.

**Q: What is the difference between query parameters and path parameters?**  
A: Query parameters follow `?` in a URL, such as `?category=dev`. Path parameters are placeholders inside the URL path itself, such as `/jokes/{id}` — not used in our documented endpoints.

**Q: What does HTTP 200 mean?**  
A: The HTTP server successfully handled the request. The JSON payload shows its returned data.

**Q: Why is a proxy sometimes necessary?**  
A: Browsers enforce CORS policies for cross-origin requests; a compatible proxy can make permitted requests on behalf of the client.

**Q: Did we write a backend?**  
A: No. The assignment is focused on OpenAPI and Scalar, so we intentionally document a third-party API.
