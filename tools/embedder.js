class Embedder {
    constructor(provider = "deepinfra") {
        if (provider === "deepinfra") {
            // Replace with actual API key and model
            this.apiKey = "lNZ2DVyMAUDvdxRNSTuFLL9xmII9IrmR";
            this.model = "sentence-transformers/all-MiniLM-L12-v2";
            this.url = "https://api.deepinfra.com/v1/openai/embeddings";
        } else {
            throw new Error("Invalid provider");
        }
    }

    async encode(input) {
        const headers = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.apiKey}`,
        };

        const data = {
            model: this.model,
            input: input,
            encoding_format: "float",
        };

        try {
            const response = await fetch(this.url, {
                method: "POST",
                headers: headers,
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                console.error("HTTP error", response.status, response.statusText);
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error("Request failed", error);
            return null;
        }
    }
}

// Example usage:
(async () => {
    try {
        const embedder = new Embedder();
        const input = "Your input string here";
        const result = await embedder.encode(input);

        if (result) {
            console.log("Embedding result:", result);
        } else {
            console.log("Failed to fetch embeddings.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
})();

