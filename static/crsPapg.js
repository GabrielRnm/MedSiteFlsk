/*if (isFile == 'False') {
    const vBox = document.querySelector('iframe');

    // const bLink = new Blob(([vBox.src]), { type: 'video/mp4' });
    const bLink = new MediaSource();

    const xhr = new XMLHttpRequest();
    xhr.open("get", vBox.src);
    xhr.responseType = "arraybuffer";
    xhr.onload = () => {
        cb(xhr.response);
    };

    const bUrl = URL.createObjectURL(xhr.send());

    console.log(bUrl);
    console.log(vBox.src);

    vBox.src = bUrl;
}*/