const spawn = require("child_process").spawn
const ROUTERPATH = "pro-football-reference-web-scraper/pro_football_reference_web_scraper/node_router.py"

/**
 * Function to get a player's game log
 * "python" indicates we are looking to run a python script
 * arg[0] = file; path to the file from the root directory
 * method: indicates which python method we would like to obtain data from
 * name: name of player in question
 * position: position of player in question
 * year: year for which you would like to obtain the player's game log
 */
const getPlayerGameLog = (name, position, year, callback) => {
    /**
     * Spawn a child python process
     * "python" indicates terminal command to run the script
     * arg[0] = ROUTERPATH, or the path to the python routing file
     * arg[1] = gameLog; the code for getPlayerGameLog
     * arg[2] = name (mandatory for python child process)
     * arg[3] = position (mandatory for python child process)
     * arg[4] = year (mandatory for python child process)
     */
    const pythonProcess = spawn("python", [ROUTERPATH, "gameLog", name, position, year])
    var response = '' //store response from the python process

    //upon receipt of data from the child process, append the data received to the response
    pythonProcess.stdout.on('data', (data) => {
        response += data.toString()
    })

    //upon end of the child process, call the callback function with the data received from the child
    pythonProcess.stdout.on('end', () => {
        callback(response)
    })
}

//export the function for getting player game log data.
module.exports = getPlayerGameLog;