const ROOT = '/api/';


function get(url) {
    return fetch(ROOT + url).then(response => response.json())
}

export {get};