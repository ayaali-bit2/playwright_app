const projectName = "Playwright Lexical Test";
let runCount = 0;

function incrementRunCount() {
  runCount += 1;
  return runCount;
}

function formatSummary(userName) {
  const timestamp = new Date().toISOString();
  return `${projectName} - ${userName} - ${timestamp}`;
}

const createGreeter = (name) => {
  const safeName = String(name).trim() || "Guest";
  return `Hello, ${safeName}!`;
};

const add = (a, b) => a + b;

const buildReport = (items) => {
  const normalizedItems = Array.isArray(items) ? items : [];
  return {
    total: normalizedItems.length,
    firstItem: normalizedItems[0] ?? null,
  };
};

module.exports = {
  projectName,
  runCount,
  incrementRunCount,
  formatSummary,
  createGreeter,
  add,
  buildReport,
};
