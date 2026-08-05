const projectName = "playwright_app";
let runCount = 0;

function incrementRunCount() {
  runCount += 1;
  return runCount;
}

console.log(`${projectName} run #${incrementRunCount()}`);
