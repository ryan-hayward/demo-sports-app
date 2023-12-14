const app = require('./app')

const port = process.env.PORT

// Adding comments to test git commit on new email address
app.listen(port, (err) => {
    if (err) console.log(err);
    console.log('Server is up and running on port ' + port)
})