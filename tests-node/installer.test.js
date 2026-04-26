"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const {
  SKILL_DIR_NAME,
  installTargets,
  listTargets,
  normalizeTarget,
  normalizeTargetList,
  resolveInstallPlans,
} = require("../lib/installer");

const PROJECT_ROOT = path.resolve(__dirname, "..");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

test("normalizeTarget supports canonical single target", () => {
  assert.equal(normalizeTarget("codex"), "codex");
  assert.equal(normalizeTarget("claude-code"), "claude");
  assert.equal(normalizeTarget("gemini-cli"), "gemini");
});

test("normalizeTargetList expands aliases and all", () => {
  assert.deepEqual(normalizeTargetList("cursor,copilot,trae-cn"), [
    "cursor",
    "copilot",
    "trae",
  ]);
  assert.deepEqual(normalizeTargetList("all"), [
    "codex",
    "claude",
    "gemini",
    "opencode",
    "windsurf",
    "copilot",
    "agent-skills",
  ]);
});

test("resolveInstallPlans creates official wrapper artifacts for claude and gemini", () => {
  const projectDir = path.join(os.tmpdir(), "zentao-workflow-install-plan");
  const claudePlan = resolveInstallPlans({
    target: "claude",
    scope: "project",
    projectDir,
  });
  const geminiPlan = resolveInstallPlans({
    target: "gemini",
    scope: "project",
    projectDir,
  });

  assert.equal(claudePlan.plans.length, 3);
  assert.equal(geminiPlan.plans.length, 3);
  assert.ok(
    claudePlan.plans.some((plan) =>
      plan.destinationPath.endsWith(path.join(".claude", "commands", "zentao-workflow.md")),
    ),
  );
  assert.ok(
    geminiPlan.plans.some((plan) =>
      plan.destinationPath.endsWith(path.join(".gemini", "commands", "zentao-workflow.toml")),
    ),
  );
});

test("installTargets writes runtime bundle and wrapper files", () => {
  const projectDir = fs.mkdtempSync(
    path.join(os.tmpdir(), "zentao-workflow-install-"),
  );

  const result = installTargets({
    target: "claude,opencode,copilot,cursor",
    scope: "project",
    projectDir,
  });

  assert.deepEqual(result.targets, ["claude", "opencode", "copilot", "cursor"]);
  assert.ok(
    fs.existsSync(
      path.join(projectDir, ".claude", "commands", "zentao-workflow.md"),
    ),
  );
  assert.ok(
    fs.existsSync(
      path.join(projectDir, ".claude", "agents", "zentao-workflow.md"),
    ),
  );
  assert.ok(
    fs.existsSync(
      path.join(projectDir, ".claude", "agent-resources", SKILL_DIR_NAME, "SKILL.md"),
    ),
  );
  assert.ok(
    fs.existsSync(
      path.join(projectDir, ".opencode", "skills", SKILL_DIR_NAME, "SKILL.md"),
    ),
  );
  assert.ok(
    fs.existsSync(
      path.join(projectDir, ".github", "skills", SKILL_DIR_NAME, "SKILL.md"),
    ),
  );
  assert.ok(
    fs.existsSync(
      path.join(projectDir, ".agents", "skills", SKILL_DIR_NAME, "scripts", "chandao_fetch.py"),
    ),
  );
  assert.equal(
    fs.existsSync(
      path.join(
        projectDir,
        ".agents",
        "skills",
        SKILL_DIR_NAME,
        "scripts",
        "chandao_fetch",
        "__pycache__",
      ),
    ),
    false,
  );
});

test("package.json version stays in sync with VERSION", () => {
  const packageJson = readJson(path.join(PROJECT_ROOT, "package.json"));
  const version = fs.readFileSync(path.join(PROJECT_ROOT, "VERSION"), "utf8").trim();
  assert.equal(packageJson.version, version);
});

test("listTargets exposes mainstream agent targets", () => {
  const ids = listTargets().map((target) => target.id);
  assert.deepEqual(ids, [
    "codex",
    "claude",
    "gemini",
    "opencode",
    "windsurf",
    "agent-skills",
    "cursor",
    "copilot",
    "trae",
  ]);
});
