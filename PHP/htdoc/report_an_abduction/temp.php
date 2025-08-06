<html>
<head>
    <title>Aliens Abducted Me - Report an Abductuion</title>
</head>
<body>
    <h2>Aliens Abducted Me - Report an Abduction</h2>


<?php
    $when_it_happened = $_POST['whenithappened'];
    $how_long = $_POST['howlong'];
    $alien_description = $_POST['aliendescription'];
    $fang_spotted = $_POST['fangspotted'];
    $email = $_POST['email'];


    echo 'THanks for submitting the form.<br />';
    echo 'You were abducted ' . $when_it_happened;
    echo ' and were gone for ' . $how_long . '<br />';
    echo 'Describe them: ' . $alien_description . '<br />';
    echo 'Was Fang there? ' . $fang_spotted . '<br />';
    echo 'Your email adress is ' . $email;
?>


</body>
</html>