const persons_warpper = document.querySelector('#persons-wrapper')
const provinces_input = document.querySelector('#provinces')
const districts_input = document.querySelector('#districts')
const wardses_input = document.querySelector('#wardses')
const p_addr_wrapper = document.querySelector('#p-addr-wrapper')
const person_provinces_input = document.querySelector('#person-provinces')
const person_districts_input = document.querySelector('#person-districts')
const person_wardses_input = document.querySelector('#person-wardses')
const gender_input = document.querySelector('#gender-input')
const birth_year_input = document.querySelector('#birth-year-input')
const occupation_input = document.querySelector('#occupation-input')
const family_addr = document.querySelector('#family-addr')

const provinces_options = document.querySelector('#provinces-list')
const districts_options = document.querySelector('#districts-list')
const wardses_options = document.querySelector('#wardses-list')
const person_provinces_options = document.querySelector('#person-provinces-list')
const person_districts_options = document.querySelector('#person-districts-list')
const person_wardses_options = document.querySelector('#person-wardses-list')

const household_size_input = document.querySelector('#household-size')
const occupation_datalist = document.querySelector('#occupation-list')

const person_edit_1 = document.querySelector('#person-edit_1')
const person_remove_1 = document.querySelector('#person-remove_1')

const add_person = document.querySelector("#add-person")
const minus_person = document.querySelector("#minus-person")
minus_person.setAttribute('disabled', '')

const model_ok = document.querySelector('#model-ok')


function requireInput()
{
    const inputs = document.querySelectorAll('input')
    inputs.forEach( elem => {
            elem.oninvalid = function () {
            console.log('test')
            elem.setAttribute('placeholder', 'Bắt buộc')
            elem.classList.add('red-placeholder')  
        }
    })
}

requireInput()

persons_warpper.querySelectorAll('input').forEach(elem => {
    elem.addEventListener('click', () => {
        resetPerson()
    })
})


// const person_addr_check_1 = document.querySelector("#person-addr-check_1")
// let person_addr_not_with_family = false

person_remove_1.addEventListener('click', removePerson)
person_edit_1.addEventListener('click', resetPerson)

let household_size = 1
let current_hhsize = 1
let active_person = 1

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
            persons_warpper.innerHTML = ''
            household_size = value
        }
        else household_size_input.value = household_size
    }
    else household_size = value

    for (let i = current_hhsize + 1; i <= household_size; i++) {     
        createPerson(i)
    } 
    current_hhsize = household_size
}


const p_addr_inputs = p_addr_wrapper.querySelectorAll('input')

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



async function getAndSetAddress(url, select_input, select_option, type) {
    let res = await fetch(url);
    data = []
    res = await res.json();
    // data = res.data
    select_option.innerHTML=''
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

    setAddress(data, select_input, select_option)
}

async function test(url)
{
    const data = await fetch(url);
    const res = await data.json();
    return res;
}

function setAddress(data, select_input, select_option)
{
    data.forEach(item => {
        const name = item.name
        const id = item.code
        option = customCreateElement('option', null, null,name,[{"name":"value", "value":name}, {"name":"data_id", "value": id}])
        option.addEventListener('click', ()=> {
            select_input.value = name
            var event = new Event('change');
            select_input.dispatchEvent(event);
            select_option.classList.add('display-none')
        })
        select_option.appendChild(option)
    })

}

function value2Code(value) {
    let selected_option = document.querySelector('option[value="'+value+'"]')
    let code = selected_option.getAttribute('data_id')
    return code
}

// console.log(url_provinces)


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
    model_ok.setAttribute('disabled', '')
    getAndSetAddress(url_districts, districts_input, districts_options, "District")
    // console.log(districts_to_code)
}

function districtsChange(code, wardses_options, wardses_input) {
    // console.log(code)
    url_wardses = api_host + "d/" + code + "?depth=2"
    console.log(url_wardses)
    wardses_input.value = ''
    model_ok.setAttribute('disabled', '')
    getAndSetAddress(url_wardses, wardses_input, wardses_options, "Wards")
}

