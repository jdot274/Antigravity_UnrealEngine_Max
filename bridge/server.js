const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { CallToolRequestSchema, ListToolsRequestSchema } = require("@modelcontextprotocol/sdk/types.js");
const WebSocket = require("ws");
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const { GoogleGenerativeAI } = require("@google/generative-ai");
require("dotenv").config();

// --- CONFIGURATION ---
const WSS_PORT = 3001;
const HTTP_PORT = 3002;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "YOUR_KEY_HERE";

const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

// --- HTTP SERVER (Remote Chat Interface) ---
const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post("/chat", async (req, res) => {
  const { message, context } = req.body;
  console.error(`[Nexus Remote] Received: ${message}`);

  try {
    const prompt = `
      You are the Antigravity Nexus AI, an expert engineering assistant.
      Context: ${JSON.stringify(context || {})}
      Task: Respond to the user's request about the Antigravity project.
      User: ${message}
    `;

    const result = await model.generateContent(prompt);
    const responseText = result.response.text();

    // Relay to Canvas if needed
    broadcast("ai_response", { text: responseText, original: message });

    res.json({ response: responseText });
  } catch (error) {
    console.error("[Nexus Remote] Gemini Error:", error);
    res.status(500).json({ error: "Failed to communicate with Gemini API" });
  }
});

app.listen(HTTP_PORT, () => {
  console.error(`[Nexus Remote] HTTP Chat API running on port ${HTTP_PORT}`);
});

// --- WEBSOCKET SERVER (Canvas/Hub Sync) ---
const wss = new WebSocket.Server({ port: WSS_PORT });
console.error(`[Nexus Bridge] WebSocket server running on port ${WSS_PORT}`);

function broadcast(type, payload) {
  const message = JSON.stringify({ type, payload });
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// --- MCP SERVER ---
const mcpServer = new Server(
  {
    name: "Antigravity_UnrealEngine_Bridge",
    version: "1.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

mcpServer.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "add_card",
        description: "Add a card to the Nexus Canvas",
        inputSchema: {
          type: "object",
          properties: {
            title: { type: "string" },
            content: { type: "string" },
            type: { type: "string", enum: ["note", "task", "file"], default: "note" }
          },
          required: ["title", "content"],
        },
      },
      {
        name: "nexus_chat",
        description: "Talk to the Antigravity AI via Gemini",
        inputSchema: {
          type: "object",
          properties: {
            message: { type: "string", description: "The message to send to the AI" }
          },
          required: ["message"],
        },
      },
    ],
  };
});

mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "add_card") {
    broadcast("add_card", args);
    return { content: [{ type: "text", text: `Card '${args.title}' added to Canvas.` }] };
  }

  if (name === "nexus_chat") {
    const result = await model.generateContent(args.message);
    const text = result.response.text();
    broadcast("ai_chat", { text });
    return { content: [{ type: "text", text: text }] };
  }

  throw new Error(`Unknown tool: ${name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await mcpServer.connect(transport);
  console.error("[Nexus Bridge] MCP Server active");
}

main().catch(console.error);
