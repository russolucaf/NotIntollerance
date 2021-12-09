let map = L.map('map').setView([40.8359336, 14.2487826], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright%22%3EOpenStreetMap</a> contributors'
}).addTo(map);

let toto = L.marker([40.91958, 14.1530177]).addTo(map);
let popup = toto.bindPopup('<b> Pizzeria Toto Sapore</b><br />Via Santa Maria a cubito, 45, 80019, Qualiano.<br /> 081 195 22481');
let donna = L.marker([40.8902679, 14.2634456]).addTo(map);
popup = donna.bindPopup('<b> Pizzeria Donna Luisella</b><br />Corso Secondigliano, 151/E, 80144, Napoli.<br /> 081 038 0851');
let black = L.marker([40.9421776, 14.2667388]).addTo(map);
popup = black.bindPopup('<b> Paninoteca Black Burger</b><br />Corso Vittorio Emanuele III, 167, 80027, Frattamaggiore.<br /> 339 352 5163');
let veraci = L.marker([40.8405052, 14.2470714]).addTo(map);
popup = veraci.bindPopup('<b> Pizzeria Pizzaioli Veraci</b><br />Vico Tre Re a Toledo, 1, 80132, Napoli.<br /> 081 020 9641');