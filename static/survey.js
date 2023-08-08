const person_warpper = document.querySelector('#persons-wrapper')
const p_addr_wrapper_1 = document.querySelector('#p-addr-wrapper_1')
const provinces_input = document.querySelector('#provinces')
const districts_input = document.querySelector('#districts')
const wardses_input = document.querySelector('#wardses')

const person_provinces_input_1 = document.querySelector('#person-provinces_1')
const person_districts_input_1 = document.querySelector('#person-districts_1')
const person_wardses_input_1 = document.querySelector('#person-wardses_1')

const provinces_options = document.querySelector('#provinces-list')
const districts_options = document.querySelector('#districts-list')
const wardses_options = document.querySelector('#wardses-list')
const person_districts_options_1 = document.querySelector('#person-districts-list_1')
const person_wardses_options_1 = document.querySelector('#person-wardses-list_1')

const household_size_input = document.querySelector('#household-size')
const occupation_datalist = document.querySelector('#occupation-list')

const reset_btn_1 = document.querySelector('#reset_1')
const remove_1 = document.querySelector('#remove_1')

const add_person = document.querySelector("#add-person")
const minus_person = document.querySelector("#minus-person")
minus_person.setAttribute('disabled', '')


const person_addr_check_1 = document.querySelector("#person-addr-check_1")
let person_addr_not_with_family = false

remove_1.addEventListener('click', removePerson)
reset_btn_1.addEventListener('click', resetPerson)

let household_size = 1
let current_hhsize = 1

household_size_input.addEventListener('change', ()=> {
    const value = Number(household_size_input.value)
    if(value !== household_size)
    {
        console.log(value)
        // add_btn.removeAttribute('disabled')
        updateHousholdSize()
    }
    // else add_btn.setAttribute('disabled', '')
})

add_person.addEventListener('click', (event) => {
    event.preventDefault()
    household_size++
    household_size_input.value=household_size
    updateHousholdSize()
    minus_person.removeAttribute('disabled')
})

minus_person.addEventListener('click', (event) => {
    if(current_hhsize > 1)
    {
        event.preventDefault()
        household_size--
        household_size_input.value=household_size
        updateHousholdSize()
    }
    if(current_hhsize == 1) minus_person.setAttribute('disabled', '')
})

function updateHousholdSize()
{
    const value = Number(household_size_input.value)
    if(value < current_hhsize )
    {
        const res = confirm("Bạn sẽ phải nhập lại từ đầu. Vẫn tiếp tục?")
        if(res)
        {
            current_hhsize = 0
            person_warpper.innerHTML = ''
            household_size = value
        }
        else household_size_input.value = household_size
    }
    else household_size = value

    for (let i = current_hhsize + 1; i <= household_size; i++) {     
            personElements = createPerson(i)
            person_warpper.appendChild(personElements)
    } 
    current_hhsize = household_size
}

// household_size_input.addEventListener("focusout", () =>{
//     updateHousholdSize()
// })

const p_addr_inputs_1 = p_addr_wrapper_1.querySelectorAll('input')
person_addr_check_1.addEventListener('change', ()=>{
    person_addr_not_with_family = person_addr_check_1.checked
    console.log(person_addr_not_with_family)
    if(person_addr_not_with_family)
    {
        p_addr_wrapper_1.classList.remove('display-none')
        p_addr_inputs_1.forEach((elem) => {
            console.log(elem)
            elem.setAttribute('required', '')
        })
    }
    else {
        p_addr_wrapper_1.classList.add('display-none')
        p_addr_inputs_1.forEach((elem) => {
            elem.removeAttribute('required')
        })
    }
})

const occupation_list = [
    'Bác sĩ',
    'Giáo viên',
    'Công nhân',
    'Nông dân',
    'Học sinh',
    'Thương nhân',
    'Công chức'
]

occupation_list.forEach( job => {
    occupation_datalist.appendChild( customCreateElement('option', null,null, job))
})



// const url_provinces = "https://vn-public-apis.fpo.vn/provinces/getAll?limit=-1"
const api_host = "https://provinces.open-api.vn/api/"

let provinces_to_code = []
let districts_to_code = []
let p_districts_to_code = []
let wardses_to_code = []
let p_wardses_to_code = []


async function getAndSetAddress(url, selector, type) {
    let res = await fetch(url);
    data = []
    res = await res.json();
    // data = res.data
    selector.innerHTML=''
    if(type == 'Province')
    {
        data = res
    }
    else if (type == 'District')
    {
        data = res.districts
    }
    else data = res.wards
    console.log(type)

    setAddress(data, selector)
}

async function test(url)
{
    const data = await fetch(url);
    const res = await data.json();
    return res;
}

