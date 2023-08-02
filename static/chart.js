provinces_select = document.querySelector('#provinces_stat')
districts_select = document.querySelector('#districts_stat')
wardses_select = document.querySelector('#wardses_stat')


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
