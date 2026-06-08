# orchestrator.py
import os
import asyncio
import json
from typing import Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Ensure the Google Gen AI SDK can fetch the credentials smoothly
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("Missing GEMINI_API_KEY environment variable. Please check your .env file.")

client = genai.Client()

class MultiAgentTravelSystem:
    def __init__(self):
        # Configure operational guidelines for each agent node
        self.model_name = "gemini-2.5-flash"
        
    async def run_flight_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 1: Specialized in parsing flight payloads and narrowing choices."""
        prompt = f"""
        You are the Flight Search Agent. Analyze the travel route from {context['origin']} to {context['destination']}.
        Given these available raw flight options from the MCP Server: {json.dumps(context['raw_flights'])}
        Select the best option balancing efficiency and cost, and provide a clear structural summary.
        """
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return {"selected_flight": response.text}

    async def run_hotel_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 2: Handles hospitality evaluation."""
        prompt = f"""
        You are the Hotel Recommendation Agent. Review accommodations for {context['destination']}.
        Raw MCP data options: {json.dumps(context['raw_hotels'])}
        Synthesize the recommendation details matching a traveler's preference profile.
        """
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return {"selected_hotel": response.text}

    async def run_weather_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 3: Evaluates environmental and atmospheric factors for scheduling optimization."""
        # Mock weather data that would normally be fetched via weather_mcp.py
        mock_weather = {"forecast": "Clear skies, mild temperatures ranging from 18°C to 24°C. Perfect for walking tours."}
        
        prompt = f"""
        You are the Weather Information Agent. Analyze this forecast data for {context['destination']}: {mock_weather['forecast']}.
        Provide packing tips and highlight any days where outdoor activities should be prioritized.
        """
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return {"weather_profile": response.text}

    async def orchestrate_plan(self, origin: str, destination: str, duration_days: int, budget_tier: str) -> str:
        """
        Agent 4 (Orchestrator / Itinerary Planning Agent):
        Manages the complete lifecycle loop, triggers parallel processing of peer agents,
        handles A2A synthesis, and resolves conflicts into a cohesive plan.
        """
        print(f"[A2A ORCHESTRATOR] Initializing Travel Request to {destination} for {duration_days} days...")

        # 1. Simulating Tool Execution from the Underlying MCP Server Layer
        # (In an integrated runtime, the agents use tool-calling definitions to hit the MCP endpoints automatically)
        print("[A2A ORCHESTRATOR] Pulling ground-truth data structures from MCP Servers...")
        
        # Simulating external data retrieval locally for the assignment proof-of-concept
        from mcp_servers.travel_mcp import search_flights, recommend_hotels
        raw_flights = await search_flights(origin=origin, destination=destination, date="2026-10-12")
        raw_hotels = await recommend_hotels(destination=destination, tier=budget_tier)

        # 2. Parallelizing Peer Agent Executions (Simulating asynchronous A2A fan-out distribution)
        print("[A2A ORCHESTRATOR] Dispatching context sub-tasks to downstream specialized agents...")
        
        context_payload = {
            "origin": origin,
            "destination": destination,
            "raw_flights": raw_flights,
            "raw_hotels": raw_hotels
        }

        flight_task = self.run_flight_agent(context_payload)
        hotel_task = self.run_hotel_agent(context_payload)
        weather_task = self.run_weather_agent(context_payload)

        # Await the responses as part of the unified A2A communication stream
        flight_res, hotel_res, weather_res = await asyncio.gather(flight_task, hotel_task, weather_task)
        print("[A2A ORCHESTRATOR] Aggregated responses returned from all sub-agents successfully.")

        # 3. Comprehensive Final Synthesis
        print("[A2A ORCHESTRATOR] Synthesizing complete multi-agent itinerary...")
        final_synthesis_prompt = f"""
        You are the Master Itinerary Planning Agent. Your job is to compile a pristine, detailed travel itinerary.
        
        Trip Parameters:
        - Origin: {origin}
        - Destination: {destination}
        - Duration: {duration_days} Days
        
        Collaborative Agent Feedbacks (A2A Inputs):
        1. Flight Agent Decision: {flight_res['selected_flight']}
        2. Hotel Agent Decision: {hotel_res['selected_hotel']}
        3. Weather Agent Analysis: {weather_res['weather_profile']}
        
        Generate a comprehensive Travel Plan consisting of:
        - Flight Logistics Section
        - Hotel Lodging Section
        - Day-by-Day structured schedule accounting for the weather guidelines.
        Ensure it is structured cleanly with markdown headers.
        """

        master_response = client.models.generate_content(
            model=self.model_name,
            contents=final_synthesis_prompt,
        )
        
        return master_response.text

async def main():
    system = MultiAgentTravelSystem()
    final_itinerary = await system.orchestrate_plan(
        origin="Delhi",
        destination="Mumbai",
        duration_days=4,
        budget_tier="luxury"
    )
    print("\n=================== FINAL GENERATED TRAVEL PLAN ===================\n")
    print(final_itinerary)

if __name__ == "__main__":
    asyncio.run(main())