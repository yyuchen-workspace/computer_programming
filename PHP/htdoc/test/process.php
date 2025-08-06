<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 取得表單資料
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);

    echo "<h2>Form Submitted</h2>";
    echo "<p><strong>Name:</strong> " . $name . "</p>";
    echo "<p><strong>Email:</strong> " . $email . "</p>";
} else {
    echo "<p>No data submitted yet.</p>";
}
?>
