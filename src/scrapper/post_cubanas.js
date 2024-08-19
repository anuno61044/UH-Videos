function post_fetch(url, name, image, year, link, id_audiences, id_clasification, id_countries, id_language) {

    const nuevoArticulo = {
        data: {
            name: name,
            url: link,
            photo: image,
            year: year,
            audiences: {
                id: id_audiences
            },
            clasification: {
                id: id_clasification
            },
            countries: {
                id: id_countries
            },
            languages: {
                id: id_language
            }
        }
    };

    fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
    },
    body: JSON.stringify(nuevoArticulo)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

}

const url = 'http://localhost:1337/api/videos';
const fs = require('fs');
const readline = require('readline');

const procesarURLs = (rutaArchivo, audencies, clasification, countries, language) => {

    let id_audiences = 0
    switch (audencies) {
        case 'adultos':
            id_audiences = 1;
            break;
        case 'infantiles':
            id_audiences = 2;
            break;
        case 'todos':
            id_audiences = 3;
            break;
        default:
            break;
    }
    
    let id_clasification = 0
    switch (clasification) {
        case 'pelicula':
            id_clasification = 1;
            break;
        case 'anime':
            id_clasification = 2;
            break;
        case 'serie':
            id_clasification = 3;
            break;
        case 'corto':
            id_clasification = 4;
            break;
        case 'novela':
            id_clasification = 5;
            break;
        case 'animados':
            id_clasification = 6;
            break;
        default:
            break;
    }
    
    let id_countries = 0
    switch (countries) {
        case 'cubana':
            id_countries = 1;
            break;
        case 'extranjera':
            id_countries = 2;
            break;
        default:
            break;
    }

    let id_language = 0
    switch (language) {
        case 'español':
            id_language = 1;
            break;
        case 'ingles':
            id_language = 2;
            break;
        case 'japones':
            id_language = 3;
            break;
        default:
            break;
    }


    const lector = readline.createInterface({
            input: fs.createReadStream(rutaArchivo),
            output: process.stdout,
            terminal: false
        });
        lector.on('line', (linea) => {
            // const line = 'https://visuales.uclv.cu/Infantiles/ADULTOS/Arcane./Arcane%201x7.mp4'
            
            let line = linea.split('-foto-')

            if (line[0] != 'https://visuales.uclv.cu//Peliculas/Cubanas/') {
                
                year = NaN
                let arr = line[0].split('/')
                let title = ''
                if(arr[arr.length-2].split('_').length > 1) {
                    year = arr[arr.length-2].split('_')[0]
                    let arr_name = arr[arr.length-2].split('_')[1].split('%20')
                    
                    for (let index = 0; index < arr_name.length; index++) {
                        if(index == 0) {
                            title = arr_name[index]
                            continue
                        }
                        title = title + " " + arr_name[index]
                    }
                }
                else {
                    let arr_name = arr[arr.length-2].split('%20')
                    for (let index = 0; index < arr_name.length; index++) {
                        if(index == 0) {
                            title = arr_name[index]
                            continue
                        }
                        title = title + " " + arr_name[index]
                    }
                }

                post_fetch(url, title, line[1], year, linea, id_audiences, id_clasification, id_countries, id_language)

            }

            
            // console.log(linea)
        });
    };



procesarURLs('./Cubanas.txt', 'adultos', 'pelicula', 'cubana', 'español');
// procesarURLs('./clasificados/anime, extrajera, todos, japones, (no año).txt', 'todos', 'anime', 'extranjera', 'japones');

// for (let i = 4000; i < 4800; i++) {
//     fetch(`http://localhost:1337/api/videos/${i}`, {
//         method: 'DELETE',
//             headers: {
//                 'Authorization': 'Bearer a4512af4a55b4679505540b0219f14832a7c4b5a683f398109ccfda6dff37f9c6a9eb693b677858feb324ef33c3e622f30dd9fc376f796482ca75ca3a43f0b1ce0e2de00a78c85216761e47161a513a3c3c8f36b89cac752e8862671a79353bc92c48f0db897b64961eefb1838e096d58dfc28c066b90d42681a9b7c718cb249'
//             }
//     })
//     .then(response => response.json())
//     .then(data => console.log(data))
//     .catch(error => console.error('Error:', error));
// }
