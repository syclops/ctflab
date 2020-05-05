<?php
  include "config.php";
  $con = new SQLite3($database_file);

  $id = $_POST["idnum"];
  $query = "SELECT id, name FROM users WHERE id='$id'";
  $result = $con->query($query);

  echo "<h1>Directory search results</h1>";

  echo "<style>
    table, th, td {
      border: 1px solid black;
    }
    th, td {
      padding: 15px;
    }
  </style>
  ";

  echo "<table>";
  echo "<tr>";
  echo "<th><b>ID number</b></th>";
  echo "<th><b>Username</b></th>";
  echo "</tr>";
  while ($row = $result->fetchArray()) {
    echo "<tr>";
    echo "<th>" . $row[0] . "</th>";
    echo "<th>" . $row[1] . "</th>";
    echo "</tr>";
  }
  echo "</table>";

?>
