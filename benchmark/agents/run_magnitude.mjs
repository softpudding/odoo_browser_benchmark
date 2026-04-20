#!/usr/bin/env node
/**
 * Benchmark wrapper for Magnitude (https://github.com/magnitudedev/browser-agent).
 *
 * Setup:
 *     cd benchmark/agents && npm install magnitude-core
 *
 * Usage:
 *     uv run benchmark-eval run <task> --agent command \
 *         --cmd "node benchmark/agents/magnitude_agent.mjs"
 *
 * Env: Uses OPENAI_API_KEY (or DASHSCOPE_API_KEY mapped automatically).
 */

import { Agent } from "magnitude-core";

// Map DashScope to OpenAI-compatible if needed
if (!process.env.OPENAI_API_KEY && process.env.DASHSCOPE_API_KEY) {
  process.env.OPENAI_API_KEY = process.env.DASHSCOPE_API_KEY;
  process.env.OPENAI_BASE_URL =
    process.env.DASHSCOPE_BASE_URL ||
    process.env.BAILIAN_BASE_URL ||
    "https://dashscope.aliyuncs.com/compatible-mode/v1";
}

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

async function main() {
  const agent = new Agent();

  try {
    await agent.act(`Navigate to ${startUrl}`);

    if (login) {
      await agent.act(
        `Log in with username '${login}' and password '${password}'`
      );
    }

    await agent.act(instruction);

    console.log("Magnitude: task completed");
    process.exit(0);
  } catch (err) {
    console.error("Magnitude error:", err);
    process.exit(1);
  } finally {
    await agent.close();
  }
}

main().catch((err) => {
  console.error("Magnitude error:", err);
  process.exit(1);
});
