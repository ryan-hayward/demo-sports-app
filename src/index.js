//vanilla
const http = require('http')
const path = require('path')

//npm installs
const express = require('express')


//local imports




//set up express app
const app = express()
const server = http.createServer(app)
const port = process.env.PORT || 3000