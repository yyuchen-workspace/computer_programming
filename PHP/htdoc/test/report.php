<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Aliens Abducted Me - Report an Abduction</title>
</head>
<body>
    <h2>Aliens Abducted Me - Report an Abduction</h2>

<?php
    // 確保表單的欄位都已提交
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $when_it_happened = isset($_POST['whenithappened']) ? $_POST['whenithappened'] : 'No date provided';
        $how_long = isset($_POST['howlong']) ? $_POST['howlong'] : 'No duration provided';
        $alien_description = isset($_POST['aliendescription']) ? $_POST['aliendescription'] : 'No description provided';
        $fang_spotted = isset($_POST['fangspotted']) ? $_POST['fangspotted'] : 'No answer';
        $email = isset($_POST['email']) ? $_POST['email'] : 'No email provided';

        // 顯示提交的資料
        echo 'Thanks for submitting the form.<br />';
        echo 'You were abducted ' . htmlspecialchars($when_it_happened) . ' and were gone for ' . htmlspecialchars($how_long) . '<br />';
        echo 'Describe them: ' . htmlspecialchars($alien_description) . '<br />';
        echo 'Was Fang there? ' . htmlspecialchars($fang_spotted) . '<br />';
        echo 'Your email address is ' . htmlspecialchars($email);
    } else {
        echo 'No form data received.';
    }
?>

</body>
</html>