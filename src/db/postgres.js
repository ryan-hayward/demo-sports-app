const postgres = require('postgres')

//set up postgres db connection, 5432 default port
const sql = postgres({ 
    host: 'localhost',
    port: 5432,
    database:'demo-sports-app-db'
})

//MONGODB example
// mongoose.connect(process.env.MONGODB_URL, {
//     useNewUrlParser: true,
//     useCreateIndex: true,
//     useFindAndModify: false
// })