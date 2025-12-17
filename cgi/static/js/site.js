document.addEventListener("DOMContentLoaded", initApiTests);


function initApiTests() {
    const apiNames = ["user", "order", "discount"];
    const apiMethods = ["get", "post"];
    for(let apiName of apiNames) {
        for(let apiMethod of apiMethods) {
            let btnId = `api-${apiName}-${apiMethod}-btn`;
            let btn = document.getElementById(btnId);
            if(btn) {
                btn.addEventListener("click", apiTestBtnClicked);
            }
        }
    }
}

function apiTestBtnClicked(e) {
    const [prefix, apiName, apiMethod, _] = e.target.id.split('-');
    const resId = `${prefix}-${apiName}-${apiMethod}-result`;
    const td = document.getElementById(resId);
    if(td) {
        fetch(`/${apiName}`, {
            method: apiMethod.toUpperCase(),
            headers: {
                "Access-Control-Allow-Origin": "cgi221.loc",
                "Custom-Header": "My Value",
                "Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==" // "Aladdin" and password open sesame"
            }
            
        }).then(r => {
            if (r.ok){
                r.json().then(j => td.innerHTML = `<pre>${JSON.stringify(j, null, 4)}</pre>`);
            }
            else{
                r.text().then(t => td.innerText = t);
            }
        })
    }
    else {
        throw "Container not found: " + resId;
    }
}