
<?php
// Get the user-agent string
$userAgent = strtolower($_SERVER['HTTP_USER_AGENT']);

// Check if the user-agent contains "okhttp"
if (strpos($userAgent, 'okhttp') === false) {
    echo "<br><br><br><br><br>Invalid player detected. Please use FongMi TV or OKTV on Android mobile devices or Android TV.";
} else {
    header("Location: https://raw.githubusercontent.com/newrecha/TVBOX/main/0914-only-sex.json");
    exit;


}

?>