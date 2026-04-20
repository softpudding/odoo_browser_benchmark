#!/usr/bin/env node
/**
 * Benchmark wrapper for Stagehand (https://github.com/browserbase/stagehand).
 *
 * Setup:
 *     cd benchmark/agents && npm install @browserbasehq/stagehand
 *
 * LIMITATION: Stagehand v2 hardcodes "openai/gpt-4.1-mini" and ignores
 * custom modelName in LOCAL mode. Requires OPENAI_API_KEY with access to
 * gpt-4.1-mini. DashScope/Qwen models are NOT supported.
 *
 * Usage:
 *     uv run benchmark-eval run <task> --agent command \
 *         --cmd "node benchmark/agents/run_stagehand.mjs"
 */

import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { Stagehand } = require("@browserbasehq/stagehand");

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
const model = process.env.BENCHMARK_MODEL || "qwen3.6-plus";

if (!instruction || !startUrl) {
  console.error(
    "ERROR: BENCHMARK_INSTRUCTION and BENCHMARK_START_URL must be set"
  );
  process.exit(1);
}

let fullInstruction = "";
if (login) {
  fullInstruction = `First, log in with username '${login}' and password '${password}'. Then: `;
}
fullInstruction += instruction;

async function main() {
  const stagehand = new Stagehand({
    env: "LOCAL",
    headless: false,
    enableCaching: false,
    modelName: model,
    modelClientOptions: {
      apiKey: process.env.OPENAI_API_KEY,
      baseURL: process.env.OPENAI_BASE_URL,
    },
  });

  await stagehand.init();

  try {
    const pages = await stagehand.context.pages();
    const page = pages[0];
    await page.goto(startUrl);

    const agent = stagehand.agent({
      modelName: model,
      modelClientOptions: {
        apiKey: process.env.OPENAI_API_KEY,
        baseURL: process.env.OPENAI_BASE_URL,
      },
    });
    const result = await agent.execute({
      instruction: fullInstruction,
      maxSteps: parseInt(process.env.BENCHMARK_MAX_STEPS || "200", 10),
    });

    console.log("Stagehand result:", JSON.stringify(result, null, 2));

    if (result && result.success !== false) {
      process.exit(0);
    } else {
      process.exit(1);
    }
  } finally {
    await stagehand.close();
  }
}

main().catch((err) => {
  console.error("Stagehand error:", err);
  process.exit(1);
});
