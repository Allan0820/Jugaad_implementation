function download(){
    let zip=new JSZip()
    

    let file= document.getElementById('files')
    console.log(file.files)

    Array.from(file.files).forEach((f,i) => {
        mz.append(f.name,f, {password: "~~~"});
        // zip.file(f.name,f)
    })
    zip.generateAsync({type:'blob'})
    .then((content) =>{
        saveAs(content,"Filedownload.zip")
    })
}