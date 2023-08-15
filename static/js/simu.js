const incubation = document.querySelector('#initial')
const district = document.querySelector('#districts_stat')
const general_province = document.querySelector('#btn-check-outlined-1')
const province = document.querySelector('#provinces_stat')
const general_ward = document.querySelector('#btn-check-outlined-3')
const ward = document.querySelector('#wards_stat')
const view_stat_btn = document.querySelector('#see_simul_btn-15823')

//Draw pie chart
// function updateChart(jdata) {
//   let labels = [];
//   let dataPoints = [];

//   jdata.forEach(item => {
//     labels.push(item.label);
//     dataPoints.push(parseInt(item.y));
//   });
//   var canvas = document.getElementById("chart-3823");
//   var ctx = canvas.getContext("2d");
//   canvas.style.width = "100%";
//   canvas.style.height = "100%";
//   var barColors = [
//     "#b91d47",
//     "#00aba9",
//     "#2b5797",
//     "#e8c3b9",
//     "#1e7145",
//     "#9a5ca5",
//     "#ff7f50",
//     "#ffd700",
//     "#ffa500",
//     "#32cd32",
//     "#ff69b4",
//     "#cd5c5c",
//     "#4169e1",
//     "#8a2be2",
//     "#ff1493",
//     "#20b2aa",
//     "#008080",
//     "#f08080",
//     "#00ced1",
//     "#800080",
//     "#8b4513",
//     "#00ff7f",
//     "#d2691e",
//     "#8b008b",
//     "#4682b4",
//   ];
  
//   var chart = new Chart(ctx, {
//     type: "pie",
//     data: {
//       labels: labels,
//       datasets: [
//         {
//           backgroundColor: barColors,
//           data: dataPoints,
//           borderColor: barColors,
//           borderWidth: 1,
//         },
//       ],
//     },
//     options: {
      
//       plugins: {
//         // Change options for ALL labels of THIS CHART
//         datalabels: {
//           formatter: (value, ctx) => {
//             let sum = ctx.dataset._meta[0].total;
//             let percentage = (value * 100 / sum).toFixed(2) + "%";
//             return percentage;
//           },
//           fontSize: 12,
//           color: '#fff',
//         }    
//       },
//       responsive: true,
//       maintainAspectRatio: false,
//       title: {
//         display: true,
//         text: "Dân số theo mỗi quận",
//         fontColor: '#ffffff',
//         fontSize: 20,
//         position: 'right',
//       },
//       legend: {
//         display: true,
//         position: 'right',
//         labels: {
//           fontColor: '#ffffff',
//           fontSize: 13,
//         },     

//       },
//       // tooltips: {
//       //   callbacks: {
//       //     label: function (tooltipItem, data) {
//       //       var dataset = data.datasets[tooltipItem.datasetIndex];
//       //       var currentValue = dataset.data[tooltipItem.index];
//       //       return data.labels[tooltipItem.index] + ": " + currentValue + " người";
//       //     },
//       //   },
//       // },
//       layout:{
//         padding:{
//           top: 10,
//           bottom:5
//         }
//       }      
//     },
//   });
// }