function setAddress(data, selector)
{
    data.forEach(item => {
        const name = item.name
        const id = item.code
        option = customCreateElement('option', null, null,name,[{"name":"value", "value":name}, {"name":"data_id", "value": id}])
        selector.appendChild(option)
    })

}

function value2Code(value) {
    let selected_option = document.querySelector('option[value="'+value+'"]')
    let code = selected_option.getAttribute('data_id')
    return code
}

let url_provinces = api_host + "?depth=1"
console.log(url_provinces)
getAndSetAddress(url_provinces, provinces_options, "Province").then( () => {
    let value = 'Thành phố Hồ Chí Minh';
    provinces_input.value = value
    person_provinces_input_1.value = value
    let code = value2Code(value)
    provincesChange(code, wardses_options, districts_options, wardses_input, districts_input)
    provincesChange(code, person_wardses_options_1, person_districts_options_1, person_wardses_input_1, person_districts_input_1)
})



function provincesChange(code, wardses_options, districts_options, wardses_input, districts_input) {
    // code = provinces_to_code[selector.value]
    // url_districts = `https://vn-public-apis.fpo.vn/districts/getByProvince?provinceCode=${code}&limit=-1`
    // console.log(selector.options)
    url_districts = api_host + "p/" + code +  "?depth=2"
    console.log(url_districts)
    wardses_options.innerHTML=''
    districts_options.innerHTML = ''
    districts_input.value = ''
    wardses_input.value = ''
    getAndSetAddress(url_districts, districts_options, "District")
    // console.log(districts_to_code)
}

function districtsChange(code, wardses_options, wardses_input) {
    // console.log(event.target.value)
    // if(unit == "family")
    //     code = districts_to_code[event.target.value]
    // else code = p_districts_to_code[event.target.value]
    console.log(code)
    // url_wardses = `https://vn-public-apis.fpo.vn/wards/getByDistrict?districtCode=${code}&limit=-1`
    url_wardses = api_host + "d/" + code + "?depth=2"
    console.log(url_wardses)
    wardses_input.value = ''
    getAndSetAddress(url_wardses, wardses_options, "Wards")
}



provinces_input.addEventListener('change', ()=> {
    let value = event.target.value
    let code = value2Code(value)
    provincesChange(code, provinces_input, wardses_options, districts_options, wardses_input, districts_input)
})

person_provinces_input_1.addEventListener('change', ()=> {
    let value = event.target.value
    let code = value2Code(value)
    provincesChange(code, person_provinces_input_1, person_wardses_options_1, person_districts_options_1, person_wardses_input_1, person_districts_input_1)
  })

districts_input.addEventListener('change', ()=> {
    let value = event.target.value
    let code = value2Code(value)
    districtsChange(code, wardses_options, wardses_input)
})

person_districts_input_1.addEventListener('change', ()=> {
    let value = event.target.value
    let code = value2Code(value)
    districtsChange(code, person_wardses_options_1, person_wardses_input_1)
})


// let person_number = 1;

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
    // console.log(elem)
    return elem
}

// const household_size_input = document.querySelector("#household-size")

// household_size_input.addEventListener('change', () => {
//     household_size = household_size_input.value
//     console.log(household_size)
// }) 

function findAndSetID(old_selector, new_id=null, name=null, html = null, value=null)
{
    
    const elem = document.querySelector(old_selector)
    // console.log(elem)
    if(new_id != null)
    elem.id =  new_id
    
    if(html != null)
        elem.innerHTML = html
    
    if(value != null)
        elem.value =  value
    
    if(name != null)
    // name.forEach( (i) => {
        //     elem.setAttribute(i.name, i.value)
        // })
        elem.setAttribute('name', name)
}

function resetPerson()
{
    event.preventDefault()
    let person_number   
    if(event.target.tagName == "I")
        person_number = event.target.parentNode.getAttribute("person")
    else person_number = event.target.getAttribute("person")
    console.log(`g ${person_number}`)
    findAndSetID(`#gender_${person_number}`, null, null, null, "")
    console.log('d')
    findAndSetID(`#datepicker_${person_number}`, null, null, null, "")
    console.log('c')
    findAndSetID(`#occupation_${person_number}`, null, null, null, "")
}

