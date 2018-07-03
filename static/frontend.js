$(document).ready(function() {

	console.log('document is loaded')

	if (document.URL == "127.0.0.1:5000/") {
		$.get('/onload', function(data, cpas){
			var text = data
			var cpa = cpas
			header = text + "'s dashboard"
			$('.dash-select').text(header)
			console.log(cpa)
		})
	} // end if
	if (document.URL == "127.0.0.1:5000/") {
		$.get('/data-pop', function(data){

			var chart_1_data = []
			obj = JSON.parse(data)

			for (var i = 0; i < obj.length; i++){
				chart_1_data.push(obj[i])
			}

			console.log( chart_1_data)

			demo = {
			  initPickColor: function() {
			    $('.pick-class-label').click(function() {
			      var new_class = $(this).attr('new-class');
			      var old_class = $('#display-buttons').attr('data-class');
			      var display_div = $('#display-buttons');
			      if (display_div.length) {
			        var display_buttons = display_div.find('.btn');
			        display_buttons.removeClass(old_class);
			        display_buttons.addClass(new_class);
			        display_div.attr('data-class', new_class);
			      }
			    });
			  },

			  initDocChart: function() {
			    chartColor = "#FFFFFF";

			    // General configuration for the charts with Line gradientStroke
			    gradientChartOptionsConfiguration = {
			      maintainAspectRatio: false,
			      legend: {
			        display: false
			      },
			      tooltips: {
			        bodySpacing: 4,
			        mode: "nearest",
			        intersect: 0,
			        position: "nearest",
			        xPadding: 10,
			        yPadding: 10,
			        caretPadding: 10
			      },
			      responsive: true,
			      scales: {
			        yAxes: [{
			          display: 0,
			          gridLines: 0,
			          ticks: {
			            display: false
			          },
			          gridLines: {
			            zeroLineColor: "transparent",
			            drawTicks: false,
			            display: false,
			            drawBorder: false
			          }
			        }],
			        xAxes: [{
			          display: 0,
			          gridLines: 0,
			          ticks: {
			            display: false
			          },
			          gridLines: {
			            zeroLineColor: "transparent",
			            drawTicks: false,
			            display: false,
			            drawBorder: false
			          }
			        }]
			      },
			      layout: {
			        padding: {
			          left: 0,
			          right: 0,
			          top: 15,
			          bottom: 15
			        }
			      }
			    };

			    ctx = document.getElementById('lineChartExample').getContext("2d");

			    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
			    gradientStroke.addColorStop(0, '#80b6f4');
			    gradientStroke.addColorStop(1, chartColor);

			    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
			    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
			    gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

			    myChart = new Chart(ctx, {
			      type: 'line',
			      responsive: true,
			      data: {
			        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			        datasets: [{
			          label: "Active Users",
			          borderColor: "#f96332",
			          pointBorderColor: "#FFF",
			          pointBackgroundColor: "#f96332",
			          pointBorderWidth: 2,
			          pointHoverRadius: 4,
			          pointHoverBorderWidth: 1,
			          pointRadius: 4,
			          fill: true,
			          backgroundColor: gradientFill,
			          borderWidth: 2,
			          data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
			        }]
			      },
			      options: gradientChartOptionsConfiguration
			    });
			  },

			  initDashboardPageCharts: function() {

			    chartColor = "#FFFFFF";

			    // General configuration for the charts with Line gradientStroke
			    gradientChartOptionsConfiguration = {
			      maintainAspectRatio: false,
			      legend: {
			        display: false
			      },
			      tooltips: {
			        bodySpacing: 4,
			        mode: "nearest",
			        intersect: 0,
			        position: "nearest",
			        xPadding: 10,
			        yPadding: 10,
			        caretPadding: 10
			      },
			      responsive: 1,
			      scales: {
			        yAxes: [{
			          display: 0,
			          gridLines: 0,
			          ticks: {
			            display: false
			          },
			          gridLines: {
			            zeroLineColor: "transparent",
			            drawTicks: false,
			            display: false,
			            drawBorder: false
			          }
			        }],
			        xAxes: [{
			          display: 0,
			          gridLines: 0,
			          ticks: {
			            display: false
			          },
			          gridLines: {
			            zeroLineColor: "transparent",
			            drawTicks: false,
			            display: false,
			            drawBorder: false
			          }
			        }]
			      },
			      layout: {
			        padding: {
			          left: 0,
			          right: 0,
			          top: 15,
			          bottom: 15
			        }
			      }
			    };

			    gradientChartOptionsConfigurationWithNumbersAndGrid = {
			      maintainAspectRatio: false,
			      legend: {
			        display: false
			      },
			      tooltips: {
			        bodySpacing: 4,
			        mode: "nearest",
			        intersect: 0,
			        position: "nearest",
			        xPadding: 10,
			        yPadding: 10,
			        caretPadding: 10
			      },
			      responsive: true,
			      scales: {
			        yAxes: [{
			          gridLines: 0,
			          gridLines: {
			            zeroLineColor: "transparent",
			            drawBorder: false
			          }
			        }],
			        xAxes: [{
			          display: 0,
			          gridLines: 0,
			          ticks: {
			            display: false
			          },
			          gridLines: {
			            zeroLineColor: "transparent",
			            drawTicks: false,
			            display: false,
			            drawBorder: false
			          }
			        }]
			      },
			      layout: {
			        padding: {
			          left: 0,
			          right: 0,
			          top: 15,
			          bottom: 15
			        }
			      }
			    };

			    var ctx = document.getElementById('bigDashboardChart').getContext("2d");

			    var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
			    gradientStroke.addColorStop(0, '#80b6f4');
			    gradientStroke.addColorStop(1, chartColor);

			    var gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
			    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
			    gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");

			    var myChart = new Chart(ctx, {
			      type: 'line',
			      data: {
			        labels: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
			        datasets: [{
			          label: "Data",
			          borderColor: chartColor,
			          pointBorderColor: chartColor,
			          pointBackgroundColor: "#1e3d60",
			          pointHoverBackgroundColor: "#1e3d60",
			          pointHoverBorderColor: chartColor,
			          pointBorderWidth: 1,
			          pointHoverRadius: 7,
			          pointHoverBorderWidth: 2,
			          pointRadius: 5,
			          fill: true,
			          backgroundColor: gradientFill,
			          borderWidth: 2,
			          data: [50, 150, 100, 190, 130, 90, 150, 160, 120, 140, 190, 95]
			        }]
			      },
			      options: {
			        layout: {
			          padding: {
			            left: 20,
			            right: 20,
			            top: 0,
			            bottom: 0
			          }
			        },
			        maintainAspectRatio: false,
			        tooltips: {
			          backgroundColor: '#fff',
			          titleFontColor: '#333',
			          bodyFontColor: '#666',
			          bodySpacing: 4,
			          xPadding: 12,
			          mode: "nearest",
			          intersect: 0,
			          position: "nearest"
			        },
			        legend: {
			          position: "bottom",
			          fillStyle: "#FFF",
			          display: false
			        },
			        scales: {
			          yAxes: [{
			            ticks: {
			              fontColor: "rgba(255,255,255,0.4)",
			              fontStyle: "bold",
			              beginAtZero: true,
			              maxTicksLimit: 5,
			              padding: 10
			            },
			            gridLines: {
			              drawTicks: true,
			              drawBorder: false,
			              display: true,
			              color: "rgba(255,255,255,0.1)",
			              zeroLineColor: "transparent"
			            }

			          }],
			          xAxes: [{
			            gridLines: {
			              zeroLineColor: "transparent",
			              display: false,

			            },
			            ticks: {
			              padding: 10,
			              fontColor: "rgba(255,255,255,0.4)",
			              fontStyle: "bold"
			            }
			          }]
			        }
			      }
			    });

			    var cardStatsMiniLineColor = "#fff",
			      cardStatsMiniDotColor = "#fff";

			    ctx = document.getElementById('lineChartExample').getContext("2d");

			    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
			    gradientStroke.addColorStop(0, '#80b6f4');
			    gradientStroke.addColorStop(1, chartColor);

			    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
			    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
			    gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

			    myChart = new Chart(ctx, {
			      type: 'line',
			      responsive: true,
			      data: {
			        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			        datasets: [{
			          label: "Active Users",
			          borderColor: "#f96332",
			          pointBorderColor: "#FFF",
			          pointBackgroundColor: "#f96332",
			          pointBorderWidth: 2,
			          pointHoverRadius: 4,
			          pointHoverBorderWidth: 1,
			          pointRadius: 4,
			          fill: true,
			          backgroundColor: gradientFill,
			          borderWidth: 2,
			          data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
			        }]
			      },
			      options: gradientChartOptionsConfiguration
			    });


			    ctx = document.getElementById('lineChartExampleWithNumbersAndGrid').getContext("2d");

			    gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
			    gradientStroke.addColorStop(0, '#18ce0f');
			    gradientStroke.addColorStop(1, chartColor);

			    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
			    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
			    gradientFill.addColorStop(1, hexToRGB('#18ce0f', 0.4));

			    myChart = new Chart(ctx, {
			      type: 'line',
			      responsive: true,
			      data: {
			        labels: ["12pm,", "3pm", "6pm", "9pm", "12am", "3am", "6am", "9am"],
			        datasets: [{
			          label: "Email Stats",
			          borderColor: "#18ce0f",
			          pointBorderColor: "#FFF",
			          pointBackgroundColor: "#18ce0f",
			          pointBorderWidth: 2,
			          pointHoverRadius: 4,
			          pointHoverBorderWidth: 1,
			          pointRadius: 4,
			          fill: true,
			          backgroundColor: gradientFill,
			          borderWidth: 2,
			          data: [40, 500, 650, 700, 1200, 1250, 1300, 1900]
			        }]
			      },
			      options: gradientChartOptionsConfigurationWithNumbersAndGrid
			    });

			    var e = document.getElementById("barChartSimpleGradientsNumbers").getContext("2d");

			    gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
			    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
			    gradientFill.addColorStop(1, hexToRGB('#2CA8FF', 0.6));


			    


			    var a = {
			      type: "bar",
			      data: {
			        labels: ["campaign 1", "campaign 2", "campaign 3", "campaign 4"],
			        datasets: [{
			          label: "Active Countries",
			          backgroundColor: gradientFill,
			          borderColor: "#2CA8FF",
			          pointBorderColor: "#FFF",
			          pointBackgroundColor: "#2CA8FF",
			          pointBorderWidth: 2,
			          pointHoverRadius: 1,
			          pointHoverBorderWidth: 1,
			          pointRadius: 0,
			          fill: true,
			          borderWidth: 1,
			          data: chart_1_data
			        }]
			      },
			      options: {
			        maintainAspectRatio: false,
			        legend: {
			          display: false
			        },
			        tooltips: {
			          bodySpacing: 4,
			          mode: "nearest",
			          intersect: 0,
			          position: "nearest",
			          xPadding: 10,
			          yPadding: 10,
			          caretPadding: 10
			        },
			        responsive: 1,
			        scales: {
			          yAxes: [{
			            gridLines: 0,
			            gridLines: {
			              zeroLineColor: "transparent",
			              drawBorder: false
			            }
			          }],
			          xAxes: [{
			            display: 0,
			            gridLines: 0,
			            ticks: {
			              display: false
			            },
			            gridLines: {
			              zeroLineColor: "transparent",
			              drawTicks: false,
			              display: false,
			              drawBorder: false
			            }
			          }]
			        },
			        layout: {
			          padding: {
			            left: 0,
			            right: 0,
			            top: 15,
			            bottom: 15
			          }
			        }
			      }
			    };

			    var viewsChart = new Chart(e, a);
			  },

			  showNotification: function(from, align) {
			    color = 'primary';

			    $.notify({
			      icon: "now-ui-icons ui-1_bell-53",
			      message: "Welcome to <b>Now Ui Dashboard</b> - a beautiful freebie for every web developer."

			    }, {
			      type: color,
			      timer: 8000,
			      placement: {
			        from: from,
			        align: align
			      }
			    });
			  }

			};




		

			demo.initDashboardPageCharts();

		}) //end /data-pop
	} //end if


	var i = 1
	var name = $('input[name="campaign_name"]').val()
	var dog = $('input[name="dog"]').val()
	var beer = $('input[name="beer"]').val()

	function iterate_through_form(){


		i++

		var current_div = '.selector > div:nth-child(' + i + ')'

		$(current_div).removeClass('hidden')
		$('.selector > div').not(current_div).addClass('hidden')


		if (i > $('.selector > div').length){
			$('.continue_in_form').addClass('hidden')
			$('.back_in_form').addClass('hidden')
			$('.create_ad').removeClass('hidden')

			$('.ad_summary').removeClass('hidden')
			console.log(name + " " + dog + " " + beer)
		}

		if (i > 1){
			$('.back_in_form').prop( "disabled", false );
		}

		
		return i, name, dog, beer
	}

	function back_in_form(){


		i -= 1

		if (i == 1) {
			$('.back_in_form').addClass('hidden')
		}


		var current_div = '.selector > div:nth-child(' + i + ')'

		$(current_div).removeClass('hidden')
		$('.selector > div').not(current_div).addClass('hidden')


		if (i > $('.selector > div').length){
			$('.continue_in_form').addClass('hidden')
			$('.create_ad').removeClass('hidden')
			console.log(name + " " + dog + " " + beer)
		}

		return i



	}



	$('.continue_in_form').click(function(ev){
		ev.preventDefault()

		iterate_through_form()

	})

	$('.back_in_form').click(function(ev){
		ev.preventDefault()

		back_in_form()
	})

}) // end document.ready










