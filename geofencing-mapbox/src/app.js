const path = require('path')
const express = require('express')

const app = express()
const publicDirectoryPath = path.join(__dirname, '../public')

app.use(express.static(publicDirectoryPath))


app.get('/', function (req, res) {
  res.send('Hello World')
})
 
app.listen(3000, () => {
  console.log("server is running on port 3000")
})