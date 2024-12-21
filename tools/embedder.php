<?php

declare(strict_types=1);

class Embedder
{
    private string $apiKey;
    private string $model;
    private string $url;

    public function __construct(string $provider = "deepinfra")
    {
        if ($provider === "deepinfra") {
            $this->apiKey = getenv('MDL_API_KEY'); // Assuming environment variables are used for keys
            $this->model = getenv('EMB_MDL'); // Replace with actual model
            $this->url = "https://api.deepinfra.com/v1/openai/embeddings";
        } else {
            throw new InvalidArgumentException("Invalid provider");
        }
    }

    public function encode(string $input): ?array
    {
        $headers = [
            "Content-Type: application/json",
            "Authorization: Bearer {$this->apiKey}"
        ];

        $data = json_encode([
            "model" => $this->model,
            "input" => $input,
            "encoding_format" => "float"
        ]);

        $response = $this->makePostRequest($this->url, $headers, $data);

        if ($response['status_code'] === 200) {
            return json_decode($response['body'], true);
        }

        return null;
    }

    private function makePostRequest(string $url, array $headers, string $data): array
    {
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
    $embedder = new Embedder();
    $result = $embedder->encode("Your input string here");
    var_dump($result);
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}
