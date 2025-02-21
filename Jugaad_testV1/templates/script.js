const zip = new JSZip();

zip.file("Hello.txt", "Hello World\n");
console.log("inside the script.js method")

zip.generateAsync({type:"blob"})
.then(function(content) {
    // see FileSaver.js
    saveAs(content, "example.zip");
});