var filterFunction = function (input, datalist) {
    filter = input.value.toUpperCase();
    options = datalist.getElementsByTagName("option");
    // console.log(options)
    for (i = 0; i < options.length; i++) {
      txtValue = options[i].textContent || options[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        options[i].style.display = "";

      } else {
        options[i].style.display = "none";
      }
    }
  }

let check = false
const option_lists = document.querySelectorAll('.option-list')

option_lists.forEach((elem) => {
    elem.addEventListener("mouseover", () => {
        check = true
    })

    elem.addEventListener("mouseleave", () => {
        check = false
    })
})


function prepareAddr(province_input, district_input, wards_input,
    province_options, district_options, wards_options,)
{
    let url_provinces = api_host + "?depth=1"
    getAndSetAddress(url_provinces, province_input, province_options, "Province").then( () => {
        let value = 'Thành phố Hồ Chí Minh';
        province_input.value = value
        let code = value2Code(value)
        provincesChange(code, wards_options, district_options, wards_input, district_input)
    })

    province_input.addEventListener('focusout', ()=> { 
        if(!check)
            province_options.classList.add('display-none')
    })
    
    district_input.addEventListener('focusout', ()=> {
        if(!check)
            district_options.classList.add('display-none')
    })
    
    wards_input.addEventListener('focusout', ()=> {
        if(!check)
            wards_options.classList.add('display-none')
    })

    province_input.addEventListener('change', ()=> {
        let value = event.target.value
        let code = value2Code(value)
        provincesChange(code, wards_options, district_options, 
            wards_input, district_input)
    })
    
    district_input.addEventListener('change', ()=> {
        let value = event.target.value
        let code = value2Code(value)
        districtsChange(code, wards_options, wards_input)
    })
    
    province_input.addEventListener('focus', ()=> {
        province_options.classList.remove('display-none')
    })
    
    district_input.addEventListener('focus', ()=> {
        district_options.classList.remove('display-none')
    })
    
    wards_input.addEventListener('focus', ()=> {
        wards_options.classList.remove('display-none')
    })
    
    province_input.addEventListener("keyup", filterFunction.bind(this.event, input=province_input, datalist=province_options))
    district_input.addEventListener("keyup", filterFunction.bind(this.event, input=district_input, datalist=district_options))

}


prepareAddr(provinces_input, districts_input, wardses_input,
        provinces_options, districts_options, wardses_options)


prepareAddr(person_provinces_input, person_districts_input, person_wardses_input,
    person_provinces_options, person_districts_options, person_wardses_options)




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


function findAndSetID(old_selector, new_id=null, attr=null, html = null, value=null)
{
    
    const elem = document.querySelector(old_selector)
    // console.log(elem)
    if(new_id != null)
    elem.id =  new_id
    
    if(html != null)
        elem.innerHTML = html
    
    if(value != null)
        elem.value =  value
    
    if(attr != null)
        attr.forEach( (i) => {
            elem.setAttribute(i.name, i.value)
        })
}

function getValueById(id)
{
    console.log(id)
    return document.querySelector('#'+id).value
}

function resetAdderForm(addr, provinces_input, districts_input, districts_options, wardses_input, wardses_options)
{
    districts_input.onchange = ""
    provinces_input.onchange = ""

    const addr_list = addr.split(', ')
    // console.log(addr_list)
    provinces_input.value = addr_list[0]
    if (addr_list[1])
        districts_input.value = addr_list[1]
    else
        districts_input.value = ""
    if(addr_list[2])   
        wardses_input.value = addr_list[2]
    else
        wardses_input.value = ""
    districts_input.addEventListener('change', ()=> {
        let value = event.target.value
        let code = value2Code(value)
        districtsChange(code, wardses_options, wardses_input)
    })

    provinces_input.addEventListener('change', ()=> {
        let value = event.target.value
        let code = value2Code(value)
        provincesChange(code, wardses_options, districts_options, wardses_input, districts_input)
      })

}

