const { exec } = require("child_process");

const run = (command) => {
  const process = exec(command);
  process.stdout.pipe(process.stdout);
  process.stderr.pipe(process.stderr);
};

run("start cmd /k python main.py");
run("start cmd /k python backend.py");
run("start cmd /k python ws_server.py");
run("start cmd /k npm run electron");
