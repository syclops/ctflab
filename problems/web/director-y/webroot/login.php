<?php
  //error_reporting(E_ALL);
  //ini_set('display_errors', '1');
  include "config.php";
  $con = new SQLite3($database_file);

  $username = $_POST["username"];
  $password = $_POST["password"];
  $stmt = $con->prepare("SELECT * FROM users WHERE name=:username AND password=:password");
  $stmt->bindValue(':username', $username, SQLITE3_TEXT);
  $stmt->bindValue(':password', $password, SQLITE3_TEXT);
  $result = $stmt->execute();

  $row = $result->fetchArray();

  if ($row) {
    echo "<h1>Access authorized.</h1>";
    if (strcmp($username, $directorname) == 0) {
      echo "<p>You have 1 new message. Subject: $FLAG</p>";
    } else {
      echo "<p>You have no new messages.</p>";
    }
  } else {
    echo "<h1>Access denied. Security personnel have been dispatched.</h1>";
  }
?>