family_addr.onclick = () => {
    const addr = family_addr.value
    resetAdderForm(addr, provinces_input, districts_input, districts_options, wardses_input, wardses_options)
}

function resetPerson()
{   
    event.preventDefault()
    if(event.target.tagName == "I")
    person_number = event.target.parentNode.getAttribute("person")
    else person_number = event.target.getAttribute("person")
    console.log(person_number)
    active_person = person_number
   const gender = getValueById(`gender_${person_number}`)
   const birth_year = getValueById(`birth-year_${person_number}`)
   const family_addr_val = family_addr.value
   const p_addr_val = getValueById(`addr_${person_number}`)
   const addr = (p_addr_val != '') ? p_addr_val : family_addr_val
   const occupation = getValueById(`occupation_${person_number}`)

    gender_input.value = gender
    birth_year_input.value = birth_year
    occupation_input.value = occupation

    resetAdderForm(addr, person_provinces_input, person_districts_input, person_districts_options, person_wardses_input, person_wardses_options)
      model_famaddr_warpper.classList.add('display-none')
      model_persons_warpper.classList.remove('display-none')

      model.classList.add('open');
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
                const remove_person = persons_warpper.querySelector(`#person_${person_number}`)
                persons_warpper.removeChild(remove_person)
            } 
            else if ( i > person_number){
                findAndSetID(`#person_${i}`, `person_${i-1}`)
                const person = document.querySelector(`#person_${i-1}`)
                person.querySelector('.p_num').innerHTML = `${i-1}`

                findAndSetID(`#gender_${i}`, `gender_${i-1}`, [{"name":`gender_${i-1}`}, {"name":"person", "value": i-1}])
                findAndSetID(`#birth-year_${i}`, `birth-year_${i-1}`, [{"name": "name", "value":`birth-year_${i-1}`}, {"name":"person", "value": i-1}])
                findAndSetID(`#occupation_${i}`, `occupation_${i-1}`, [{"name": "name", "value": `occupation_${i-1}`}, {"name":"person", "value": i-1}])
                findAndSetID(`#addr_${i}`, `addr_${i-1}`, [{"name": "name", "value": `addr_${i-1}`}, {"name":"person", "value": i-1}])
                findAndSetID(`#person-edit_${i}`, `person-edit_${i-1}`, [{"name":"person", "value": i-1}])
                findAndSetID(`#person-remove_${i}`, `person-remove_${i-1}`, [{"name":"person", "value": i-1}])
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
    const person_new = customCreateElement('tr', `person_${person_number}`, ['person-wrapper'])
    console.log(person_new)
    person_new.innerHTML = `
        <th class="p_num" scope="row">${person_number}</th>
        <td class="col-1">
        <input type="text" class="table-input model-btn" autocomplete="off" placeholder="..." person=${person_number} id="gender_${person_number}" name="gender_${person_number}" required>
        </td>
        <td class="col-1">
        <input type="text" class="table-input model-btn" autocomplete="off" placeholder="..." person=${person_number} id="birth-year_${person_number}" name="birth-year_${person_number}" required>
        </td>
        <td class="col-6">
        <input type="text" class="table-input model-btn" autocomplete="off" placeholder="..." person=${person_number} id="addr_${person_number}" name="addr_${person_number}" required>
        </td>
        <td class="col-2">
        <input type="text" class="table-input model-btn" autocomplete="off" placeholder="..." person=${person_number} id="occupation_${person_number}" name="occupation_${person_number}" required>
        </td>

        <td class="col-2">
        <button id="person-edit_${person_number}" class="btn person-btn model-btn" person="${person_number}" model="person">
            <i class="fa-solid fa-rotate-right"></i>
        </button>
        <button id="person-remove_${person_number}" class="btn person-btn ms-3" person="${person_number}">
            <i class="fa-solid fa-user-xmark"></i>
        </button>
        </td>
        `
    persons_warpper.appendChild(person_new)

    const edit_person = person_new.querySelector(`#person-edit_${person_number}`)
    const remove_person = document.querySelector(`#person-remove_${person_number}`)
    requireInput()
    const open_model = persons_warpper.querySelectorAll('.model-btn')
    open_model.forEach(elem => {
        elem.onclick = () => {
            resetPerson()
            model_famaddr_warpper.classList.add('display-none')
            model_persons_warpper.classList.remove('display-none')
            model.classList.add('open');
    }})
    edit_person.addEventListener('click', resetPerson)
    remove_person.addEventListener('click', removePerson)
    
}



