class VectorDb {
    constructor(provider = "zilliz") {
        if (provider === "zilliz") {
            // Replace with your actual API key and configuration
            this.apiKey = "4ec4522142b9036f6751886f7448bb5c8447624ff261013347957624f8611486a75fb001b897156aea17aad7c30b731cd532e8db";
            this.collection = "ksk";
            this.url = `https://in03-eb450554ac4fcc5.serverless.gcp-us-west1.cloud.zilliz.com`;
            console.log(this.url);
        } else {
            throw new Error("Invalid provider");
        }
    }

    async describeCollection(collection = null) {
        const headers = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.apiKey}`,
        };

        if (!collection) {
            collection = this.collection;
        }

        const data = { collectionName: collection };
        const url = `${this.url}/v2/vectordb/collections/describe`;

        try {
            const response = await fetch(url, {
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
        const vectorDb = new VectorDb();
        const collectionInfo = await vectorDb.describeCollection();

        if (collectionInfo) {
            console.log("Collection Info:", collectionInfo);
        } else {
            console.log("Failed to describe collection.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
})();
