const spawn = require("child_process").spawn
const pyDirectory = "pro-football-reference-web-scraper/pro_football_reference_web_scraper"

const pythonProcess = spawn("python",[pyDirectory + "/test-spawn.py", 44, 99]) //why do we need to run from the root?

pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString())
   })

pythonProcess.on('close', (data) => {
    console.log(data)
})