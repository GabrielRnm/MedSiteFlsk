//Diferenciais e Depoimentos



let depnum = 0;
let prev = 0

window.onload = function() {
    console.log(depoiBX.scrollWidth);
    if (depoiBX.scrollWidth < 600) {
        depnum = 0;
    }
    else {
        depnum = 0
    }
    reRen()
}


window.onresize = function() {
    document.title = (window.innerWidth + "/" + window.innerHeight);

    console.log(depoiBX.scrollWidth);
    if (depoiBX.scrollWidth < 600) {
        depnum = 0;
    }
    else {
        depnum = 2
    }
    reRen()
}

let depoiBX = document.querySelector('.depBoxWr');

let buttonS = document.createElement('button');
buttonS.style.position = 'absolute';
buttonS.style.marginLeft = '90%'
buttonS.style.backgroundColor = '#FD288D';
buttonS.style.border = '#FD288D solid 1px';
buttonS.style.borderRadius = '50%';
buttonS.classList.add('btn', 'btn-primary');
buttonS.innerHTML = '>';
buttonS.addEventListener('click', showNxt);

let buttonP = document.createElement('button');
buttonP.style.display = 'none'
buttonP.style.position = 'absolute';
buttonP.style.marginRight = '90%'
buttonP.style.backgroundColor = '#FD288D';
buttonP.style.border = '#FD288D solid 1px';
buttonP.style.borderRadius = '50%';
buttonP.classList.add('btn', 'btn-primary');
buttonP.innerHTML = '<';
buttonP.addEventListener('click', showPrv);

//console.log(depoiBX.children.length);

if (depoiBX.scrollWidth < 600) {
    depnum = 0 
}

if (depoiBX.children.length > 3) {
    //console.log('im big');
    //console.log(depoiBX.children)
    reRen();
    prev = -1
}

function reRen() {
    for (child in depoiBX.children) {
        //console.log(depoiBX.children[child]);
        //console.log(window.getComputedStyle(depoiBX.children[child]).display);
        if (child < depoiBX.children.length && child > depnum && depoiBX.children[child] != HTMLButtonElement) {
            //console.log(depoiBX.children[child]);
            depoiBX.children[child].style.display = 'none';
        }
        else if (child < depoiBX.children.length && depoiBX.children[child] != HTMLButtonElement) {
            depoiBX.children[child].style.display = '';
        }
    }
    depoiBX.append(buttonS);
    depoiBX.append(buttonP);
    buttonS.style.display = '';
}

function showNxt(e) {
    for (child in depoiBX.children) {
        console.log(child + ' : ' + depoiBX.children[child]);
        console.log('lenght : ' + depoiBX.children.length);
        if (child < depoiBX.children.length + 1 && child > depnum && depoiBX.children[child] != HTMLButtonElement) {
            if (depoiBX.children[child].style.display == 'none' && child > prev) {
                prev = child
                depoiBX.children[child].style.display = '';
                depoiBX.children[child - (depnum + 1)].style.display = 'none';
                if (child == parseInt(depoiBX.children.length - 3)){
                    buttonS.style.display = 'none';
                } else {
                    buttonP.style.display = '';
                }
                return ;
            }
        }
    }
}

function showPrv(e) {
    let count = 0
    prev = 0
    for (child in depoiBX.children) {
        if (child < depoiBX.children.length + 1 && depoiBX.children[child] != HTMLButtonElement) {
            if (depoiBX.children[child].style.display == 'none') {
                console.log('count: ' + count);
                count += 1;
            }
        }
        if (count > 0 && child < depoiBX.children.length + 1 && child == count + depnum) {
            if (depoiBX.children[child].style.display == '') {
                console.log('here');
                depoiBX.children[child - (depnum + 1)].style.display = '';
                depoiBX.children[child].style.display = 'none';
            }
        }
        if (window.getComputedStyle(depoiBX.children[0]).display == 'block')  {
            console.log('here 2');
            buttonS.style.display = '';
            buttonP.style.display = 'none';
        }
    }
}