// server.js
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const path = require("path");

const app = express();

// ---------- MIDDLEWARE ----------
app.use(cors()); // allow frontend requests
app.use(express.json()); // parse JSON bodies

// ---------- MONGODB CONNECTION ----------
mongoose.connect("mongodb://127.0.0.1:27017/solarDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("MongoDB connected (local)"))
.catch(err => console.log("MongoDB connection error:", err));

// ---------- USER SCHEMA ----------
const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  password: String,
});

const User = mongoose.model("User", userSchema);

// ---------- ROUTES ----------

// Serve index.html
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// Serve solar.html
app.get("/solar", (req, res) => {
  res.sendFile(path.join(__dirname, "solar.html"));
});

// Signup API
app.post("/api/signup", async (req, res) => {
  const { fullName, email, password } = req.body; // match frontend keys

  if (!fullName || !email || !password)
    return res.status(400).json({ success: false, message: "All fields required" });

  try {
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ success: false, message: "User already exists" });
    }

    const newUser = new User({ name: fullName, email, password });
    await newUser.save();
    res.status(200).json({ success: true, message: "Signup successful" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: "Server error" });
  }
});

// Login API
app.post("/api/login", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password)
    return res.status(400).json({ success: false, message: "All fields required" });

  try {
    const user = await User.findOne({ email, password });
    if (!user) return res.status(400).json({ success: false, message: "Invalid credentials" });

    // Send success with redirect info
    res.status(200).json({ success: true, message: "Login successful", redirect: "/solar" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: "Server error" });
  }
});

// ---------- START SERVER ----------
const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
