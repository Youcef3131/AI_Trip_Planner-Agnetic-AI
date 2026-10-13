# AI Trip Planner

An agentic AI travel-planning application built with Python, FastAPI, Streamlit, LangGraph, and LangChain. The application generates detailed travel plans using an LLM and optional real-time services for places, weather, currency conversion, and trip-cost calculations.

## Features

- Day-by-day trip itineraries.
- Tourist attractions and off-the-beaten-path suggestions.
- Restaurant, activity, and transportation recommendations.
- Current weather and short-term weather forecasts.
- Currency conversion.
- Hotel and daily expense calculations.
- FastAPI backend with a `/query` endpoint.
- Streamlit user interface.
- Tool-calling workflow powered by LangGraph.
- Google Places fallback to Tavily search when Google Places is unavailable.

## Technology stack

- Python 3.13+
- FastAPI and Uvicorn
- Streamlit
- LangChain and LangGraph
- Groq or OpenAI chat models
- OpenWeatherMap
- Google Places
- Tavily Search
- ExchangeRate-API

## Project structure

```text
AI_Trip_Planner/
├── agent/
│   └── agentic_workflow.py       # LangGraph agent and tool routing
├── config/
│   └── config.yaml               # LLM provider and model configuration
├── logger/                       # Logging utilities
├── prompt_library/
│   └── prompt.py                 # System prompt for the travel agent
├── tools/
│   ├── currency_conversion_tool.py
│   ├── expense_calculator_tool.py
│   ├── place_search_tool.py
│   └── weather_info_tool.py
├── utils/
│   ├── currency_converter.py
│   ├── expense_calculator.py
│   ├── model_loader.py
│   ├── place_info_search.py
│   └── weather_info.py
├── main.py                       # FastAPI backend
├── streamlit_app.py              # Streamlit frontend
├── requirements.txt
├── pyproject.toml
└── setup.py
```

## Prerequisites

- Python 3.13 or newer.
- Git.
- API keys for the services you want to use.
- Windows PowerShell, macOS/Linux shell, or an equivalent terminal.

## Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/Youcef3131/AI_Trip_Planner-Agnetic-AI.git
cd AI_Trip_Planner-Agnetic-AI
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
py -3.13 -m venv env
.\env\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3.13 -m venv env
source env/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `pip` is unavailable in the virtual environment, recreate the environment or run:

```bash
python -m ensurepip --upgrade
python -m pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the project root. Never commit this file or share its values.

```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
GPLACES_API_KEY=your_google_places_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
FOURSQUARE_API_KEY=your_foursquare_api_key
```

### Required and optional keys

The default provider is Groq, so `GROQ_API_KEY` is required for the default configuration. `OPENAI_API_KEY` is only required if the provider is changed to OpenAI.

The following keys enable specific tools:

| Variable | Service | Used for |
|---|---|---|
| `GROQ_API_KEY` | Groq | Default chat model |
| `OPENAI_API_KEY` | OpenAI | Optional OpenAI chat model |
| `TAVILY_API_KEY` | Tavily | Web-search fallback |
| `GPLACES_API_KEY` | Google Places | Places, attractions, restaurants, and activities |
| `OPENWEATHERMAP_API_KEY` | OpenWeatherMap | Current weather and forecasts |
| `EXCHANGE_RATE_API_KEY` | ExchangeRate-API | Currency conversion |
| `FOURSQUARE_API_KEY` | Foursquare | Reserved for future place-search integration |

The application currently uses OpenWeatherMap for weather. Open-Meteo can be used as a free, keyless alternative, but the weather implementation must be adapted before switching providers.

## Model configuration

The configured models are stored in [config/config.yaml](config/config.yaml):

```yaml
llm:
  openai:
    provider: "openai"
    model_name: "o4-mini"
  groq:
    provider: "groq"
    model_name: "openai/gpt-oss-120b"
```

The backend currently creates the graph with the Groq provider by default.

## Running the application

Start the FastAPI backend from the project root:

### Windows PowerShell

```powershell
.\env\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Start the Streamlit frontend in a second terminal:

```powershell
.\env\Scripts\python.exe -m streamlit run streamlit_app.py
```

For macOS/Linux, use:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
python -m streamlit run streamlit_app.py
```

Open the URL displayed by Streamlit, normally:

```text
http://localhost:8501
```

The frontend sends travel requests to the backend at:

```text
http://localhost:8000/query
```

## API usage

The backend exposes:

```http
POST /query
Content-Type: application/json
```

Request body:

```json
{
  "query": "Plan a trip to Geneva for 3 days"
}
```

Successful response:

```json
{
  "answer": "Generated travel plan..."
}
```

Example with PowerShell:

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/query `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"query":"Plan a trip to Geneva for 3 days"}'
```

## Agent workflow

1. The user submits a travel request through Streamlit.
2. Streamlit sends the request to FastAPI.
3. FastAPI creates a LangGraph workflow.
4. The configured LLM decides which tools are needed.
5. LangGraph executes the selected tools.
6. Tool results are returned to the LLM.
7. The final Markdown travel plan is returned to Streamlit.

Available tools include:

- `get_current_weather`
- `get_weather_forecast`
- `search_attractions`
- `search_restaurants`
- `search_activities`
- `search_transportation`
- `estimate_total_hotel_cost`
- `calculate_total_expense`
- `calculate_daily_expense_budget`
- `convert_currency`

## Security

- Do not commit `.env`, API keys, or generated credentials.
- Rotate any API key that has been exposed publicly.
- Restrict Google API keys by API and application where possible.
- Use separate development and production keys.
- Do not place secrets directly in Python files or configuration committed to Git.
- Review third-party API quotas and billing settings before deployment.

## Troubleshooting

### Backend returns `422 Unprocessable Entity`

The request must use the `query` field:

```json
{
  "query": "Plan a trip to Paris"
}
```

### Backend returns a tool validation error

Restart Uvicorn after changing tool definitions. The backend must be restarted so LangChain rebuilds the tool schemas:

```powershell
.\env\Scripts\python.exe -m uvicorn main:app --reload
```

### API key errors

Check that:

- `.env` is located in the project root.
- The variable name is spelled correctly.
- The key is active and has the required API enabled.
- The service quota has not been exceeded.

### Port 8000 is already in use

Stop the previous Uvicorn process or use another port, then update `BASE_URL` in `streamlit_app.py` accordingly.

## Validation

Run a syntax check for the project source:

```powershell
.\env\Scripts\python.exe -m compileall -q -f main.py streamlit_app.py agent config logger prompt_library tools utils
```

The repository does not currently include an automated test suite. Add unit and integration tests before using the application in production.

## Limitations

- Recommendations and prices depend on external APIs and may be incomplete or outdated.
- API availability and quotas vary by provider.
- The generated travel plan should be verified before booking.
- Travel requirements, visa information, opening hours, transport schedules, and prices should be confirmed with official sources.
- This project is intended for development and demonstration unless additional production hardening is added.
