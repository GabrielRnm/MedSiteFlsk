//Diferenciais e Depoimentos



let depnum = 0;
let prev = 0
let next = 0

window.onload = function() {
    if (depoiBX.scrollWidth < 600) {
        depnum = 0;
        prev = 0;
        next = 0;
    }
    else {
        depnum = 2
        prev = 0;
        next = 0;
    }
    reRen()
}

window.onresize = function() {
    if (depoiBX.scrollWidth < 600) {
        depnum = 0;
        prev = 0;
        next = 0;
    }
    else {
        depnum = 2;
        prev = 0;
        next = 0;
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
        //console.log(child);
        if (child > prev && child < depoiBX.children.length + 1 && !(depoiBX.children[child] instanceof HTMLButtonElement) && depoiBX.children[child].style.display == 'none' ) {
            prev = parseInt(child) - 1;
            next = parseInt(child) + 1;

            depoiBX.children[child].style.display = '';
            buttonP.style.display = '';
            
            if (depnum == 0) {
                depoiBX.children[prev].style.display = 'none';
            }
            else {
                depoiBX.children[prev - depnum].style.display = 'none';
            }
            if (next == depoiBX.children.length - 2) {
                buttonS.style.display = 'none';
            }
            return ;
        }
    }
}

function showPrv(e) {
    if (depnum == 2) {
        prev -= depnum;
        next -= depnum - 1;

        if (prev < 0)
            prev = 0

        let child = prev + 1;

        if (child <= next && child >= prev && child < depoiBX.children.length + 1 && !(depoiBX.children[child] instanceof HTMLButtonElement) && depoiBX.children[child].style.display == 'none' ) {
            depoiBX.children[prev].style.display = '';
            depoiBX.children[next].style.display = 'none';
            buttonS.style.display = '';

            if (prev == 0) {
                next = 0;
                buttonP.style.display = 'none';
            }
            return ;
        }
    }
    else if (depnum == 0) {
        prev -= depnum;
        next -= depnum;

        if (prev < 0)
            prev = 0;

        let child = prev + 1;

        if (child <= next && child >= prev && child < depoiBX.children.length + 1 && !(depoiBX.children[child] instanceof HTMLButtonElement)) {
            depoiBX.children[prev].style.display = '';
            buttonS.style.display = '';
                
            depoiBX.children[child].style.display = 'none';
            if (prev != 0) {
                prev -= 1
                next -= 1
                return
            }
            if (prev == 0) {
                next = 0;
                buttonP.style.display = 'none';
            }
            return ;
        }
    }


    
}