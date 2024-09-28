<?php
declare(strict_types=1);

// Set the allowed origin and allowed methods

header("Access-Control-Allow-Headers: *");
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');

//$basedir = '/home/kugel/temp/js/klimaDashboard/public';
$basedir = '../';
$requestPayload = json_decode(file_get_contents('php://input'), true);

if (isset($requestPayload['topic']) && isset($requestPayload['lang'])) {
    $topic = htmlspecialchars($requestPayload['topic']);
    $lang = htmlspecialchars($requestPayload['lang']);
    $filePath = "$basedir/details/$lang/$topic.html";

    if (file_exists($filePath)) {
        header('Content-Type: text/html');
        echo file_get_contents($filePath);
        exit();
    } else {
        http_response_code(404);
        exit('File not found');
    }
} else {
    http_response_code(400);
    exit('Missing parameters');
}


?>



