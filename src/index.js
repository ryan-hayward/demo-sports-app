const app = require('./app')

const port = process.env.PORT

app.listen(port, (err) => {
    if (err) console.log(err);
    console.log('Server is up and running on port ' + port)
})