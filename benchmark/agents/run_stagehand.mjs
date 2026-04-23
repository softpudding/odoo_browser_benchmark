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
// Stagehand v3 requires "provider/model" form. Default to openai/qwen3.6-plus
// and point the OpenAI AI-SDK client at DashScope's compatible endpoint.
const useAnthropic = !!process.env.ANTHROPIC_API_KEY && !process.env.OPENAI_API_KEY;
const rawModel = process.env.BENCHMARK_MODEL || (useAnthropic ? "claude-sonnet-4-20250514" : "qwen3.6-plus");
const model = rawModel.includes("/")
  ? rawModel
  : (useAnthropic ? `anthropic/${rawModel}` : `openai/${rawModel}`);

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
  const clientOptions = useAnthropic
    ? { apiKey: process.env.ANTHROPIC_API_KEY, baseURL: process.env.ANTHROPIC_BASE_URL }
    : { apiKey: process.env.OPENAI_API_KEY, baseURL: process.env.OPENAI_BASE_URL };
  // Strip undefined baseURL so Stagehand falls back to provider default.
  for (const k of Object.keys(clientOptions)) {
    if (clientOptions[k] === undefined) delete clientOptions[k];
  }
  // Stagehand v3 takes `model: { modelName, ...clientOptions }` on both the
  // constructor and agent(); `modelName`/`modelClientOptions` top-level are
  // ignored (the constructor silently falls back to openai/gpt-4.1-mini).
  const modelConfig = { modelName: model, ...clientOptions };
  console.log(`Stagehand: using ${model} via ${clientOptions.baseURL ?? "provider default"}`);

  const stagehand = new Stagehand({
    env: "LOCAL",
    headless: false,
    enableCaching: false,
    model: modelConfig,
  });

  await stagehand.init();

  try {
    const pages = await stagehand.context.pages();
    const page = pages[0];
    await page.goto(startUrl);

    const agent = stagehand.agent({ model: modelConfig });
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
