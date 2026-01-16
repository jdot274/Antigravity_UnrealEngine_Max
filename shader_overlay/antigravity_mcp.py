from mcp.server.fastmcp import FastMCP
import json
import os

# Initialize FastMCP Server
mcp = FastMCP("AntigravityTennis")

# Shared State (Simulated connection to Unreal)
STATE_FILE = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"

@mcp.tool()
def get_game_score() -> str:
    """Returns the current score of the Antigravity Tennis match."""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                score = data.get("tennis_score", {"p1": 0, "p2": 0})
                return f"Player 1: {score['p1']} | Player 2: {score['p2']}"
    except:
        pass
    return "Match not active or state unreachable."

@mcp.tool()
def cheer_for_player(player_name: str, message: str) -> str:
    """Displays a cheer message on the stadium overlay."""
    print(f"🎉 CHEER: {player_name} says '{message}'")
    # In a real impl, this would write to a 'cheer_queue.json' that Unreal reads
    return "Cheer sent to Stadium Hologram."

if __name__ == "__main__":
    mcp.run()
