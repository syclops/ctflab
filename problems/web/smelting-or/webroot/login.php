<?php
  include "config.php";
  $con = new SQLite3($database_file);

  $username = $_POST["username"];
  $password = $_POST["password"];
  $debug = $_POST["debug"];
  $processed_username = preg_replace('/or/i', '', $username);
  $processed_password = preg_replace('/or/i', '', $password);
  $query = "SELECT * FROM users WHERE name='$processed_username' AND password='$processed_password'";
  $result = $con->query($query);
  if (intval($debug)) {
    echo "<pre>";
    echo "username: ", htmlspecialchars($username), "\n";
    echo "password: ", htmlspecialchars($password), "\n";
    echo "SQL query: ", htmlspecialchars($query), "\n";
    echo "</pre>";
  }

  $row = $result->fetchArray();

  if ($row) {
    echo "<h1>Access authorized.</h1>";
    echo "<p>Welcome to TEM Refinery (version $FLAG)</p>";
  } else {
    echo "<h1>Access denied. Security personnel have been dispatched.</h1>";
  }
?>
