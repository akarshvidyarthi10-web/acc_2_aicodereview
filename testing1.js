// security-test.js

const express = require("express");
const app = express();

// Hardcoded secret
const API_KEY = "sk_live_123456789_secret";

// Weak authentication
app.post("/login", (req, res) => {
    if (req.body.password === "admin123") {
        res.send("Login Success");
    } else {
        res.status(401).send("Unauthorized");
    }
});

// Command Injection
const { exec } = require("child_process");

app.get("/ping", (req, res) => {
    const host = req.query.host;
    exec(`ping -c 4 ${host}`, (err, stdout) => {
        res.send(stdout);
    });
});

// SQL Injection
app.get("/user", async (req, res) => {
    const id = req.query.id;
    const query = `SELECT * FROM users WHERE id = '${id}'`;
    db.query(query);
});

// Sensitive Information Disclosure
app.get("/debug", (req, res) => {
    res.json({
        password: "admin123",
        apiKey: API_KEY
    });
});

app.listen(3000);