function removePerson()
{
    event.preventDefault()
    let person_number
    if(event.target.tagName == "I")
        person_number = event.target.parentNode.getAttribute("person")
    else person_number = event.target.getAttribute("person")
    console.log(person_number)
    if(household_size > 1)
    {
        for(let i = 1; i <= current_hhsize; i++)
        {
            if (i == person_number)
            {
                console.log('remove')
                const remove_person = document.querySelector(`#person_${person_number}`)
                person_warpper.removeChild(remove_person)
            } 
            else if ( i > person_number){
                findAndSetID(`#person_${i}`, `person_${i-1}`)
                const person = document.querySelector(`#person_${i-1}`)
                person.querySelector('h6').innerHTML = `Thành viên ${i-1}`

                findAndSetID(`#gender_${i}`, `gender_${i-1}`, `gender_${i-1}`)
                findAndSetID(`#datepicker_${i}`, `datepicker_${i-1}`, `birth-year_${i-1}`)
                findAndSetID(`#occupation_${i}`, `occupation_${i-1}`, `occupation_${i-1}`)
                findAndSetID(`#reset_${i}`, `reset_${i-1}`)
                findAndSetID(`#remove_${i}`, `remove_${i-1}`)
                findAndSetID(`#person-addr-wrapper_${i}`, `person-addr-wrapper_${i-1}`)
                findAndSetID(`#person-addr-check_${i}`, `person-addr-check_${i-1}`)
                findAndSetID(`#p-addr-wrapper_${i}`, `p-addr-wrapper_${i-1}`)
                findAndSetID(`#person-provinces_${i}`, `person-provinces_${i-1}`, `p-province_${person_number}`)
                findAndSetID(`#person-districts_${i}`, `person-districts_${i-1}`, `p-district_${person_number}`)
                findAndSetID(`#person-wardses_${i}`, `person-wardses_${i-1}`, `p-wards_${person_number}`)
                findAndSetID(`#person-districts-list_${i}`, `person-districts-list_${i-1}`)
                findAndSetID(`#person-wardses-list_${i}`, `person-wardses-list_${i-1}`)
                const person_dists_input = person.querySelector(`#person-districts_${i-1}`) 
                person_dists_input.setAttribute('list', `person-districts-list_${i-1}`)
                const person_wards_input = person.querySelector(`#person-wardses_${i-1}`)
                person_wards_input.setAttribute('list', `person-wardses-list_${i-1}`)

                const reset_btn = person.querySelector(`#reset_${i-1}`)
                reset_btn.setAttribute("person", i-1)
                
                const remove_btn = person.querySelector(`#remove_${i-1}`)
                remove_btn.setAttribute("person", i-1)
            }
        }

        current_hhsize--
        household_size=current_hhsize
        console.log(current_hhsize)
        household_size_input.value=current_hhsize

        if(current_hhsize == 1)
            minus_person.setAttribute('disabled', '')

    }
    else alert("Số lượng tối thiểu là 1!")
}

