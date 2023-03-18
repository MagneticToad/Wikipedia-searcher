const fs = require('fs');

function encode(string) {
    let encoded = encodeURIComponent(string);
    encoded = encoded.replace(/\!/g, "%21");
    encoded = encoded.replace(/\*/g, "%2A");
    encoded = encoded.replace(/\(/g, "%28");
    encoded = encoded.replace(/\)/g, "%29");
    encoded = encoded.replace(/\'/g, "%27");
    return encoded;
}

console.log("Loading titles into memory");
var titles = fs.readFileSync('./raw_titles.txt', 'utf8').split("\n");
console.log("Loaded");

//fs.writeFileSync("titles_and_views.txt", ""); //clear the file

async function proccessItems(startNumber, endNumber) {
    const batchSize = 100;
    const minDelay = 1100;
  
    let delay = 0;
    let fails;
    let hasFailed;
    for (let i = startNumber; i <= endNumber; i += batchSize) {
        fails = 0;
        
        do {
            console.log(`Starting batch with first article ${titles[i]} (number ${i})`);
            var batchStart = i;
            var batchEnd = Math.min(batchStart + batchSize - 1, endNumber);

            const requests = [];
            for (let j = batchStart; j <= batchEnd; j++) {
                requests.push(fetch(`https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/${encode(titles[j])}/monthly/19000101/20230301`, {
                    method: "GET"
                }));
            }

            var start = Date.now();
            const responses = await Promise.all(requests);
            var data = await Promise.all(responses.map(response => response.json()));

            hasFailed = false;
            data.forEach((item, index) => {
                if (item.items === undefined) {
                    console.log(titles[index + batchStart]);
                    console.log(item);
                    if (item.type === "https://mediawiki.org/wiki/HyperSwitch/errors/request_rate_exceeded") {
                        hasFailed = true;
                    }
                }
            });

            if (hasFailed) {
                console.log("Request rate exceeded");
                fails++;
                console.log(`Failure number ${fails}; waiting ${2**fails} seconds`);
                await new Promise(resolve => setTimeout(resolve, (2**fails)*1000 )); //wait 2^fails seconds before retrying e.g. 2 seconds first, then 4 if failed again, then 8 etc.
            }
        } while (hasFailed);
        

        let processedData = data.map((item, index) => {
            return {
                name: item.items ? item.items[0].article : titles[index + batchStart],
                count: item.items ? item.items.reduce((accumulator, currentValue) => accumulator + currentValue.views, 0) : -1
            }
        });
        let textToWrite = processedData.reduce((accumulator, currentValue) => accumulator + `${currentValue.name}|${currentValue.count}\n`, "");

        await new Promise(resolve => fs.appendFile("titles_and_views.txt", textToWrite, resolve));

        const end = Date.now();
        const elapsed = end - start;

        delay = Math.max(minDelay - elapsed, 0);
        console.log(`Finished batch with last article ${titles[batchEnd]} after ${elapsed}ms`);
        console.log(`Waiting ${delay}ms to continue`);
        await new Promise(resolve => setTimeout(resolve, delay));
        
    }
}

proccessItems(1509600, 1699999);

//processed 949999 inclusive