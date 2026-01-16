from mcp.server.fastmcp import FastMCP
import json
import os
import math

# Initialize Galaxy Knowledge Server
mcp = FastMCP("GalaxyKnowledge")

DB_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/galaxy_knowledge_db.json"

def _load_db():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def _cosine_similarity(v1, v2):
    "Simple manual cosine similarity for 3D simulation vectors"
    dot = sum(a*b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a*a for a in v1))
    norm_b = math.sqrt(sum(b*b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

@mcp.tool()
def search_knowledge(query: str) -> str:
    """
    Searches the Galaxy Knowledge Vector Database for relevant tasks, ideas, or code snippets.
    Supports semantic matching (simulated).
    """
    data = _load_db()
    if not data:
        return "🌌 Galaxy Knowledge Empty."
    
    # In a real system, we'd embed the query. 
    # Here we do a keyword match + simulated vector ranking.
    results = []
    
    print(f"🔍 Searching Galaxy for: '{query}'")
    
    for entry in data:
        score = 0
        # Keyword Boost
        if query.lower() in entry['content'].lower() or query.lower() in entry['topic'].lower():
            score += 0.5
            
        # Simulated Vector Similarity (Randomized/Hash-based for demo if no real embedding)
        # For now, just utilizing the keyword score mostly.
        
        if score > 0:
            results.append((score, entry))
            
    results.sort(key=lambda x: x[0], reverse=True)
    
    if not results:
        return "No matching galaxy knowledge found."
        
    response = "🌌 **Galaxy Knowledge Search Results:**\n"
    for score, item in results[:3]:
        response += f"- **[{item['category']}] {item['topic']}**: {item['content']}\n"
        
    return response

@mcp.tool()
def add_knowledge(topic: str, category: str, content: str) -> str:
    """Adds a new knowledge entry to the vector database."""
    import uuid
    import datetime
    
    entry = {
        "id": str(uuid.uuid4()),
        "category": category,
        "topic": topic,
        "content": content,
        "timestamp": datetime.datetime.now().isoformat(),
        "vector": [0.5, 0.5, 0.5] # Default neutral vector
    }
    
    data = _load_db()
    data.append(entry)
    
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=4)
        
    return f"✅ Knowledge '{topic}' added to Galaxy Database."

@mcp.tool()
def read_all_tasks() -> str:
    """Returns all logged tasks from the database."""
    data = _load_db()
    tasks = [d for d in data if d['category'] == 'Task']
    if not tasks:
        return "No tasks logged."
        
    result = "📋 **Active Galaxy Tasks:**\n"
    for t in tasks:
        result += f"- {t['topic']}\n"
    return result

if __name__ == "__main__":
    mcp.run()
