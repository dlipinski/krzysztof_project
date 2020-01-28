
let pythonDictString = 'flex_dict = {\n'
document.querySelectorAll('table')[2].querySelectorAll('tr').forEach(tr=>{
    let tds = tr.querySelectorAll('td');
    pythonDictString += `\t"${tds[1].querySelector('span').innerHTML.trim()}": "${tds[0].innerHTML.trim()}",\n`;
});
pythonDictString += "}";
console.log(pythonDictString);