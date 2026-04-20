#!/usr/bin/env node
/**
 * Benchmark wrapper for Magnitude (https://github.com/magnitudedev/browser-agent).
 *
 * Setup:
 *     cd benchmark/agents && npm install magnitude-core
 *
 * Requires ANTHROPIC_API_KEY (uses Claude) or GOOGLE_API_KEY (uses Gemini).
 *
 * Usage:
 *     uv run benchmark-eval run <task> --agent command \
 *         --cmd "node benchmark/agents/run_magnitude.mjs"
 */

import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { Agent, BrowserConnector } = require("magnitude-core");

const instruction = process.env.BENCHMARK_INSTRUCTION;
const startUrl = process.env.BENCHMARK_START_URL;
const login = process.env.BENCHMARK_LOGIN || "";
const password = process.env.BENCHMARK_PASSWORD || "";

if (!instruction || !startUrl) {
  console.error(
    "ERROR: BENCHMARK_INSTRUCTION and BENCHMARK_START_URL must be set"
  );
  process.exit(1);
}

// Build LLM config based on available API keys
function buildLlmConfig() {
  if (process.env.ANTHROPIC_API_KEY) {
    return {
      provider: "anthropic",
      options: {
        model: process.env.BENCHMARK_MODEL || "claude-sonnet-4-20250514",
        apiKey: process.env.ANTHROPIC_API_KEY,
      },
    };
  }
  if (process.env.GOOGLE_API_KEY) {
    return {
      provider: "google-ai",
      options: {
        model: process.env.BENCHMARK_MODEL || "gemini-2.5-pro-preview-05-06",
        apiKey: process.env.GOOGLE_API_KEY,
      },
    };
  }
  if (process.env.OPENAI_API_KEY) {
    return {
      provider: "openai",
      options: {
        model: process.env.BENCHMARK_MODEL || "gpt-4o",
        apiKey: process.env.OPENAI_API_KEY,
      },
    };
  }
  console.error("ERROR: Set ANTHROPIC_API_KEY, GOOGLE_API_KEY, or OPENAI_API_KEY");
  process.exit(1);
}

let fullInstruction = "";
if (login) {
  fullInstruction = `First, log in with username '${login}' and password '${password}'. Then: `;
}
fullInstruction += instruction;

async function main() {
  const llm = buildLlmConfig();
  console.log(`Magnitude: using ${llm.provider}/${llm.options.model}`);

  const agent = new Agent({
    llm,
    connectors: [
      new BrowserConnector({
        url: startUrl,
        browser: { headless: false },
      }),
    ],
  });

  try {
    await agent.start();
    await agent.act(fullInstruction);

    console.log("Magnitude: task completed");
    process.exit(0);
  } catch (err) {
    console.error("Magnitude error:", err.message || err);
    process.exit(1);
  } finally {
    await agent.close();
  }
}

main().catch((err) => {
  console.error("Magnitude error:", err.message || err);
  process.exit(1);
});
