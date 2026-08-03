const projectName = "Playwright Lexical Test";
let runCount = 0;

function incrementRunCount() {
  runCount += 1;
  return runCount;
}



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
  add,
  buildReport,
};
