const http = require("http");
const fs = require("fs");

const port = 8080;
const path  = process.env.MEDIA_PATH;

const requestHandler = (req,res)=> {
    console.log(req.url);
    fs.readdir(path+"/*.mp4",(err,items)=>{
        var msg = {
            'kind': 'ItemList',
            'apiVersion': 'v1',
            'items': []
        };
        if (!items) {
            return msg;
        }

        for (let i = 0; i < items.length; i++) {
            msg.items.push(items[i]);
        }
        res.end(JSON.stringify(msg));
    })
}

var server = http.createServer(requestHandler);
server.listen(port,err=>{
    if (err) {
        console.log("Error starting server",err);
    }
    console.log(`Server is active on port ${port}`);
})