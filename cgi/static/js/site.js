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
    const errorTests = {
        "api-401-missing-header-btn": { 
            endpoint: "/user",
            method: "GET",
            headers: {}, 
            result: "api-missing-header-result"
        },
        "api-401-incorrect-scheme-btn": { 
            endpoint: "/user",
            method: "GET",
            headers: { "Authorization": "Bearer invalid_token" },
            result: "api-incorrect-scheme-result"
        },
        "api-401-short-credentials-btn": { 
            endpoint: "/user",
            method: "GET",
            headers: { "Authorization": "Basic QQ==" },
            result: "api-short-credentials-result"
        },
        "api-401-malformed-credentials-btn": { 
            endpoint: "/user",
            method: "GET",
            headers: { "Authorization": "Basic QWxhZG~~~RpbjpvcGVuIHNlc2FtZQ==" },
            result: "api-malformed-credentials-result"
        }
    };

    Object.entries(errorTests).forEach(([btnId, params]) => {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.onclick = () => runApiErrorTest(params.endpoint, params.method, params.headers, params.result);
        }
    });
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

function runApiErrorTest(endpoint, method, headers, resId) {
    const td = document.getElementById(resId);
    if (!td) {
        console.error("Container not found: " + resId);
        return;
    }

    td.innerHTML = "<i>Testing...</i>";

    fetch(endpoint, {
        method: method,
        headers: {
            "Access-Control-Allow-Origin": "cgi221.loc",
            ...headers 
        }
    })
    .then(r => r.json().catch(() => r.text()))
    .then(data => {
        if (typeof data === 'object') {
            td.innerHTML = `<pre style="color: #a00;">${JSON.stringify(data, null, 4)}</pre>`;
        } else {
            td.innerText = data;
        }
    })
    .catch(err => {
        td.innerHTML = `<b style="color:red">Network Error:</b> ${err.message}`;
    });
}