const open_model_btn = document.querySelectorAll('.model-btn');
const model = document.querySelector('.js-model');
const closeBtn = document.querySelectorAll('.model-close');
const container = document.querySelector('.js-model-container');
const model_famaddr_warpper = document.querySelector(".model-family-addr-warpper")
const model_persons_warpper = document.querySelector(".model-person-wrapper")


open_model_btn.forEach(element => {
    element.onclick = function () {
        event.preventDefault()
        
        let model_type   
        if(element.tagName == "I")
            model_type = element.parentNode.getAttribute("model")
        else model_type = element.getAttribute("model")

        console.log(model_type)
        if(model_type == "family-addr")
        {
            model_famaddr_warpper.classList.remove('display-none')
            model_persons_warpper.classList.add('display-none')
        }
        else {
            model_famaddr_warpper.classList.add('display-none')
            model_persons_warpper.classList.remove('display-none')
        }

        model.classList.add('open');
    }
})

function hideModel(){
    model.classList.remove('open');
}

closeBtn.forEach(element => {
    console.log(test)
    element.addEventListener('click', () => {
    event.preventDefault()
    hideModel()
    })
})

model.addEventListener('click', hideModel);
container.addEventListener('click', function (event) {
    event.preventDefault()
    event.stopImmediatePropagation()
    event.stopPropagation();
})


model_ok.addEventListener('click', ()=> {
    let is_family_addr = !model_famaddr_warpper.classList.contains('display-none')
    if(is_family_addr)
    {
        const province = provinces_input.value
        const district = districts_input.value
        const ward =  wardses_input.value   
        if(province != '' && district != '' && ward != '')
        {
            let family_addr_val = province + ", " + district + ", " + ward
            family_addr.value = family_addr_val
        }
    }
    else
    {
        const birth_year = birth_year_input.value
        const gender = gender_input.value
        const occupation = occupation_input.value

        const province = person_provinces_input.value
        const district = person_districts_input.value
        const ward =  person_wardses_input.value   
        if(province != '' && district != '' && ward != '')
        {
            let family_addr_val = province + ", " + district + ", " + ward
            document.querySelector(`#addr_${active_person}`).value = family_addr_val
        }

        if(birth_year && gender && occupation)
        {
            findAndSetID(`#gender_${active_person}`, null, null, null, gender)
            findAndSetID(`#birth-year_${active_person}`, null, null, null, birth_year)
            findAndSetID(`#occupation_${active_person}`, null, null, null, occupation)
        }
    }

    model_ok.setAttribute('disabled', '')
})

$(document).ready(function() {
    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });


    $('.model-family-addr-warpper input').change(()=>{
        console.log('test')
        const empty_input = $('.model-family-addr-warpper input').filter(function() { return this.value == ""; }).length
        if(empty_input == 0)
            $('#model-ok').removeAttr('disabled')
        else
            $('#model-ok').attr('disabled', '')

    })

    $('.model-person-wrapper input').change(()=>{
        console.log('test')
        const empty_input = $('.model-person-wrapper input').filter(function() { return this.value == ""; }).length
        if(empty_input == 0)
            $('#model-ok').removeAttr('disabled')
        else 
            $('#model-ok').attr('disabled', '')
        })
});




// $("#datepicker_1").hide()