const { promisify } = require("util");
const { writeFile } = require("fs");
var mtg = require("mtgtop8");

const standardEvents = promisify(mtg.standardEvents);
const modernEvents = promisify(mtg.modernEvents);
const getEvent = promisify(mtg.eventInfo);
const getDeck = promisify(mtg.deck);

async function writeJson(obj, fileName) {
    const write = promisify(writeFile);
    console.log(`write json ${fileName}`);
    var jsonData = JSON.stringify(obj);
    try {
        await write(fileName, jsonData, 'utf8');
    } catch (e) {
        console.error(`couldn't write to ${fileName}`, e);
    }
}

async function main() {
    // var page = 4;
    var format = 'modern';

    try {
        for (let page = 1; page < 14; page++) {
            var events = await modernEvents(page);
            console.log(`get event page ${page}`);

            var promises = [];

            events.forEach(event => {
                promises.push(getEvent(event.id).then(info => {
                    console.log(`get event ${info.title}`)
                    info.decks.forEach(deck => {
                        getDeck(event.id, deck.id).then(deckData => writeJson(deckData, `decks/deck_${format}_${page}_${event.id}_${deck.id}.json`))
                        .catch(e => console.error(e));
                    });
                }).catch(e => console.error(e)));
            });

            await Promise.all(promises);
        }
        
    } catch (e) {
        console.error("Error: ", e)
    }
    
}

main();