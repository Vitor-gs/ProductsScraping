# ProductsScraping

A Python-based web scraping project to extract product data from Baldor's online catalog: [https://www.baldor.com/catalog](https://www.baldor.com/catalog)

## Project Scope

This scraper collects data for two major product lines from Baldor’s catalog: **AC Motors** and **DC Motors**. Only the categories listed below are included in the scraping process.

### Targeted Product Categories

- **AC Motors**
  - General Purpose
  - Severe Duty
  - Washdown Duty
  - Explosion Proof
  - Pump
  - HVAC
  - Farm Duty
  - Definite Purpose
  - Unit Handling
  - Variable Speed AC
  - Custom AC Motors

- **DC Motors**
  - Integral HP and RPM III
  - Fractional and Permanent Magnet


## Technologies Used

- **Python**
  - `requests` for HTTP requests
  - `BeautifulSoup` for HTML parsing

## How to Run

### Option 1 – Using `uv`

1. Clone this repository.
2. Install `uv`.
3. Run the script:
```bash
  python src/main.py
```
If the above doesn't work, try:
```bash
  uv run --script src/main.py
```

### Option 2 – Traditional Virtual Environment

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies from _requirements.txt_.
4. Run the script:
```bash
  python src/main.py
```

## Potential Improvements

While the current implementation uses synchronous requests (via the `requests` library), which is straightforward and reliable, there is room to improve efficiency.

As a possible enhancement, adopting asynchronous requests using tools like `httpx` in combination with `asyncio` could help reduce overall scraping time. This approach would allow multiple HTTP requests (such as asset downloads) to be processed concurrently, potentially improving performance without changing the core scraping logic.
