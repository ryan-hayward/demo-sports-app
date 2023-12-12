const express = require('express')
require('./db/mongoose')
require('./db/postgres')
const userRouter = require('./routers/player-data')

const app = express()

app.use(express.json())
app.use(userRouter)

module.exports = app