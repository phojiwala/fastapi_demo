self.onmessage = function(e) {
    console.log('Worker received products:', e.data.length);
    const products = e.data;

    const chunkSize = 100;
    for (let i = 0; i < products.length; i += chunkSize) {
        const chunk = products.slice(i, i + chunkSize);
        console.log('Sending chunk:', i/chunkSize + 1);
        self.postMessage({
            products: chunk,
            isLastChunk: i + chunkSize >= products.length
        });
    }
};
