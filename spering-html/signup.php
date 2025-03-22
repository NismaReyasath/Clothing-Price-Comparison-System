<?php
$servername = "localhost";
$username = "root";  // Change if needed
$password = "";       // Change if needed
$dbname = "price_compare_db";

// Connect to the database
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get user input
$fullName = $_POST['fullName'];
$userName = $_POST['username'];
$email = $_POST['email'];
$password = $_POST['password'];
$confirmPassword = $_POST['confirmPassword'];

// Check if passwords match
if ($password !== $confirmPassword) {
    die("Error: Passwords do not match.");
}

// Check if username already exists
$stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
$stmt->bind_param("s", $userName);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    die("Error: Username taken. Please try another one.");
}

// Hash the password before storing
$hashedPassword = password_hash($password, PASSWORD_DEFAULT);

// Insert user into database
$stmt = $conn->prepare("INSERT INTO users (full_name, username, email, password_hash) VALUES (?, ?, ?, ?)");
$stmt->bind_param("ssss", $fullName, $userName, $email, $hashedPassword);

if ($stmt->execute()) {
    echo "Signup successful! Redirecting to login...";
    echo "<script>setTimeout(() => { window.location.href = 'login.html'; }, 2000);</script>";
} else {
    echo "Error: " . $stmt->error;
}

// Close connection
$stmt->close();
$conn->close();
?>
    