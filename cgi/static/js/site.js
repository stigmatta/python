class Base64 {
    static #textEncoder = new TextEncoder();
    static #textDecoder = new TextDecoder();

    // https://datatracker.ietf.org/doc/html/rfc4648
    static encode = (str) =>
        btoa(String.fromCharCode(...Base64.#textEncoder.encode(str)));

    static decode = (str) =>
        Base64.#textDecoder.decode(
            Uint8Array.from(atob(str), c => c.charCodeAt(0))
        );

    static encodeUrl = (str) =>
        this.encode(str)
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=/g, '');

    static decodeUrl = (str) =>
        this.decode(str.replace(/-/g, '+').replace(/_/g, '/'));

    static jwtEncodeBody = (header, payload) =>
        this.encodeUrl(JSON.stringify(header)) + '.' +
        this.encodeUrl(JSON.stringify(payload));

    static jwtDecodePayload = (jwt) =>
        JSON.parse(this.decodeUrl(jwt.split('.')[1]));

    static jwtDecodeHeader = (jwt) =>
        JSON.parse(this.decodeUrl(jwt.split('.')[0]));
}

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

    document.querySelector('[data-id="api-discount-get-btn"]').addEventListener("click", apiPassBtnClicked);
    for(let btn of document.querySelectorAll("[data-token]")) {
        btn.addEventListener("click", selfTestBtnClicked);
    }


    const allBtn = document.getElementById("run-all-tests")
    if(allBtn) {
        allBtn.addEventListener("click", runAllTestsClicked);
    }

}

function runAllTestsClicked() {
    for(let btn of document.querySelectorAll("[data-token]")) {
        btn.click()
    }
}


function selfTestBtnClicked(e) {
    const successCode = 200;
    const btn = e.target.closest("[data-token]");
    if (!btn) return;

    const tr = btn.closest("tr");
    if (!tr) return;

    const res = tr.querySelector("[data-result]");
    const dtl = tr.querySelector("[data-details]");

    fetch("/discount", {
        method: "GET",
        headers: {
            "Authorization": btn.dataset.token
        }
    })
    .then(r => {
        const cls = r.status == successCode ? "test-ok" : "test-fail";
        dtl.innerHTML = `<span class="${cls}" title="expected code: ${successCode}">HTTP status: <b>${r.status}</b></span><br/>`;
        return r.json();
    })
    .then(j => {
        let expected = dtl.getAttribute("data-isok");
        let code = dtl.getAttribute("data-code");
        let data = dtl.getAttribute("data-data");

        let cls = j.status.isOk.toString() == expected ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class="${cls}" title="expected isOk: ${expected}">REST isOk: <b>${j.status.isOk}</b></span><br/>`;

        cls = j.status.code.toString() == code ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class="${cls}" title="expected code: ${expected}">REST status: <b>${j.status.code}</b></span><br/>`;

        cls = j.status.message == j.status.message ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class = "${cls}" title="expected message: ${j.status.message}">REST message: <b>${j.status.message}</b></span><br/>`;

        cls = String(j.data) == data ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class="${cls}" title="expected data: ${data}">
            REST data: <b>${j.data}</b>
        </span><br/>`;

            const hasFail = dtl.querySelector(".test-fail");
            res.textContent = hasFail ? "FAILED" : "SUCCESS";
            res.className = hasFail ? "test-fail" : "test-ok";

    })
    .catch(err => {
        dtl.textContent = err.message;
    });
}




function apiPassBtnClicked(e) {
    const [prefix, apiName, apiMethod, _] = e.target.getAttribute("data-id").split('-');
    const resId = `${prefix}-${apiName}-${apiMethod}-result`;
    const td = document.querySelector(`[data-id="${resId}"]`);
    const path = e.target.getAttribute("data-path");

    const tokenElem = document.getElementById("token");
    const token = tokenElem ? tokenElem.innerText : null;
    if(td) {
        fetch(`/${apiName}${path}`, {
            method: apiMethod.toUpperCase(),
            headers: {
                "Access-Control-Allow-Origin": "cgi221.loc",
                "Custom-Header": "My Value",
                "Authorization": token == null || token.length == 0 
                    ? "Basic YWRtaW46YWRtaW4=" 
                    : `Bearer ${token}` // "admin" and password admin
            }
            
        }).then(r => {
            if (r.ok) {
                r.json().then(j => {
                    td.innerHTML = `<pre>${JSON.stringify(j, null, 4)}</pre>`;
                    if(j.meta.data_type == "token") {
                        document.getElementById("token").innerText = j.data;
                        const payloadBase64 = j.data.split('.')[1];
                        const payloadJson = JSON.parse(Base64.decodeUrl(payloadBase64));

                        document.getElementById("token-payload").innerHTML =
                            `<pre>${JSON.stringify(payloadJson, null, 4)}</pre>`;
                    }

                    const headerJson = Base64.jwtDecodeHeader(j.data);
                    document.getElementById("token-header").innerHTML =
                        `<pre>${JSON.stringify(headerJson, null, 4)}</pre>`;

                });
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

function apiTestBtnClicked(e) {
    const [prefix, apiName, apiMethod, _] = e.target.id.split('-');
    const resId = `${prefix}-${apiName}-${apiMethod}-result`;
    const td = document.getElementById(resId);
    const tokenElem = document.getElementById("token");
    const token = tokenElem ? tokenElem.innerText : null;
    if(td) {
        fetch(`/${apiName}`, {
            method: apiMethod.toUpperCase(),
            headers: {
                "Access-Control-Allow-Origin": "cgi221.loc",
                "Custom-Header": "My Value",
                "Authorization": token == null || token.length == 0 
                    ? "Basic YWRtaW46YWRtaW4=" 
                    : `Bearer ${token}` // "admin" and password admin
            }
            
        }).then(r => {
            if (r.ok) {
                r.json().then(j => {
                    td.innerHTML = `<pre>${JSON.stringify(j, null, 4)}</pre>`;
                    if(j.meta.data_type == "token") {
                        document.getElementById("token").innerText = j.data;
                        const payloadBase64 = j.data.split('.')[1];
                        const payloadJson = JSON.parse(Base64.decodeUrl(payloadBase64));

                        document.getElementById("token-payload").innerHTML =
                            `<pre>${JSON.stringify(payloadJson, null, 4)}</pre>`;
                    }

                    const headerJson = Base64.jwtDecodeHeader(j.data);
                    document.getElementById("token-header").innerHTML =
                        `<pre>${JSON.stringify(headerJson, null, 4)}</pre>`;

                });
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