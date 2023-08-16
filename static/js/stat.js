
const general_district = document.querySelector('#btn-check-outlined-2')
const district = document.querySelector('#districts_stat')
const general_province = document.querySelector('#btn-check-outlined-1')
const province = document.querySelector('#provinces_stat')
const general_ward = document.querySelector('#btn-check-outlined-3')
const ward = document.querySelector('#wards_stat')
const view_stat_btn = document.querySelector('#view_stat_btn-3823')
var title = "all"
var selected_province = ""
var province_existed = false 
var district_existed = false 
document.addEventListener("DOMContentLoaded", function(){
  const event_title = document.getElementById("province_name")
  event_title.addEventListener("change", function(e){
    selected_province = e.target.value
    //console.log(selected_province)
    title = "province"
    if(selected_province == "") {
      province_existed = false
    }
    else {
      province_existed = true 
    }
  })
})
document.addEventListener("DOMContentLoaded", function(){
  const event_title = document.getElementById("btn-check-outlined-1")
  event_title.addEventListener("focus", function(e){
    title = "province"
  })
})
document.addEventListener("DOMContentLoaded", function(){
  const event_title = document.getElementById("btn-check-outlined-4")
  event_title.addEventListener("focus", function(e){
    title = "ages"
  })
})
document.addEventListener("DOMContentLoaded", function(){
  const event_title = document.getElementById("btn-check-outlined-5")
  event_title.addEventListener("focus", function(e){
    title = "jobs"
  })
})
document.addEventListener("DOMContentLoaded", function(){
  const event_title = document.getElementById("btn-check-outlined-6")
  event_title.addEventListener("focus", function(e){
    title = "genders"
  })
})
function getChart(bar_Colors, border_Colors, dataPoints, labels, ctx) {
  var title_chart = "Dân Số Theo Tất Cả Quận"
  var set = false
  switch(title) {
    case "province" : {
      set = true
      if(province_existed === true) {
        if(district_existed === true) {
        }
        else {
          title_chart = "Dân Số Theo " + selected_province
        }
      }
      else {
        title_chart = "Dân Số Theo Các Tỉnh, Thành Phố"
      }
    }
    case "jobs": {
      if(set === false) {
        title_chart = "Dân Số Theo Nghề Nghiệp"
      }
    }
    case "all": {
      return chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              backgroundColor: bar_Colors,
              data: dataPoints,
              borderColor: border_Colors,
              borderWidth: 1,
            },
          ],
        },
        options: {
          plugins: {
            datalabels: {
              anchor: 'center',
              formatter: (value, ctx) => {
                let dataset = ctx.dataset.data;
                let sum = dataset.reduce((total, data) => total + data, 0);
                let percentage = ((value / sum) * 100).toFixed(2) + "%";
                return percentage;
              },
              fontSize: 12,
              color: '#fff',
            },
          },
          legend: {
            position: 'top', // Adjust the legend position
            align: 'start',  // Align the legend with the start of the chart
            labels: {
              fontColor: '#fff',
              generateLabels: (chart) => {
                return chart.data.labels.map((label, index) => ({
                  text: label,
                  fillStyle: chart.data.datasets[0].backgroundColor[index],
                }));
              },
            },
          },
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            xAxes: [
               {
                   stacked: true,
                   gridLines: {
                    color: "transparent",
                    display: true,
                    drawBorder: false,
                    zeroLineColor: "#fff",
                    zeroLineWidth: 1
    
    
                  },
                   ticks: {
                    fontColor: '#fff', // Change to the desired color
                  },
               }
             ],
            yAxes: [
               {
                   stacked: true,
                   gridLines: {
                    color: "transparent",
                    display: true,
                    drawBorder: false,
                    zeroLineColor: "#fff",
                    zeroLineWidth: 1
    
    
                  },
                   ticks: {
                    fontColor: '#fff', // Change to the desired color
                  },
               }
             ]
           },
          animation: {
            animateRotate: true,
            duration: 2000,
            animateScale: true
          },
          title: {
            display: true,
            text: title_chart,
            fontColor: '#ffffff',
            fontSize: 20,
            position: 'right',
          },
          // tooltips: {
          //   callbacks: {
          //     label: function (tooltipItem, data) {
          //       var dataset = data.datasets[tooltipItem.datasetIndex];
          //       var currentValue = dataset.data[tooltipItem.index];
          //       return data.labels[tooltipItem.index] + ": " + currentValue + " người";
          //     },
          //   },
          // },
          layout:{
            padding:{
              top: 10,
              bottom:5
            }
          }      
        },
      });
      break;
    }
    case "genders": {
      set = true
      title_chart = "Dân Số Theo Giới Tính"
    }
    case "ages": {
      if(set === false) {
       title_chart = "Dân Số Theo Độ Tuổi"
      }
      return chart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: labels,
          datasets: [
            {
              backgroundColor: bar_Colors,
              data: dataPoints,
              borderColor: bar_Colors,
              borderWidth: 1,
            },
          ],
        },
        options: {
          plugins: {
            datalabels: {
              formatter: (value, ctx) => {
                let dataset = ctx.dataset.data;
                let sum = dataset.reduce((total, data) => total + data, 0);
                let percentage = ((value / sum) * 100).toFixed(2) + "%";
                return percentage;
              },
              fontSize: 12,
              color: '#fff',
            }    
          },
          responsive: true,
          maintainAspectRatio: false,
          title: {
            display: true,
            text: title_chart,
            fontColor: '#ffffff',
            fontSize: 20,
            position: 'right',
          },
          legend: {
            display: true,
            position: 'right',
            labels: {
              fontColor: '#ffffff',
              fontSize: 13,
            },     
    
          },
          layout:{
            padding:{
              top: 10,
              bottom:5
            }
          }      
        },
      });
      break;
    }
  }
}
function updateChart(jdata) {
  let labels = [];
  let dataPoints = [];
  //console.log(jdata)
  jdata.forEach(item => {
    if(province_existed === true) {
      if(district_existed === true) {
      }
      else {
        if(item.addr1 === selected_province) {
          labels.push(item.addr2)
        }
      }
    }
    else if(title === "all") {
      labels.push(item.addr2);
    }
    else if(title === "province") {
      labels.push(item.addr1);
    }
    else if(title === "ages") {
      labels.push(item.age_group);
      dataPoints.push(parseInt(item['count']));
      return;
    }
    else if(title === "genders") {
      labels.push(item.gender);
    }
    else if(title === "jobs") {
      labels.push(item.occupation);
    }
    dataPoints.push(parseInt(item['count(*)']));
    
  });
  
  var canvas = document.getElementById("chart-3823");
  canvas.remove()
  const oldChart = document.getElementsByClassName("chartjs-size-monitor")
  if (oldChart.length) {
    for (let chart of oldChart) {
      chart.remove()
    }
  }
  const newCanvas = document.createElement("canvas")
  newCanvas.id = "chart-3823"
  var canvas_container = document.getElementById("chart_container-8823");
  canvas_container.append(newCanvas)
  var ctx = newCanvas.getContext("2d")
  newCanvas.style.width = "100%";
  newCanvas.style.height = "100%";
  var bar_Colors = [
    'rgba(255, 99, 132, 0.5)',
    'rgba(54, 162, 235, 0.5)',
    'rgba(255, 206, 86, 0.5)',
    'rgba(75, 192, 192, 0.5)',
    'rgba(153, 102, 255, 0.5)',
    'rgba(255, 159, 64, 0.5)',
    'rgba(201, 203, 207, 0.5)',
    'rgba(255, 0, 0, 0.5)',
    'rgba(0, 255, 0, 0.5)',
    'rgba(0, 0, 255, 0.5)',
    'rgba(128, 128, 128, 0.5)',
    'rgba(0, 128, 128, 0.5)',
    'rgba(128, 0, 128, 0.5)',
    'rgba(255, 255, 0, 0.5)',
    'rgba(0, 255, 255, 0.5)'
  ];
  
  var border_Colors = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
    'rgba(201, 203, 207, 1)',
    'rgba(255, 0, 0, 1)',
    'rgba(0, 255, 0, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(128, 128, 128, 1)',
    'rgba(0, 128, 128, 1)',
    'rgba(128, 0, 128, 1)',
    'rgba(255, 255, 0, 1)',
    'rgba(0, 255, 255, 1)'
  ];
  var chart =  getChart(bar_Colors, border_Colors, dataPoints, labels, ctx)
}

