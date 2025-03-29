const express = require("express");
const mysql = require("mysql");
const bcrypt = require("bcryptjs");
const cors = require("cors");
const bodyParser = require("body-parser");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "yourpassword",
  database: "users_db",
});

db.connect((err) => {
  if (err) {
    console.error("Database connection failed: " + err.stack);
    return;
  }
  console.log("Connected to MySQL");
});

// Signup API
app.post("/signup", async (req, res) => {
  const { fullName, email, username, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);

  db.query(
    "INSERT INTO users (fullName, email, username, password) VALUES (?, ?, ?, ?)",
    [fullName, email, username, hashedPassword],
    (err, result) => {
      if (err) return res.status(500).json({ error: err });
      res.json({ message: "User registered successfully!" });
    }
  );
});

// Login API
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  db.query(
    "SELECT * FROM users WHERE username = ?",
    [username],
    async (err, results) => {
      if (err) return res.status(500).json({ error: err });
      if (results.length === 0) return res.status(401).json({ error: "User not found" });

      const validPassword = await bcrypt.compare(password, results[0].password);
      if (!validPassword) return res.status(401).json({ error: "Invalid password" });

      res.json({ message: "Login successful!" });
    }
  );
});

app.listen(3000, () => console.log("Server running on port 3000"));
