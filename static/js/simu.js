const fixedReg = /^Giá trị = "-?\d+(\.\d+)?"$/;
const normReg = /^μ = "-?\d+(\.\d+)?"; σ = "-?\d+(\.\d+)?"$/;
const poisReg = /^λ = "-?\d+(\.\d+)?"$/;
const gammaReg = /^α  = "-?\d+(\.\d+)?"; β = "-?\d+(\.\d+)?"$/;
const bernReg = /^ρ = "-?\d+(\.\d+)?"$/;
const binomReg = /^n = \"...\"; ρ = \"...\"$/;
const negBinomReg = /^r = \"...\"; ρ = \"...\"$/;



function changeErrorStyle(elementSelect){
    elementSelect.classList.add("did-error-input");
}

function checkConstraints_distribution(elementIndex) {
    console.log(`${elementIndex}_initial_form-15823`);
    const selectBox = document.getElementById(`${elementIndex}_selectBox-16823`);
    const inputBox = document.getElementById(`${elementIndex}_inputBox-16823`);

    const initialSelect = document.getElementById(`${elementIndex}_initial_form-15823`);
    const selectChoice = document.getElementById(`${elementIndex}_distri_select-15823`);
    const inputContent = document.getElementById(`${elementIndex}_value_inpt-15823`);

    const inputVal = inputContent.value;
    const selectVal = selectChoice.value;

    if (initialSelect.value === 'Giá trị cụ thể'){
        if (fixedReg.test(inputVal) === false){
            changeErrorStyle(inputBox);
            return false;
        }
    }else if(initialSelect.value === 'Ngẫu nhiên'){
        if(selectVal === ""){
            changeErrorStyle(selectBox);
            return false;
        }else{
            if (((selectVal === 'Normal' || selectVal === 'LogNormal') && normReg.test(inputVal) === false)
            || (selectVal === 'Poisson' && poisReg.test(inputVal) === false) 
            || (selectVal === 'Gamma' && gammaReg.test(inputVal) === false) 
            || (selectVal === 'Bernoulli' && gammaReg.test(inputVal) === false) 
            || (selectVal === 'Binomial' && binomReg.test(inputVal) === false) 
            || (selectVal === 'Negative Binomial' && negBinomReg.test(inputVal) === false)) {
                changeErrorStyle(inputBox);
                return false;
            }
        }
    }
    return true;
}

function checkIntegerBox(elementIndex){
    const inputBox = document.getElementById(`${elementIndex}_inputBox-16823`);
    const inputContent = document.getElementById(`${elementIndex}_value_inpt-15823`);
    
    const intReg = /^\d+$/;
    if(intReg.test(inputContent.value) === false){
        changeErrorStyle(inputBox);
        return false;
    }
    return true;
}

function checkAllConstrains(){
    for (let i = 1; i <= 4; i++) {
        if(checkConstraints_distribution(i) === false){
            return false;
        }
    }
    for (let i = 5; i <= 6; i++) {
        if(checkIntegerBox(i) === false){
            return false;
        }
    }
    return true;
}

function removeErrorStyle(){
    var elementsWithClass = document.querySelectorAll(".did-error-input");
  
    elementsWithClass.forEach(function(element) {
        element.classList.remove("did-error-input");
    });
}

function parseInputContent_toProperty(inputStr){
    console.log(inputStr);
    
    if(inputStr === ""){
        return {};
    }
    
    var sanitizedString = inputStr.replace(/"(-?\d+(\.\d+)?)"/g, '$1');

    var jsonObject = JSON.parse(
        '{' +
        sanitizedString
          .split('; ')
          .map(pair => `"${pair.replace(/ = /, '":')}`)
          .join(', ') +
        '}'
      );
    // console.log(jsonObject);
    return jsonObject;
}

function codeToInputName(code){
    switch(code){
        case 1:
            return "incu_period";
        case 2:
            return "infect_period";
        case 3:
            return "fatal_rate";
        case 4:
            return "vaccine_time";
        case 5: 
            return "n_day";
        case 6: 
            return "n_seed_case";
        default:
            return "invalid";
    }
}

function fetchData_idx(elementIndex) {
    const initialSelect = document.getElementById(`${elementIndex}_initial_form-15823`);
    const selectChoice = document.getElementById(`${elementIndex}_distri_select-15823`);
    const inputContent = document.getElementById(`${elementIndex}_value_inpt-15823`);

    var property = parseInputContent_toProperty(inputContent.value);
    var type;
    if(initialSelect.value === "Giá trị cụ thể"){
        type = "Fixed";
    }else if(initialSelect.value === "Ngẫu nhiên"){
        type = selectChoice.value;
    }else{
        type = "Fixed";
        property = {"Giá trị":1};
    }

    var jsonData = {
        "type": type,
        "properties": property,
    }
    return jsonData;
}

function fetchData(){
    var jsonData = {};

    for (let i = 1; i <= 4; i++) {
        const key = codeToInputName(i);
        const dictionary = fetchData_idx(i);
        jsonData[key] = dictionary;
    }

    for (let i = 5; i <= 6; i++) {
        jsonData[codeToInputName(i)] = {
            "type": "Fixed",
            "properties": {
                "Giá trị": parseInt(document.getElementById(`${i}_value_inpt-15823`).value)
            }
        };
    }
    console.log(jsonData);
    return jsonData;
}

function sendJsonData(data) {
    fetch('/simu_user_para', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

const submitSimul = document.querySelector('#see_simul_btn-15823');

// console.log(submitSimul);

submitSimul.addEventListener('click', function(){
    removeErrorStyle();

    if(checkAllConstrains()===true){
        const jsonData = fetchData();
        sendJsonData(jsonData); // Send the JSON data to the server
    }else{
        alert("Điều kiện trong các trường không thỏa, vui lòng kiểm tra lại:\n1. Chỉ cần thay thế dấu '...' trong trường 'Giá trị thực'.\n2. Trường số ngày nhiễm và số người tiền phát phải là số nguyên không âm.")
    }
    // console.log("clicked");
});





