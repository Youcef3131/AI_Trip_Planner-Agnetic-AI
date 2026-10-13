
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self,model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])
        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self,state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        for message in reversed(user_question):
            if isinstance(message, HumanMessage):
                request = message.content
                if isinstance(request, str):
                    self.place_search_tools.last_user_request = request
                break
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        for tool_call in response.tool_calls:
            if tool_call["name"] in {
                "search_attractions",
                "search_restaurants",
                "search_activities",
                "search_transportation",
            }:
                args = tool_call.get("args") or {}
                place = args.get("location") or args.get("city") or args.get("query")
                if place:
                    tool_call["args"] = {
                        "location": place,
                        "city": None,
                        "query": None,
                    }
                else:
                    tool_call["args"] = {
                        "location": self.place_search_tools.last_user_request,
                        "city": None,
                        "query": None,
                    }
        return {"messages": [response]}
    def build_graph(self):
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        self.graph = graph_builder.compile()
        return self.graph
        
    def __call__(self):
        return self.build_graph()