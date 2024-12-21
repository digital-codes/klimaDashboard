<?php

declare(strict_types=1);

class VectorDb {
    private string $apiKey;
    private string $collection;
    private string $url;

    public function __construct(string $provider = "zilliz") {
        if ($provider === "zilliz") {
            // Replace with actual API key and configuration values
            $this->apiKey = getenv("VECTOR_API_KEY");
            $this->collection = "ksk";
            $this->url = "https://in03-eb450554ac4fcc5.serverless.gcp-us-west1.cloud.zilliz.com";
            echo $this->url . PHP_EOL;
        } else {
            throw new InvalidArgumentException("Invalid provider");
        }
    }

    public function describeCollection(?string $collection = null): ?array {
        if ($collection === null) {
            $collection = $this->collection;
        }

        $headers = [
            "Content-Type: application/json",
            "Authorization: Bearer {$this->apiKey}"
        ];

        $data = json_encode(["collectionName" => $collection]);
        $url = "$this->url/v2/vectordb/collections/describe";

        $response = $this->makePostRequest($url, $headers, $data);

        if ($response['status_code'] === 200) {
            return json_decode($response['body'], true);
        }

        echo "HTTP error: " . $response['status_code'] . PHP_EOL;
        return null;
    }

    private function makePostRequest(string $url, array $headers, string $data): array {
        $ch = curl_init($url);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

        $body = curl_exec($ch);
        $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        return ['status_code' => $statusCode, 'body' => $body];
    }
}

// Example usage
try {
    $vectorDb = new VectorDb();
    $collectionInfo = $vectorDb->describeCollection();

    if ($collectionInfo) {
        echo "Collection Info:" . PHP_EOL;
        print_r($collectionInfo);
    } else {
        echo "Failed to describe collection." . PHP_EOL;
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . PHP_EOL;
}

