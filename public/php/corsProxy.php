<?php
declare(strict_types=1);

// Set the allowed origin and allowed methods

header("Access-Control-Allow-Headers: *");
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');


$specs_file = "./proxy.json";

// read specs 
$specs_content = file_get_contents($specs_file);
if ($specs_content === false) {
    http_response_code(400);
    exit('Error reading the specs file');
}

$specs = json_decode($specs_content, true); 
// Check if the JSON was decoded successfully
if ($specs === null) {
    http_response_code(400);
    exit('Error decoding the specs file');
} 

$keys_file = "./keys.json";

// read specs 
$keys_content = file_get_contents($keys_file);
if ($keys_content === false) {
    http_response_code(400);
    exit('Error reading the keys file');
}

$keys = json_decode($keys_content, true); 
// Check if the JSON was decoded successfully
if ($specs === null) {
    http_response_code(400);
    exit('Error decoding the keys file');
} 

function getItemParms($url) {
    global $specs;
    global $keys;
    if (array_key_exists($url,$specs)) {
        $u = $specs[$url];
        if (array_key_exists("key",$u)) {
            $u["url"] = $u["url"] . "&auth=" . $keys[$u["key"]];
        } 
        return $u;
    } else {
        http_response_code(400);
        exit('Wrong key');
    }
}

function requestFile ($topic) {
    $item = getItemParms(htmlspecialchars($topic));
    $url = $item["url"];
    $format = $item["format"];
    
    // Make sure the URL is valid
    if (filter_var($url, FILTER_VALIDATE_URL) === false) {
        http_response_code(400);
        exit('Invalid URL');
    }
    
    // Get the content type of the requested resource
    //$mime_type = mime_content_type($url);
    
    // Fetch the content from the URL using cURL
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $content = curl_exec($ch);
    curl_close($ch);
    // Output the content
    // header('Content-Type: text/plain');
    if ($format != "json") {
        $content = json_encode(array("data" => $content));
    }
    //print_r($content);
    return $content;
}


// Check the request method
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    // Handle pre-flight OPTIONS requests
    header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization');
    exit();
}

// Get the URL to proxy from the query string
$parms = $_GET['topic'];

if (isset($_GET['mode'])) {
    $mode = $_GET['mode'];
} else {
    $mode = "";
}

$tl = explode(",",$parms);
$topic = $tl[0];


function convertArray($inputArray) {
    // Get all keys from the input array
    $keys = ["unix_seconds","share"]; //array_keys($inputArray);

    // Get the length of the first array (assuming all arrays are the same length)
    $length = count($inputArray[$keys[0]]);

    $result = [];
    
    // Loop through each index of the arrays
    for ($i = 0; $i < $length; $i++) {
        $item = [];
        
        // For each key, assign the corresponding value from the array
        foreach ($keys as $key) {
            $item[$key] = $inputArray[$key][$i];
        }
        
        // Add the constructed item to the result array
        $result[] = $item;
    }
    
    return $result;
}


$results = array();

if ($mode == "single") {
    $content = requestFile($topic);
    // important to convert to array
    /*
    If you're working with JSON or an API response, you may have decoded the JSON object 
    using json_decode() without passing the second parameter (true), which would return 
    the data as an associative array. By default, json_decode() returns an object of type stdClass.
    */
    $results = convertArray(json_decode($content,true));
    
} else {
    foreach($tl as $t) {
        $content = requestFile($t);
        $results[$t] = json_decode($content);
    };
}


// save
$tmpfile = tempnam(".", "CORS");
// file_put_contents($tmpfile,$content);
file_put_contents($tmpfile,json_encode($results));
// detect type
$mime_type = mime_content_type($tmpfile);
// set header
header("Content-type: " . $mime_type);
echo file_get_contents($tmpfile);
// remove file
unlink($tmpfile);

?>



