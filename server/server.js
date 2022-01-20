const express = require('express')
const bodyParser = require("body-parser");
const path = require('path')
const fs = require('fs');
const { hostname } = require('os');
const app = express()

const host = "localhost"
const port = 3000

app.get('/', function (req, res) {
    //Home
});

app.get('/account/:name/:homeroom/:studentId', function (req, res) {
    //Account
    fs.readFile('data/' + req.params.homeroom + "/" + req.params.name + "-" + req.params.homeroom + "-" + req.params.studentId + ".json", (err, data) => {
        if (err)
            throw err;

        const json = JSON.parse(data);
        const out = {
            "name": json.name,
            "homeroom":  json.homeroom,
            "studentId":  json.studentId,
            "balance": json.balance,
            "isComittee": json.isComittee,
            "jobs": json.jobs
        };
        console.log(out);
        res.json(out);
    });
});

app.post('/account/create/', function(req, res) {
    const body = req.body;
    const name = body.name;
    const homeroom = body.homeroom;
    const studentId = body.studentId;
    const balance = body.balance;
    const isComittee = body.isComittee;
    const jobs = body.jobs;

    fs.writeFile(JSON.stringify({
        "name": name,
        "homeroom": homeroom,
        "studentId": studentId,
        "balance": balance,
        "isComitee": isComittee,
        "jobs": jobs
    }));

    res.end(response);
});

app.listen(port, () => console.log('Listening on ' + host + ":" + port))