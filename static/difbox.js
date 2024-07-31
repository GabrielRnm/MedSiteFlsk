//Diferenciais e Depoimentos

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

if (depoiBX.children.length > 3) {
    //console.log('im big');
    //console.log(depoiBX.children)
    for (child in depoiBX.children) {
        if (child < depoiBX.children.length && child > 2 && depoiBX.children[child] != HTMLButtonElement) {
            //console.log(depoiBX.children[child]);
            depoiBX.children[child].style.display = 'none';
        }
    }
    depoiBX.parentElement.parentElement.append(buttonS);
    depoiBX.parentElement.parentElement.append(buttonP);
}

function showNxt(e) {
    for (child in depoiBX.children) {
        //console.log(child + ' : ' + depoiBX.children[child]);
        if (child < depoiBX.children.length + 1 && child > 2 && depoiBX.children[child] != HTMLButtonElement) {
            //console.log(child);
            //console.log(depoiBX.children[child]);
            if (depoiBX.children[child].style.display == 'none') {
                //console.log(depoiBX.children[child - 3]);
                depoiBX.children[child - 3].style.display = 'none';
                depoiBX.children[child].style.display = '';
                return
            }
            else {
                buttonS.style.display = 'none';
                buttonP.style.display = '';
            }
        }
    }
}

function showPrv(e) {
    let count = 0
    for (child in depoiBX.children) {
        if (child < depoiBX.children.length + 1) {
            //console.log('count child: ' + child);
            if (depoiBX.children[child].style.display == 'none') {
                count += 1;
                //console.log(count);
            }
        }
        if (count > 0 && child < depoiBX.children.length + 1 && child == count + 2) {
            //console.log('aftercount:' + child);
            if (depoiBX.children[child].style.display == '') {
                //console.log(depoiBX.children[child - 3]);
                depoiBX.children[child - 3].style.display = '';
                depoiBX.children[child].style.display = 'none';
                //console.log('the invisible child: ' + child)
                
            }
        }
        if (depoiBX.children[0].style.display == '')  {
            buttonS.style.display = '';
            buttonP.style.display = 'none';
        }
    }

}