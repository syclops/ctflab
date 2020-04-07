<?php
  include "config.php";
  $con = new SQLite3($database_file);

  $id = $_POST["id"];
  $query = "SELECT id, name FROM users WHERE id='$id'";
  $result = $con->query($query);

  $row = $result->fetchArray();

  echo "<h1>Search results</h1>";
  echo "<pre>";
  foreach ($row as $item) {
    echo $item;
  }
  echo "</pre>";
?>
