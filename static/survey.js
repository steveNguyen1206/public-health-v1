const person_warpper = document.querySelector('#persons-wrapper')
const add_btn = document.querySelector('#add-person')
const provinces_input = document.querySelector('#provinces')
const districts_input = document.querySelector('#districts')
const wardses_input = document.querySelector('#wardses')

const provinces_options = document.querySelector('#provinces-list')
const districts_options = document.querySelector('#districts-list')
const wardses_options = document.querySelector('#wardses-list')

const household_size_input = document.querySelector('#household-size')
const occupation_datalist = document.querySelector('#occupation-list')

const reset_btn_1 = document.querySelector('#reset_1')
const remove_1 = document.querySelector('#remove_1')



remove_1.addEventListener('click', removePerson)

reset_btn_1.addEventListener('click', resetPerson)

let household_size = 1
let current_hhsize = 1

household_size_input.addEventListener('change', ()=> {
    const value = Number(household_size_input.value)
    if(value !== household_size)
    {
        console.log(value)
        add_btn.removeAttribute('disabled')
        household_size = value
    }
})




const occupation_list = [
    'Doctor',
    'Teacher',
    'Labor',
    'Farmer',
    'Student'
]

occupation_list.forEach( job => {
    occupation_datalist.appendChild( customCreateElement('option', null,null, job))
})



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
    if(type == 'Province')
        provinces_options.appendChild(customCreateElement('option', null, null, 'Province', [{"name":"disabled", "value":'true'}, {"name":"selected", "value":'true'}]))

    setAddress(data, selector)
    data = Object.assign({}, ...data.map((x) => ({[x.name]: x.code})))
    if(type == 'Province')
    {
        provinces_to_code = data
    }
    else if (type == 'District')
    {
        districts_to_code = data
    }
    else wardses_to_code = data
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
        option = customCreateElement('option', null, null,name,[{"name":"value", "value":name}])
        selector.appendChild(option)
    })

}


provinces_to_code = getAndSetAddress(url_provinces, provinces_options, "Province").then( () => {provinces_input.value = 'Hồ Chí Minh';
provincesChange()})

function provincesChange() {
    code = provinces_to_code[provinces_input.value]
    console.log(code)
    url_districts = `https://vn-public-apis.fpo.vn/districts/getByProvince?provinceCode=${code}&limit=-1`
    wardses_options.innerHTML=''
    districts_options.innerHTML = ''
    districts_input.value = ''
    wardses_input.value = ''
    getAndSetAddress(url_districts, districts_options, "District")
    console.log(districts_to_code)
}



provinces_input.addEventListener('change', ()=> {
  provincesChange()
})

districts_input.addEventListener('change', (e, value=null)=> {
    code = districts_to_code[e.target.value]
    console.log(code)
    url_wardses = `https://vn-public-apis.fpo.vn/wards/getByDistrict?districtCode=${code}&limit=-1`
    wardses_input.value = ''
    getAndSetAddress(url_wardses, wardses_options, "Wards")
    
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
    if(new_id != null)
        elem.id = new_id
    
    if(html != null)
        elem.innerHTML = html

    if(value != null)
        elem.value = value
    
    if(name != null)
        // name.forEach( (i) => {
        //     elem.setAttribute(i.name, i.value)
        // })
        elem.setAttribute("name", name)
}

function resetPerson(event)
{
    event.preventDefault()
    let person_number = event.target.getAttribute("person")
    console.log(`g ${person_number}`)
    findAndSetID(`#gender_${person_number}`, null, null, null, "")
    console.log('d')
    findAndSetID(`#datepicker_${person_number}`, null, null, null, "")
    console.log('c')
    findAndSetID(`#occupation_${person_number}`, null, null, null, "")
}

function removePerson(event)
{
    event.preventDefault()
    let person_number = event.target.getAttribute("person")
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
                console.log(i)
                findAndSetID(`#person_${i}`, `person_${i-1}`)
                const person = document.querySelector(`#person_${i-1}`)
                person.querySelector('h6').innerHTML = `Thành viên ${i-1}`

                findAndSetID(`#gender_${i}`, `gender_${i-1}`, `gender_${i-1}`)
                findAndSetID(`#datepicker_${i}`, `datepicker_${i-1}`, `birth-year_${i-1}`)
                findAndSetID(`#occupation_${i}`, `occupation_${i-1}`, `occupation_${i-1}`)
                findAndSetID(`#reset_${i}`, `reset_${i-1}`)
                findAndSetID(`#remove_${i}`, `remove_${i-1}`)
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

    }
    else alert("Số lượng tối thiểu là 1!")
}

function createPerson(person_number) 
{
    const outer_div = customCreateElement('div', `person_${person_number}`, ['form-control', 'mb-3'],null, null)
    const outer_row = customCreateElement('div', "", ['row'],null, null)

    const person_title = document.createElement(type = 'h6')
    person_title.innerHTML = `Thành viên ${person_number}`
                
    const gender_title = customCreateElement('label', null, ["form-label"], 'Giới tính')
    const gender_col =  customCreateElement('div', null, ["col", "mb-3"], null, null)
    const  gender_input = customCreateElement('select', `gender_${person_number}`, ["form-select"],  null, [{"name": "name", "value": `gender_${person_number}`}])
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
    const year_input = customCreateElement('input', `datepicker_${person_number}`, ["form-control"], null,[{"name": "type", "value": "text"}, {"name":"name", "value": `birth-year_${person_number}`}])

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
    const occupation_input = customCreateElement('input', `occupation_${person_number}`, ['form-select'] ,null, [{"name":"type", "value":"text"},{"name":"name", "value":`occupation_${person_number}`}, {"name":"list", "value":'occupation-list'}])
    // occupation_list.forEach( job => {
    //     occupation_datalist.appendChild( customCreateElement('option', null,null, job))
    // })
    occupation_col.appendChild(occupation_label)
    occupation_col.appendChild(occupation_input)

    const modify_col = customCreateElement('div', null, ["col"], null, null)
    const reset_btn = customCreateElement('button', `reset_${person_number}`, ["btn", "btn-primary", "mb-1"], "Đặt lại", [{"name":"person", "value":person_number}])
    const remove_btn = customCreateElement('button', `remove_${person_number}`, ["btn", "btn-primary"], "Xóa thành viên", [{"name":"person", "value":person_number}])
    remove_btn.addEventListener('click', removePerson)
    reset_btn.addEventListener('click', resetPerson)

    modify_col.appendChild(reset_btn)
    modify_col.appendChild(remove_btn)

    outer_row.appendChild(person_title)
    outer_row.appendChild(gender_col)
    outer_row.appendChild(year_col)
    outer_row.appendChild(occupation_col)
    outer_row.appendChild(modify_col)
    
    outer_div.appendChild(outer_row)
    return outer_div
}


add_btn.addEventListener('click', function(even) {
    even.preventDefault();
    
    if(household_size < current_hhsize )
    {
        const res = confirm("Bạn sẽ phải nhập lại từ đầu. Vẫn tiếp tục?")
        if(res)
        {
            current_hhsize = 0
            person_warpper.innerHTML = ''
        }

    } 

    for (let i = current_hhsize + 1; i <= household_size; i++) {     
            personElements = createPerson(i)
            person_warpper.appendChild(personElements)
    } 
    current_hhsize = household_size

    add_btn.setAttribute('disabled', '')

})


$(document).ready(function() {
    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });
  });




// $("#datepicker_1").hide()