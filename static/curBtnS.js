let cursButton = document.querySelector('.CrsBtn');
cursButton.addEventListener('click', showCourses);

let doc = document;

let cOptions = document.createElement('div');
cOptions.style.position = 'absolute';
cOptions.style.width = '75pt'
cOptions.style.textAlign = 'center';
cOptions.style.display = 'none';
cOptions.style.flexDirection = 'column';
cOptions.style.backgroundColor = 'rgb(255, 240, 255)';
cOptions.style.color = 'rgba(38,59,78,255)';
cOptions.style.fontWeight = 'bold';
//cOptions.innerText = '';

let opt1 = document.createElement('a');
opt1.href = '/aPages/Enem';
opt1.innerText = 'ENEM';
opt1.style.color = 'inherit';
opt1.style.margin = '5% 5%';
opt1.style.borderBottom = 'gray solid 2pt';

let opt2 = document.createElement('a');
opt2.href = '/aPages/Particulares';
opt2.innerText = 'Particular';
opt2.style.color = 'inherit';
opt2.style.margin = '5% 5%';
opt2.style.borderBottom = 'gray solid 2pt';

cursButton.appendChild(cOptions);
cOptions.appendChild(opt1);
cOptions.appendChild(opt2);

function showCourses(e) {
    if (cOptions.style.display != 'flex') { 
        cursButton.style.backgroundColor = 'rgb(255, 240, 255)';
        cOptions.style.display = 'flex';
    }
    else {
        cursButton.style.backgroundColor = 'rgb(255, 255, 255)';
        cOptions.style.display = 'none';
    }
}