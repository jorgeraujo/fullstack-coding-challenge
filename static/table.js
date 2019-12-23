function loadTableData(translationData){
    let tableBody = document.getElementById('translationTableData');
    let dataHtml = '';
    jsonResponse = JSON.parse(translationData)
    for(let translation of jsonResponse.translations){
        dataHtml += `<tr><td>${translation.uid}</td><td>${translation.state}</td><td>${translation.text_to_translate}</td><td>${translation.translation}</td></tr>`
    }
    tableBody.innerHTML = dataHtml;
} 

function getAllTranslations(){
    let getTranslationsRequest = new XMLHttpRequest();
    getTranslationsRequest.onreadystatechange = function(){
        console.log(getTranslationsRequest.response);
        loadTableData(getTranslationsRequest.response);
    }
    getTranslationsRequest.open('GET', 'http://localhost:5000/translations/');
    getTranslationsRequest.send();
}

form = document.getElementById('translation-form')
input = document.getElementById("text_to_translate")

form.addEventListener("submit", function(evt) {
    evt.preventDefault();
    
    param = {text_to_translate:input.value}
    let getTranslationsRequest = new XMLHttpRequest();
    getTranslationsRequest.onreadystatechange = function(){
    }
    

    getTranslationsRequest.open('POST', 'http://localhost:5000/');
 
    getTranslationsRequest.send(JSON.stringify(param));
});

document.onload = getAllTranslations();