function loadTableData(translationData){
    let tableBody = document.getElementById('translationTableData');
    let dataHtml = '';
    jsonResponse = JSON.parse(translationData)
    for(let translation of jsonResponse.translations){
        dataHtml += `<tr><td>${translation.uid}</td><td>${translation.state}</td><td>${translation.text_to_translate}</td><td>${translation.translation}</td></tr>`
    }
    tableBody.innerHTML = dataHtml;
}

function updateTranslationOnTable(uid,translation){
    let UID = 0;
    let STATE = 1;
    let TEXT = 2;
    let TRANSLATED_TEXT = 3;
    let table = document.getElementById('translationTable');
    let tableBody = document.getElementById('translationTableData');

    for(let i=0, row; row=tableBody.rows[i];i++){
        console.log('got here');
        console.log(row.cells[UID].textContent);
        console.log(uid);
        if(row.cells[UID].textContent===uid){
            row.cells[TRANSLATED_TEXT].innerHTML = `<td>${translation}<td>`;
            row.cells[STATE].innerHTML = `<td>translated<td>`;
        }
    }
}

function insertTranslation(text){
    let tableBody = document.getElementById('translationTableData');
    let newRow = tableBody.insertRow();
    const rowGenerateId = ID();
    newRow.id = rowGenerateId;
    let newCell = newRow.insertCell(0);
    let uid_text = document.createTextNode('None');
    newCell.appendChild(uid_text);
    newCell = newRow.insertCell(1);
    let state = document.createTextNode('requested');
    newCell.appendChild(state);
    newCell = newRow.insertCell(2);
    let textString = document.createTextNode(text);
    newCell.appendChild(textString);
    newCell = newRow.insertCell(3);
    let text_translated = document.createTextNode('...');
    newCell.appendChild(text_translated);
    return rowGenerateId;
}

function getAllTranslations(){
    let getTranslationsRequest = new XMLHttpRequest();
    getTranslationsRequest.onreadystatechange = function(){
        if(getTranslationsRequest.readyState === XMLHttpRequest.DONE && getTranslationsRequest.status === 200) {
        console.log(getTranslationsRequest.response);
        loadTableData(getTranslationsRequest.response);
        }
    }
    getTranslationsRequest.open('GET', 'http://localhost:5000/translations/');
    getTranslationsRequest.responseType = 'text';
    getTranslationsRequest.send();
}

form = document.getElementById('translation-form')
input = document.getElementById("text_to_translate")

form.addEventListener("submit", function(evt) {
    evt.preventDefault();
    param = {text_to_translate:input.value}
    const newRowId = insertTranslation(input.value);
  
    let getTranslationsRequest = new XMLHttpRequest();
    getTranslationsRequest.onreadystatechange = function(){ 
        if(getTranslationsRequest.readyState === XMLHttpRequest.DONE && getTranslationsRequest.status === 200) {

        const row = document.getElementById(newRowId);
        console.log(row);
        response = JSON.parse(getTranslationsRequest.response);
        console.log(response)
        row.cells[0].innerHTML = `<td>${response['uid']}<td>`
        row.cells[1].innerHTML = `<td>pending<td>`
    }
    
    }
    getTranslationsRequest.open('POST', 'http://localhost:5000/');
    getTranslationsRequest.responseType = 'text';
    getTranslationsRequest.send(JSON.stringify(param));
});

var socket;
document.addEventListener("DOMContentLoaded", function() {
    socket = io.connect('http://localhost:5000');
    console.log('Your socket is ready!');

socket.on('after connect', function(msg){
    console.log('After connect', msg);
 });

 socket.on('translation completed', function(msg){
    console.log('translation completed', msg);
    updateTranslationOnTable(msg.uid, msg.translation);
 });
});

var ID = function () {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substr(2, 9);
  };

document.onload = getAllTranslations();