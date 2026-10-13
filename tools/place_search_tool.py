import os
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from typing import List, Optional
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.last_user_request = ""
        self.google_api_key = os.environ.get("GPLACES_API_KEY")
        self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        def resolve_place(
            location: Optional[str] = None,
            city: Optional[str] = None,
            query: Optional[str] = None,
        ) -> str:
            place = location or city or query or self.last_user_request
            if not place or not place.strip():
                return "the requested destination"
            return place.strip()

        @tool
        def search_attractions(
            location: Optional[str] = None,
            city: Optional[str] = None,
            query: Optional[str] = None,
        ) -> str:
            """Search attractions. Provide the city or destination as location, city, or query."""
            place = resolve_place(location, city, query)
            try:
                attraction_result = self.google_places_search.google_search_attractions(place)
                if attraction_result:
                    return f"Following are the attractions of {place} as suggested by google: {attraction_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_restaurants(
            location: Optional[str] = None,
            city: Optional[str] = None,
            query: Optional[str] = None,
        ) -> str:
            """Search restaurants. Provide the city or destination as location, city, or query."""
            place = resolve_place(location, city, query)
            try:
                restaurants_result = self.google_places_search.google_search_restaurants(place)
                if restaurants_result:
                    return f"Following are the restaurants of {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_activities(
            location: Optional[str] = None,
            city: Optional[str] = None,
            query: Optional[str] = None,
        ) -> str:
            """Search activities. Provide the city or destination as location, city, or query."""
            place = resolve_place(location, city, query)
            try:
                restaurants_result = self.google_places_search.google_search_activity(place)
                if restaurants_result:
                    return f"Following are the activities in and around {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_transportation(
            location: Optional[str] = None,
            city: Optional[str] = None,
            query: Optional[str] = None,
        ) -> str:
            """Search transportation. Provide the city or destination as location, city, or query."""
            place = resolve_place(location, city, query)
            try:
                restaurants_result = self.google_places_search.google_search_transportation(place)
                if restaurants_result:
                    return f"Following are the modes of transportation available in {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]