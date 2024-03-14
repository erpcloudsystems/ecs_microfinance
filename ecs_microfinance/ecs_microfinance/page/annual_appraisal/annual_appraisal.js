frappe.pages['annual-appraisal'].on_page_load = function(wrapper) {
	$('<style>')
        .prop('type', 'text/css')
        .html(`.page-form { justify-content: space-around; }
		.table{
			margin:1rem 0;
			width: 100%!important;
		}
		.table, td,tr{
			border: 2px solid black;
			border-collapse:collapse;
			text-align:center;
			
		}
		`)
        .appendTo($('head'));
	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Annual Appraisal',
		single_column: true
	});
	
	let $btn = page.set_primary_action('Get Report', () => create_new())
	let designation = page.add_field({
		label: 'Designation',
		fieldtype: 'Link',
		fieldname: 'designation',
		options: "Designation",
		change() {
			// console.log(designation.get_value());
		}
	});

	let employee = page.add_field({
		label: 'Employee',
		fieldtype: 'Link',
		fieldname: 'employee',
		options: "Employee",
		get_query:
			function(){ return {'filters': [['designation','=', designation.get_value()]]}},
		change() {
			// console.log(employee.get_value());
		}
	});
	let selected_date = page.add_field({
		label: 'Select Date',
		fieldtype: 'Date',
		fieldname: 'selected_date',
		change() {
			// console.log(s_employee.get_value());
		}
	});

	function create_new (){
		console.log(selected_date.get_value())
		
		if (designation.get_value() == ""){
			frappe.throw("Please Select Designation")
		}
		if (employee.get_value() == ""){
			frappe.throw("Please Select Employee")
		}
		if (!selected_date.get_value()){
			frappe.throw("Please Select Date")
		}
		frappe.call({
			method:"ecs_microfinance.ecs_microfinance.page.annual_appraisal.annual_appraisal.get_designation",
			args:{
				designation: designation.get_value(),
				employee: employee.get_value(),
				selected_date: selected_date.get_value(),
			},
			freeze:true,
			callback: function(r){
				console.log(page.main)
				$('table').remove()
				$('.head-table').remove()
				$('.weight').remove()
				$(page.main).append(returned_emp_details_table())
				const emp_details = `
					<tr>
						<td> Employee Name </td>
						<td> ${r.message[4][0].employee_name}</td>
						<td> الادارة</td>
						<td> ${r.message[4][0].department}</td>
					</tr>
					<tr>
						<td> Designation </td>
						<td> ${r.message[4][0].designation} </td>
						<td> Assessor </td>
						<td>  </td>
					</tr>
					<tr>
						<td> Date of joining </td>
						<td> ${r.message[4][0].date_of_joining} </td>
						<td> Duration </td>
						<td>  </td>
					</tr>
				`
				$('.emp-details').append(emp_details)
				$(page.main).append(`
					<div class="d-flex " style="justify-content: space-between;">
					${returned_weight_table()}
					${returned_total_weight_table()}
					</div>
				`)
				$(page.main).append()
				$(page.main).append(returned_goal_table())
				console.log( r.message[3])
				const kpi_weight = `
									
									<td > KPI Weight</td>
									<td > ${r.message[3][0].kpi_weight}</td>
							`
						$('.kpi-weight').append(kpi_weight)
				const competencies_weight = `
						<td >Competencies Weight</td>
						<td > ${r.message[3][0].competencies_weight} </td>
				`
				$('.competencies-weight').append(competencies_weight)
				let kpi_weight_total = 0
				let achieve_score = 0
				let cnt = 0 
				for (const key in r.message[0]) {
					if (r.message[0].hasOwnProperty(key)) {
					  	const value = r.message[0][key];
					  	// Do something with each key-value pair
						achieve_score += value.achieve_weight / r.message[2]
						kpi_weight_total += value.per_weightage / r.message[2]
						cnt +=1
						const row = `<tr>
									<td  colspan="1" >${value.kpi}</td>
									<td > ${value.per_weightage / r.message[2] }</td>
									<td > ${value.target / r.message[2] }</td>
									<td >	${value.achieved / r.message[2]} </td>
									<td >	${value.achieve_weight / r.message[2]} </td>
								</tr>
							`
						$('.goal').append(row)
					}
				  }
				  const last_kpi = `<tr>
									<td  colspan="1" >Total</td>
									<td > ${kpi_weight_total}</td>
									<td > </td>
									<td >	</td>
									<td >	${achieve_score / cnt} </td>
								</tr>
							`
					$('.goal').append(last_kpi)
				$(page.main).append(returned_competencies_table())
				
				const total_kpi_weight = `
									
									<td > Total KPI Percentage</td>
									<td > ${r.message[3][0].kpi_total_weight} %</td>
							`
						$('.total-kpi-weight').append(total_kpi_weight)
				const total_competencies_weight = `
						<td >Total Competencies Percentage</td>
						<td > ${r.message[3][0].competencies_total_weight} % </td>
				`
				$('.total-competencies-weight').append(total_competencies_weight)
				for (const key in r.message[1]) {
					if (r.message[1].hasOwnProperty(key)) {
					  	const value = r.message[1][key];
					  	// Do something with each key-value pair
						const row = `<tr>
									<td  colspan="1" >${value.competencies}</td>
									<td >${value.target / r.message[2]} </td>
									<td >	${value.manager_score1 / r.message[2]} </td>
									<td > ${value.achieve_weight / r.message[2]}</td>
								</tr>
							`
						$('.competencies').append(row)
					}
				  }
			}
		})
		
	}

	function returned_goal_table(){
		
		return `
		<h2 class="head-table"> ${frappe._('Goals')} </h2>
		<table class="table">
			<tbody class="goal">
				<tr>
					<td > ${frappe._('KPI')} </td>
					<td> 	${frappe._('Weight')} </td>
					<td> 	${frappe._('Target')} </td>
					<td>	${frappe._('Achieved')} </td>
					<td>	${frappe._('Achieved Prcentage')} </td>
				</tr>
				
			</tbody>
		</table>
	`
	}
	function returned_competencies_table(){
		
		return `
		<h2 class="head-table"> ${frappe._('Competencies')} </h2>
		<table class="table">
			<tbody class="competencies">
				<tr>
					<td > 
					${frappe._('Competencies')} </td>
					<td> 	${frappe._('Target')} </td>
					<td>	${frappe._('Manager Score')} </td>
					<td>	 ${frappe._('Manager Score Weight')}</td>
				</tr>
				
			</tbody>
		</table>
	`
	}
	function returned_weight_table(){
		
		return `
		<table class="table" style='width:30% !important;'>
			<tbody class="weight">
				<tr class="kpi-weight">
				</tr>
				<tr  class="competencies-weight">

				</tr>
			</tbody>
		</table>
	`
	}
	function returned_total_weight_table(){
		
		return `
		<table class="table" style='width:30% !important;'>
			<tbody class="weight">
				<tr class="total-kpi-weight">
				</tr>
				<tr  class="total-competencies-weight">

				</tr>
			</tbody>
		</table>
	`
	}
	function returned_emp_details_table(){
		
		return `
		<table class="table">
			<tbody class="emp-details">

			</tbody>
		</table>
	`
	}

}


