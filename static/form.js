person_warpper = document.querySelector('#persons-wrapper')
add_btn = document.querySelector('#add-person')
provinces_select = document.querySelector('#provinces')
districts_select = document.querySelector('#districts')
wardses_select = document.querySelector('#wardses')

const occupation_list = [
    'Doctor',
    'Teacher',
    'Labor',
    'Farmer',
    'Student'
]

occupation_list.forEach( job => {
    document.querySelector('#occupation_1').appendChild( customCreateElement('option', null,null, job, [{"name":"value", "value":job}]))
})

// async function getAddress1(url) {
//     let res = await fetch(url);
//     return res
// }

const url_provinces = "https://vn-public-apis.fpo.vn/provinces/getAll?limit=-1"

let provinces_to_code = []
let districts_to_code = []
let wardses_to_code = []


async function getAndSetAddress(url, selector, type) {
    let res = await fetch(url);
    data = []
    res = await res.json();
    data = res.data.data
    console.log(data)
    selector.innerHTML=''
    setAddress(data, selector)
    data = Object.assign({}, ...data.map((x) => ({[x.name]: x.code})))
    // if(type == 'Province')
    // {
    //     provinces_to_code = data
    // }
    // else if (type == 'District')
    // {
    //     districts_to_code = data
    // }
    // else wardses_to_code = data
    return data

}

function setAddress(data, selector)
{
    data.forEach(item => {
        const name = item.name
        option = customCreateElement('option', null, null,name,[{"name":"value", "value":name}])
        selector.appendChild(option)
    })

}


provinces_to_code = getAndSetAddress(url_provinces, provinces_select, "Province")

provinces_select.addEventListener('change', (e)=> {
    code = provinces_to_code[e.target.value]
    console.log(code)
    url_districts = `https://vn-public-apis.fpo.vn/districts/getByProvince?provinceCode=${code}&limit=-1`
    wardses_select.innerHTML=''
    districts_to_code = getAndSetAddress(url_districts, districts_select, "District")
    console.log(districts_to_code)
})

districts_select.addEventListener('change', (e)=> {
    code = districts_to_code[e.target.value]
    console.log(code)
    url_wardses = `https://vn-public-apis.fpo.vn/wards/getByDistrict?districtCode=${code}&limit=-1`
    wardses_to_code = getAndSetAddress(url_wardses, wardses_select, "Wards")
    
})


let household_size = 0;
let current_household_size = 1;

function customCreateElement(type, id=null, styles = null , innerHTML= null, attributes = null) {
    const elem = document.createElement(type)
    if(styles != null)
        styles.forEach(style => {
            elem.classList.add(style)
        });
    
    if(id!=null)
        elem.id = id
    
    if(attributes != null)
        attributes.forEach(attribute => {
                elem.setAttribute(attribute.name, attribute.value)
            });
    if(innerHTML != null)
        elem.innerHTML = innerHTML
    console.log(elem)
    return elem
}

const household_size_input = document.querySelector("#household-size")

household_size_input.addEventListener('change', () => {
    household_size = household_size_input.value
    console.log(household_size)
}) 

function createPerson(person_number) 
{
    const outer_div = customCreateElement(type = 'div', id = "", styles=['form-control', 'mb-3'])

    const person_title = document.createElement(type = 'h5')
    person_title.innerHTML = `Person ${current_household_size}`
                
    const gender_title = customCreateElement('p', null, ["form-label"], 'Gender')
    const gender_div =  customCreateElement('div', null, ["mb-3"], null, null)
    const  male_input = customCreateElement('input', `male_${current_household_size}`, ["form-check-input"],  null, [{"name":"type", "value":"radio"}, {"name": "name", "value": `gender_${current_household_size}`}, {"name":"checked", "value":"true"}, {"name":"value", "value":"male"}])
    const male_lable = customCreateElement('label', null, ["form-check-label"], "Male", [{"name":"for", "value":`male_${current_household_size}`}])
    const male_div =  customCreateElement('div', null, ["form-check", "form-check-inline"], null, null)
    male_div.appendChild(male_input)
    male_div.appendChild(male_lable)

    const  female_input = customCreateElement('input', `female_${current_household_size}`, ["form-check-input"],  null, [{"name":"type", "value":"radio"}, {"name":"name", "value": `gender_${current_household_size}`}, {"name":"value", "value":"female"}])
    const female_lable = customCreateElement('label', null, ["form-check-label"], "Female", [{"name":"for", "value":`female_${current_household_size}`}])
    const female_div =  customCreateElement('div', null, ["form-check", "form-check-inline", "ml-4"], null, null)
    female_div.appendChild(female_input)
    female_div.appendChild(female_lable)
    
    const  others_input = customCreateElement('input', `others_${current_household_size}`, ["form-check-input"],  null, [{"name":"type", "value":"radio"}, {"name":"name", "value": `gender_${current_household_size}`}, {"name":"value", "value":"others"}])
    const others_lable = customCreateElement('label', null, ["form-check-label"], "Others", [{"name":"for", "value":`others_${current_household_size}`}])
    const others_div =  customCreateElement('div', null, ["form-check", "form-check-inline", "ml-4"], null, null)
    others_div.appendChild(others_input)
    others_div.appendChild(others_lable)
    
    
    const year_div = customCreateElement('div', null, ["mb-3"], null, null)
    const year_lable = customCreateElement('label', null, null,"Year of birth", null)
    const year_input = customCreateElement('input', `datepicker_${current_household_size}`, ["form-control"], null,[{"name": "type", "value": "text"}, {"name":"name", "value": `birth-year_${current_household_size}`}])

    const date_piceker = `#datepicker_${current_household_size}`
    console.log($(date_piceker))

    
    $(document).ready(function(){
        $(date_piceker).datepicker({
            format: "yyyy",
            viewMode: "years", 
            minViewMode: "years"
        });
      });

    const occupation_input_div = customCreateElement('div', null, ['mb-3'], null, null)
    const occupation_lable = customCreateElement('label', null, ['form-lable1'], 'Occupation', null)
    const occupation_input = customCreateElement('select', `occupation_${current_household_size}`, ['form-select'] ,null, [{"name":"aria-label", "value":"Default select example"}, {"name":"name", "value":`occupation_${current_household_size}`}])
    occupation_list.forEach( job => {
        occupation_input.appendChild( customCreateElement('option', null,null, job, [{"name":"value", "value":job}]))
    })

    occupation_input_div.appendChild(occupation_input)



    year_div.appendChild(year_lable)
    year_div.appendChild(year_input)

    outer_div.appendChild(person_title)
    outer_div.appendChild(gender_title)
    outer_div.appendChild(gender_div)
    gender_div.appendChild(male_div)
    gender_div.appendChild(female_div)
    gender_div.appendChild(others_div)
    outer_div.appendChild(year_div)
    outer_div.appendChild(occupation_lable)
    outer_div.appendChild(occupation_input_div)

    
    return outer_div
}


add_btn.addEventListener('click', function(even) {
    even.preventDefault();
    console.log('test')

    if(current_household_size < household_size)
    {
        current_household_size++
        personElements = createPerson(current_household_size)
        person_warpper.appendChild(personElements)

    }


})

// $("#datepicker_1").hide()