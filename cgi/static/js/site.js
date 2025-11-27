document.addEventListener("DOMContentLoaded", initApiTests);


function initApiTests() {
    const apiNames = ["user", "order"];
    const apiMethods = ["get", "post", "put", "patch", "delete"];
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
        td.innerText = resId;
    }
    else {
        throw "Container not found: " + resId;
    }
}