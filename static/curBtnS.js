// mobile all button

let arrHM = ['Home', 'Cursos'];

let hbbtn = document.querySelector('.hbarbtn');
hbbtn.addEventListener('click', showHb);

let hbar = document.querySelector('.hbar');

let hOwrp = document.createElement('div');
hOwrp.classList.add('container');
hOwrp.classList.add('hOwrp');
hOwrp.style.position = 'absolute';
hOwrp.style.top = '2rem';
hOwrp.style.justifyContent = 'center';
hOwrp.style.width = '10rem';
hOwrp.style.zIndex = '2';
hOwrp.style.marginTop = '2.6rem';
hOwrp.style.backgroundColor = 'yellow';
hOwrp.style.display = 'none'

hbbtn.appendChild(hOwrp);

let hOrow = document.createElement('div');
hOrow.classList.add('row');
hOrow.style.backgroundColor = 'pink';

hOwrp.appendChild(hOrow)


for (child in arrHM) {
    if (arrHM[child] != 'Cursos') {
        
        let hOcol = document.createElement('a');
        hOcol.classList.add('col');
        hOcol.href = '/';
        hOcol.style.backgroundColor = 'gray';
        hOcol.style.fontSize = '0.7rem';
        hOcol.innerText = arrHM[child];

        hOrow.appendChild(hOcol);
    } else {
        
        let hOcol = document.createElement('div');
        hOcol.classList.add('col');
        hOcol.style.backgroundColor = 'gray';
        hOcol.style.fontSize = '0.7rem';
        hOcol.style.display = 'flex';
        hOcol.style.justifyContent = 'center';
        hOcol.innerText = arrHM[child];

        hOcol.addEventListener('click', hshowCourses);

        let hOptions = document.createElement('div');
        hOptions.style.position = 'absolute';
        hOptions.style.textAlign = 'center';
        hOptions.style.display = 'none';
        hOptions.style.width = '100%';
        hOptions.style.margin = '1rem 0';
        hOptions.style.flexDirection = 'column';
        hOptions.style.backgroundColor = 'rgb(255, 240, 255)';
        hOptions.style.color = 'rgba(38,59,78,255)';
        hOptions.style.fontWeight = 'bold';

        let hOpt1 = document.createElement('a');
        hOpt1.href = '/aPages/Enem';
        hOpt1.innerText = 'ENEM';
        hOpt1.style.fontSize = '0.7rem';
        hOpt1.style.color = 'inherit';
        hOpt1.style.margin = '5% 5%';
        hOpt1.style.borderBottom = 'gray solid 2pt';
        hOpt1.style.zIndex = '2';

        let hOpt2 = document.createElement('a');
        hOpt2.href = '/aPages/Particulares';
        hOpt2.innerText = 'Particular';
        hOpt2.style.fontSize = '0.7rem';
        hOpt2.style.color = 'inherit';
        hOpt2.style.margin = '5% 5%';
        hOpt2.style.borderBottom = 'gray solid 2pt';
        hOpt2.style.zIndex = '2';

        hOptions.appendChild(hOpt1);
        hOptions.appendChild(hOpt2);
        hOcol.appendChild(hOptions);

        function hshowCourses(e) {
            console.log('im here');
            if (hOptions.style.display != 'flex') { 
                //e.target.style.backgroundColor = 'rgb(255, 240, 255)';
                hOptions.style.display = 'flex';
            }
            else {
                //e.target.style.backgroundColor = 'rgb(255, 255, 255)';
                hOptions.style.display = 'none';
            }
        }

        hOrow.appendChild(hOcol);
    }
}

let hOwrpI = document.querySelector('.hOwrp');

function showHb(e) {
    console.log('hbtn');
    if (e.target.className == 'btn btn-primary hbarbtn') {
        if (hOwrpI.style.display == '') {
            hOwrpI.style.display = 'none';
        }
        else {
            hOwrpI.style.display = '';
        }
    }
}

// course button stuff

let cursButton = document.querySelector('.CrsBtn');
cursButton.addEventListener('click', showCourses);

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
opt1.style.zIndex = '2';

let opt2 = document.createElement('a');
opt2.href = '/aPages/Particulares';
opt2.innerText = 'Particular';
opt2.style.color = 'inherit';
opt2.style.margin = '5% 5%';
opt2.style.borderBottom = 'gray solid 2pt';
opt2.style.zIndex = '2';

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