view_stat_btn.addEventListener('click', function() {
  link = "/api/district/num"
  if(province_existed === true) {
    if(district_existed === true) {
       
    } 
    else {
      link = "/api/district/num"
    }
  }
  else if(title === "province") {
    link = "/api/province/num"
  }
   else if(title === "jobs") {
     link = "/api/occupation"
   }
   else if(title === "ages") {
     link = "/api/age_groups"
   }
   else if(title === "genders") {
     link = "/api/gender"
   }
  fetch(link)
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("NETWORK RESPONSE ERROR");
    }
  })
  .then(data => {
    updateChart(data);
  })
  .catch(error => console.error("FETCH ERROR:", error));
});

// Disable checkbox functionality
const checkboxes = document.querySelectorAll('.btn-check');
const form_inputs = document.querySelectorAll('.form-select');

checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', function() {
    if (this.checked) {
      // Disable other checkboxes
      checkboxes.forEach(otherCheckbox => {
        if (otherCheckbox !== this) {
          otherCheckbox.disabled = true;
        }
      });
      form_inputs.forEach(otherFormInput=>{
        otherFormInput.disabled = true;
      });
    } 
    else {
      // Enable all checkboxes
      checkboxes.forEach(otherCheckbox => {
        otherCheckbox.disabled = false;
      });
      form_inputs.forEach(otherFormInput=>{
        otherFormInput.disabled = false;
      });
    }
  });
});

//Disable form select

form_inputs.forEach(form_inpt => {
  form_inpt.addEventListener('change', function() {
    if (this.value !== 'None') {
      // Disable other form inputs
      form_inputs.forEach(other_form_input => {
        if (this !== other_form_input) {
          if (
            this.classList.contains("addr_attribute") &&
            !other_form_input.classList.contains("addr_attribute")
          ) {
            other_form_input.disabled = true;
          } else if (
            !this.classList.contains("addr_attribute")
          ) {
            other_form_input.disabled = true;
          }
        }
      });

      // Disable checkboxes
      checkboxes.forEach(otherCheckbox => {
        otherCheckbox.disabled = true;
      });
    } else {
      // Re-enable all form inputs and checkboxes
      form_inputs.forEach(other_form_input => {
        other_form_input.disabled = false;
      });

      checkboxes.forEach(otherCheckbox => {
        otherCheckbox.disabled = false;
      });
    }
  });
});
