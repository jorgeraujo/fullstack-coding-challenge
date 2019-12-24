let tableData;


function loadTableData(translationData){
    let tableBody = document.getElementById('translationTableData');
    let dataHtml = '';
    for(let translation of translationData){
        dataHtml += `<tr><td>${translation.uid}</td><td>${translation.state}</td><td>${translation.text_to_translate}</td><td>${translation.translation}</td></tr>`
    }
    tableBody.innerHTML = dataHtml;
}


function getTranslationByUID(uid) {
    for(let translation of tableData){
        if(translation.uid === uid){
            return translation;
        }
    }
}

function updateTranslationOnTable(uid,translation){
    let translationToUpdate = getTranslationByUID(uid);
    translationToUpdate.translation = translation;
    translationToUpdate.state = 'completed';
    loadTableData(tableData);
}

function compare( a, b ) {
    if ( a.translation.length > b.translation.length ){
      return -1;
    }
    if ( a.translation.length < b.translation.length ){
      return 1;
    }
    return 0;
  }
  

function sortTable(tableData){
    tableData = tableData.sort(compare);
    loadTableData(tableData);
}


function insertTranslation(text){
    let tableBody = document.getElementById('translationTableData');
    let newRow = tableBody.insertRow();
    const rowGenerateId = ID();
    console.log(typeof(tableData))
    tableData.push(
        {
            rowId:rowGenerateId,
            uid: 'none',
            text_to_translate: text,
            translation: '',
            state: 'requested'
        }
    )
    loadTableData(tableData);
    return rowGenerateId;
}

function getAllTranslations(){
    let getTranslationsRequest = new XMLHttpRequest();
    getTranslationsRequest.onreadystatechange = function(){
        if(getTranslationsRequest.readyState === XMLHttpRequest.DONE && getTranslationsRequest.status === 200) {
        console.log(getTranslationsRequest.response);
        let parsedResponse = JSON.parse(getTranslationsRequest.response);
        tableData = parsedResponse.translations;
        loadTableData(tableData);
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
    console.log(tableData);
    let getTranslationsRequest = new XMLHttpRequest();
    getTranslationsRequest.onreadystatechange = function(){ 
        if(getTranslationsRequest.readyState === XMLHttpRequest.DONE && getTranslationsRequest.status === 200) {
            response = JSON.parse(getTranslationsRequest.response);
            const rowID = document.getElementById(newRowId);
            for(let translation of tableData){
                if(translation.rowId === newRowId){
                    translation.uid = response.uid;
                    translation.state = 'pending';
            }
        }
     loadTableData(tableData);
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
    sortTable(tableData);
 });
});

var ID = function () {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substr(2, 9);
  };

function sortColumn(columnName){
    const dataType = typeof(columnName);
    let sortDirection = !sortDirection;
}

document.onload = getAllTranslations();