const general_district = document.querySelector('#btn-check-outlined-2')
const district = document.querySelector('#districts_stat')
const general_province = document.querySelector('#btn-check-outlined-1')
const province = document.querySelector('#provinces_stat')
const general_ward = document.querySelector('#btn-check-outlined-3')
const ward = document.querySelector('#wards_stat')
const view_stat_btn = document.querySelector('#view_stat_btn-3823')

// function updateChart(jdata) {
//   let m_dataPoints = [];

//   jdata.forEach(item => {
//     m_dataPoints.push({ y: parseInt(item.y),x: item.label });
//   });

//   var chart = new CanvasJS.Chart("chart_wrapper-3823", {
//     title: {
//       text: "Dân số theo mỗi quận"
//     },
//     // axisY: {
//     //   title: "Địa đ",
//     //   suffix: "người"
//     // },
//     data: [{
//       type: "pie",	
//       showInLegend: true,
//       yValueFormatString: "# người",
//       indexLabel: "{y}",
//       legendText: "{label}",
//       dataPoints: [{'label': 'Quận Bình Thạnh', 'y': 2}, {'label': 'Quận Tân Phú', 'y': 2}, {'label': 'Quận 12', 'y': 1}, {'label': 'Thành phố Thủ Đức', 'y': 3}]
//     }]
//   });

// 	var deltaY, yVal;
// 	var dps = chart.options.data[0].dataPoints;
// 	for (var i = 0; i < dps.length; i++) {
// 		deltaY = Math.round(2 + Math.random() *(-2-2));
// 		yVal = deltaY + dps[i].y > 0 ? dps[i].y + deltaY : 0;		
// 		dps[i] = {y: yVal};
// 	}
// 	chart.options.data[0].dataPoints = dps; 
// 	chart.render();
// }



view_stat_btn.addEventListener('click', function() {
  
  fetch("/api/district/num").then((response) => {
    // console.log('in funv')
    if (response.ok) {
      response.json().then(data => {
        // 'data' contains the parsed JSON data
        // console.log(data);
        // You can now work with the data
        updateChart(data);
      });
    } else {
      throw new Error("NETWORK RESPONSE ERROR");
    }
  }).catch((error) => console.error("FETCH ERROR:", error));
   
})