function createPerson(person_number) 
{
    const outer_div = customCreateElement('div', `person_${person_number}`, ['form-control', 'mb-3', 'person-wrapper'],null, null)
    const outer_row = customCreateElement('div', "", ['row'],null, null)

    const person_title = document.createElement(type = 'h6')
    person_title.innerHTML = `Thành viên ${person_number}`
                
    const gender_title = customCreateElement('label', null, ["form-label"], 'Giới tính')
    const gender_col =  customCreateElement('div', null, ["col", "mb-3"], null, null)
    const  gender_input = customCreateElement('select', `gender_${person_number}`, ["form-select"],  null, [{"name": "name", "value": `gender_${person_number}`}, {"name":"required", "value":""}])
    gender_input.innerHTML = `
                <option selected disabled></option>
                <option >Nam</option>
                <option >Nữ</option>
                <option >Khác</option>
    `
    gender_col.appendChild(gender_title)
    gender_col.appendChild(gender_input)
    
    const year_col = customCreateElement('div', null, ["col", "mb-3"], null, null)
    const year_label = customCreateElement('label', null, ["form-label"],"Năm sinh", null)
    const year_input = customCreateElement('input', `datepicker_${person_number}`, ["form-control"], null,[{"name": "type", "value": "text"}, {"name":"name", "value": `birth-year_${person_number}`}, {"name":"required", "value":""}])

    const date_piceker = `#datepicker_${person_number}`
    console.log($(date_piceker))

    
    $(document).ready(function(){
        $(date_piceker).datepicker({
            format: "yyyy",
            viewMode: "years", 
            minViewMode: "years"
        });
      });

    year_col.appendChild(year_label)
    year_col.appendChild(year_input)

    const occupation_col = customCreateElement('div', null, ["col", "mb-3"], null, null)
    const occupation_label = customCreateElement('label', null, ['form-label'], 'Nghề nghiệp', null)
    const occupation_input = customCreateElement('input', `occupation_${person_number}`, ['form-select'] ,null, [{"name":"type", "value":"text"},{"name":"name", "value":`occupation_${person_number}`}, {"name":"list", "value":'occupation-list'}, {"name":"required", "value":""}])
    // occupation_list.forEach( job => {
    //     occupation_datalist.appendChild( customCreateElement('option', null,null, job))
    // })
    occupation_col.appendChild(occupation_label)
    occupation_col.appendChild(occupation_input)

    const modify_col = customCreateElement('div', null, ["person-btn-col"], null, null)
    const reset_btn = customCreateElement('button', `reset_${person_number}`, ["btn", "mb-1", "mybtn-primary", "person-btn"], `<i class="fa-solid fa-rotate-right"></i>`, [{"name":"person", "value":person_number}])
    const remove_btn = customCreateElement('button', `remove_${person_number}`, ["btn",  "mybtn-primary", "person-btn"], `<i class="fa-solid fa-user-xmark"></i>`, [{"name":"person", "value":person_number}])
    remove_btn.addEventListener('click', removePerson)
    reset_btn.addEventListener('click', resetPerson)
    modify_col.appendChild(reset_btn)
    modify_col.appendChild(remove_btn)
    
    const person_addr_wrapper = customCreateElement('div', `person-addr-wrapper_${person_number}`)
    person_addr_wrapper.innerHTML = `
            <div class="form-check mb-3">
              <input class="form-check-input" type="checkbox" value="" id="person-addr-check_${person_number}">
              <label class="form-label form-check-label">
                Không ở chung với gia đình
              </label>
            </div>
  
            <div class="row align-items-center justify-content-between display-none" id="p-addr-wrapper_${person_number}">
              <div class="col-sm mb-3">
                <label class="form-label col-form-label-sm">Tỉnh/ Thành phố</label>
                <input type="text" list="provinces-list" class="form-select" id="person-provinces_${person_number}" name="p-province_${person_number}" autocomplete="off"/>
              </div>
    
              <div class="col-sm mb-3">
                <label class="form-label col-form-label-sm">Quận/ Huyện</label>
                <input type="text" list="person-districts-list_${person_number}" class="form-select" id="person-districts_${person_number}" name="p-district_${person_number}" autocomplete="off"/>
                <datalist id="person-districts-list_${person_number}">
                  <option disabled selected></option>
                </datalist>
              </div>
    
              <div class="col-sm mb-3">
                <label class="form-label col-form-label-sm">Xã/ Phường/ Thị trấn</label>
                <input type="text" list="person-wardses-list_${person_number}" class="form-select" id="person-wardses_${person_number}" name="p-wards_${person_number}" autocomplete="off"/>
                <datalist id="person-wardses-list_${person_number}">
                  <option disabled selected></option>
                </datalist>
              </div>
  
            </div>`
    console.log(person_addr_wrapper)

    const person_addr_check = person_addr_wrapper.querySelector(`#person-addr-check_${person_number}`)
    const p_wrapper = person_addr_wrapper.querySelector(`#p-addr-wrapper_${person_number}`)
    const p_addr_inputs = p_wrapper.querySelectorAll('input')
    person_addr_check.addEventListener('change', ()=> {

        person_addr_not_with_family = person_addr_check.checked
        console.log(person_addr_not_with_family)
        if(person_addr_not_with_family)
        {
            p_wrapper.classList.remove('display-none')
            p_addr_inputs.forEach((elem) => {
                console.log(elem)
                elem.setAttribute('required', '')
            })
        }
        else {
            p_wrapper.classList.add('display-none')
            p_addr_inputs.forEach((elem) => {
                elem.removeAttribute('required')
            })
        }
    })

    const p_provinces_input = p_wrapper.querySelector(`#person-provinces_${person_number}`)
    const p_districts_options = p_wrapper.querySelector(`#person-districts-list_${person_number}`)
    const p_wardses_options = p_wrapper.querySelector(`#person-wardses-list_${person_number}`)
    const p_districts_input = p_wrapper.querySelector(`#person-districts_${person_number}`)
    const p_wardses_input = p_wrapper.querySelector(`#person-wardses_${person_number}`)

    let value = 'Thành phố Hồ Chí Minh';
    p_provinces_input.value = value
    let code = value2Code(value)
    provincesChange(code, p_wardses_options, p_districts_options, p_wardses_input, p_districts_input)

    p_provinces_input.addEventListener('change', ()=> {
        let value = event.target.value
        let code = value2Code(value)
        provincesChange(code, p_wardses_options, p_districts_options, p_wardses_input, p_districts_input)
      })
    
    p_districts_input.addEventListener('change', ()=> {
        let value = event.target.value
        let code = value2Code(value)
        districtsChange(code, p_wardses_options, p_wardses_input)
    })

    outer_row.appendChild(person_title)
    outer_row.appendChild(gender_col)
    outer_row.appendChild(year_col)
    outer_row.appendChild(occupation_col)
    outer_row.appendChild(modify_col)
    outer_row.appendChild(person_addr_wrapper)
    
    outer_div.appendChild(outer_row)
    return outer_div
}


// add_btn.addEventListener('click', function(even) {
//     even.preventDefault();
//     updateHousholdSize()
//     add_btn.setAttribute('disabled', '')
// })


$(document).ready(function() {
    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });
  });




// $("#datepicker_1").hide()