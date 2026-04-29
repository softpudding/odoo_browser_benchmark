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

// Build LLM config based on available API keys.
// Magnitude's BAML anthropic provider ignores baseUrl, so when ANTHROPIC_BASE_URL
// points at a non-Anthropic host (e.g. DashScope's Anthropic-compat shim), we can't
// use the 'anthropic' provider. Prefer 'openai-generic' against DashScope's
// OpenAI-compat endpoint whenever a DashScope/OpenAI key is available.
function buildLlmConfig() {
  // BENCHMARK_PROVIDER lets the caller force a provider when multiple keys are
  // present. Magnitude's pixel-coordinate clicks need a model with strong
  // visual grounding (Claude Sonnet's CUA training in particular); on
  // qwen/kimi the agent loops without finishing tasks. So when ANTHROPIC_API_KEY
  // is set, prefer Anthropic by default — even if a DashScope key is also
  // present.
  const provider = process.env.BENCHMARK_PROVIDER;
  const dashKey = process.env.DASHSCOPE_API_KEY || process.env.BAILIAN_API_KEY;

  if (provider === "anthropic" || (!provider && process.env.ANTHROPIC_API_KEY)) {
    return {
      provider: "anthropic",
      options: {
        // Project's README documents Sonnet 4 as the tested target
        // (claude-sonnet-4-20250514). Use it by default so numbers align
        // with the project's own benchmark evidence.
        model: process.env.BENCHMARK_MODEL || "claude-sonnet-4-20250514",
        apiKey: process.env.ANTHROPIC_API_KEY,
      },
    };
  }
  if (provider === "openai-generic" || dashKey || process.env.OPENAI_API_KEY) {
    const apiKey = process.env.OPENAI_API_KEY || dashKey;
    const baseUrl =
      process.env.OPENAI_BASE_URL ||
      process.env.DASHSCOPE_BASE_URL ||
      process.env.BAILIAN_BASE_URL ||
      "https://dashscope.aliyuncs.com/compatible-mode/v1";
    return {
      provider: "openai-generic",
      options: {
        model: process.env.BENCHMARK_MODEL || "qwen3.6-plus",
        apiKey,
        baseUrl,
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
  console.error(
    "ERROR: Set DASHSCOPE_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY"
  );
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
