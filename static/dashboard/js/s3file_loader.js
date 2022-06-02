function uploadFileToS3(element) {
    return new Promise(function (resolve) {
        var xhr = new XMLHttpRequest();
        var reader = new FileReader();

        //Event to submit form on uploaded
        xhr.onreadystatechange = function () {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                element.fileElement.parentElement.removeChild(element.fileElement);
                resolve();
            }
        }

        //Open connection
        var url = element.fileUrl;
        xhr.open('PUT', url);

        //Prepare & send file
        reader.onload = function (evt) {
            xhr.send(evt.target.result);
        };

        //Read file
        var file = element.fileElement.files[0];
        var fileName = element.fileName;
        var fileExtension = file.name.split('.').pop();
        element.fileNameElement.value = fileName + '.' + fileExtension;
        element.fileMimeTypeElement.value = file.type;
        reader.readAsArrayBuffer(file);
    })
}