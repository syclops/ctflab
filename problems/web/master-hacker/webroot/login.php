<?php
  include "config.php";
  $con = new SQLite3($database_file);

  $username = $_POST["username"];
  $password = $_POST["password"];
  $debug = $_POST["debug"];
  $query = "SELECT * FROM users WHERE name='$username' AND password='$password'";
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
    echo "<h1>Access to mainframe authorized.</h1>";
    echo "<p>Welcome to Top Secret Inc. (version $FLAG)</p>";
  } else {
    echo "<h1>Access denied. Security personnel have been dispatched.</h1>";
  }
?>
