# Project 11 — API Documentation with Scalar

**Topic:** API Documentation with Scalar  
**Public API:** Chuck Norris Jokes API — https://api.chucknorris.io/  
**OpenAPI version:** 3.1.0  
**Technology:** HTML, CSS, JavaScript, Scalar API Reference (CDN), YAML / JSON  
**Backend/database installation:** None required. The upstream public API is hosted by its original provider.

## 1. Objective

Document a small public REST API in OpenAPI, display the documentation in Scalar, and use Scalar's built-in **Test Request** client to send real HTTP GET requests and inspect the HTTP response.

## 2. Run the project

1. Extract `Scalar_API_Documentation_Project.zip`.
2. Open a Terminal or Command Prompt in the extracted `scalar-chucknorris-project` folder.
3. Start a local static HTTP server:

   **macOS/Linux:**
   ```bash
   python3 -m http.server 8000
   ```
   Or run `./start.sh` in the extracted directory.

   **Windows:**
   ```bat
   py -m http.server 8000
   ```
   Or double-click `start.bat` if Python is configured with the `py` launcher.

4. Open **http://localhost:8000/** in Chrome, Firefox, Edge, or Safari.
5. Scroll down to the **Live API reference** rendered by Scalar.

> **Important:** Do not double-click `index.html` and open it as `file://`. A local HTTP server is necessary so the browser can load `openapi.json` normally. Internet access is required for the Scalar CDN and external API.

## 3. Demonstrate the built-in API client

### Demo A — Get categories (recommended first)

1. In the Scalar API reference, select **GET `/jokes/categories`**.
2. Press **Test Request** to launch the interactive request client (label may vary slightly with Scalar versions).
3. Confirm the server is `https://api.chucknorris.io` and method is `GET`.
4. Select **Send Request**.
5. Describe the response: a successful request normally returns **HTTP 200** and an array such as `['animal', 'career', 'dev', ...]` in JSON format.

### Demo B — Category-filtered joke

1. Select **GET `/jokes/random`**.
2. Set query parameter **`category` = `dev`**.
3. Click **Test Request → Send Request**.
4. Explain that changing the optional query parameter changes the server-side filtering and the returned JSON object has an `id` and `value` (joke text), among other fields.

### Demo C — Search jokes

1. Select **GET `/jokes/search`**.
2. Set required query parameter **`query` = `computer`**.
3. Click **Test Request → Send Request**.
4. Explain `total` (number of matches) and `result` (array of matching Joke objects).

The exact joke text and the search `total` may vary. Do not claim fixed results because these are live requests to an external service.

### Equivalent requests (for comparison only)

```bash
curl -i 'https://api.chucknorris.io/jokes/categories'
curl -i 'https://api.chucknorris.io/jokes/random?category=dev'
curl -i 'https://api.chucknorris.io/jokes/search?query=computer'
```

The actual project demo should use **Scalar's Test Request**, not only cURL.

## 4. Project files

| File | Purpose |
|---|---|
| `index.html` | Landing page and Scalar API Reference CDN embed |
| `openapi.yaml` | Human-readable OpenAPI 3.1 definition |
| `openapi.json` | Equivalent JSON document loaded by Scalar |
| `RESEARCH_REPORT.md` | Background research, architecture, key findings and references |
| `PRESENTATION_SCRIPT.md` | Ready-to-speak project walkthrough with suggested screenshots |
| `validate.py` | Offline static consistency and structural checks; optional network check |
| `start.sh` / `start.bat` | Convenience local-server launch scripts |

## 5. Architecture

```text
openapi.yaml  ──(equivalent)──>  openapi.json
                                     │
                                     ▼
    index.html + Scalar CDN → Scalar parses the spec
                                     │
                          ┌──────────┴──────────┐
                          ▼                     ▼
                     API reference        Test Request client
                                                    │
                                                    ▼
                                     https://api.chucknorris.io
                                                    │
                                                    ▼
                                        HTTP response (JSON)
```

The Scalar UI is *not* a backend. Scalar renders the specification and acts as an interface for requests to the remote API.

## 6. Validation

Run the offline structure checks:

```bash
python3 validate.py
```

To additionally check the upstream API over the internet (optional):

```bash
python3 validate.py --live
```

Checks include the expected endpoints, GET operations, response definitions, valid `$ref` schemas, equivalence between the YAML and JSON files (when PyYAML is installed), and optional live response shapes. Live checks require DNS and internet access and could fail because of connectivity or upstream service availability.

## 7. Troubleshooting

| Symptom | What to try |
|---|---|
| Scalar panel remains on “Loading” | Check internet/CDN access; refresh; try another browser; inspect browser console |
| `openapi.json` fails to load | Confirm you opened `http://localhost:8000/`, not a `file://` URL |
| Browser says CORS blocked | Scalar is configured with the public `proxy.scalar.com`; ensure it is reachable. Try direct cURL for comparison |
| API returns an error or times out | Recheck network connection and try `/jokes/categories`; external APIs sometimes have outages |
| Port `8000` already used | Run `python3 -m http.server 8080` and visit `http://localhost:8080/` |
| `python3` command missing | Install Python 3 or use another static file server, for example `npx serve .` |

**Privacy caution:** A proxy relays requests through a third party. This classroom demo requires no API key and sends only public, unauthenticated GET requests. Do not send private credentials through the hosted proxy.

## 8. Screenshots for submission

Run and demonstrate the site in your own browser, then capture **actual** screenshots of:

1. Project landing page and Scalar reference, with all three endpoints visible.
2. `/jokes/categories` selected inside Scalar.
3. Scalar **Test Request** panel showing a successful real response.
4. `/jokes/search` with `query=computer` and the returned JSON.

Screenshots are not pre-included because this workspace could not reach the public API from its command-line runtime. A live Scalar request should be tested from your browser before final submission.

## 9. Sources

- Official API: https://api.chucknorris.io/
- OpenAPI 3.1 standard: https://spec.openapis.org/oas/v3.1.0
- Scalar HTML/JavaScript integration: https://scalar.com/products/api-references/integrations/html-js
- Scalar API Reference configuration: https://scalar.com/products/api-references/configuration
- Scalar API Client: https://scalar.com/products/api-client
- Scalar source architecture: https://github.com/scalar/scalar/blob/main/AGENTS.md
