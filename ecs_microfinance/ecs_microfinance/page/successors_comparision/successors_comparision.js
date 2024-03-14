frappe.pages['successors-comparision'].on_page_load = function(wrapper) {
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
		.weight{
			font-weight:bold;
		}
		.last_year{
			color: green;
		}
		.this-year{
			color:blue;
		}
		`)
        .appendTo($('head'));
	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Successors Comparision',
		single_column: true
	});

	const urlParams = new URLSearchParams(window.location.search);
	const f_successor = urlParams.get('f_employee');
	const s_successor = urlParams.get('s_employee');
	const q_designation = urlParams.get('designation');
	let $btn = page.set_primary_action('Comparision', () => create_new())
	// let designation = page.add_field({
	// 	label: 'Designation',
	// 	fieldtype: 'Link',
	// 	fieldname: 'designation',
	// 	options: "Designation",
	// 	default: q_designation,
	// 	change() {
	// 	}
	// });
	let f_employee = page.add_field({
		label: 'First Successor',
		fieldtype: 'Link',
		fieldname: 'f_employee',
		options: "Employee",
		default: f_successor,

		// get_query:
		// 	function(){ return {'filters': [['designation','=', designation.get_value()]]}},
		change() {
			// console.log(f_employee.get_value());
		}
	});

	

	let s_employee = page.add_field({
		label: 'Second Successor',
		fieldtype: 'Link',
		fieldname: 's_employee',
		options: "Employee",
		default: s_successor,

		// get_query:
		// 	function(){ return {'filters': [['designation','=', designation.get_value()]]}},
		change() {
			// console.log(s_employee.get_value());
		}
	});
	function create_new (){
		frappe.call({
			method:"ecs_microfinance.ecs_microfinance.page.successors_comparision.successors_comparision.get_designation",
			args:{
				f_employee: f_employee.get_value(),
				s_employee: s_employee.get_value(),
			},
			freeze:true,
			callback: function(r){
				console.log(r.message )
				console.log(r.message.goals_1.length)
				$('table').remove()
				$(page.main).append(`
		<table class="table">
			<tbody >
				<tr>
					<td colspan="5">Successors Comparision</td>
				</tr>
				<tr>
					<td colspan="1" >Job title nominated to  الوظيفة المرشحين لها  </td>
					<td colspan="4"> ${q_designation}</td>
				</tr>
				
				<tr>
					<td  colspan="1" >Comparision criteria					</td>
					<td colspan="2" style="border-right: none;"> 	 </td>
					<td colspan="2" style="border-right: none; border-left: none;">	 </td>
				</tr>
			</tbody>
		</table>
	`)
				emp_details= `
					<tr>
						<td  >اسم الموظف Employee Name</td>
						<td colspan="2"> ${r.message.f_employee[4][0].employee_name}	 </td>
						<td colspan="2">  ${r.message.s_employee[4][0].employee_name}	 </td>
					</tr>
					<tr>
						<td  >الوظيفة الحالية Current Job title</td>
						<td colspan="2"> ${r.message.f_employee[4][0].designation}	 </td>
						<td colspan="2">  ${r.message.s_employee[4][0].designation}	 </td>
					</tr>
					<tr>
						<td  >الوحدة Branch</td>
						<td colspan="2">  ${r.message.f_employee[4][0].branch}	 </td>
						<td colspan="2">   ${r.message.s_employee[4][0].branch}	 </td>
					</tr>
					<tr>
						<td  >الإدارة Department</td>
						<td colspan="2">  ${r.message.f_employee[4][0].department}	 </td>
						<td colspan="2">   ${r.message.s_employee[4][0].department}	 </td>
					</tr>
					<tr>
						<td  >تاريخ التعيين Hiring date</td>
						<td colspan="2">  ${r.message.f_employee[4][0].date_of_joining}	 </td>
						<td colspan="2">   ${r.message.s_employee[4][0].date_of_joining}	 </td>
					</tr>
				`
				$('tbody').append(emp_details)
				let length_row = r.message.goals_1.length >  r.message.goals_2.length? r.message.goals_1.length :r.message.goals_2.length
				console.log("wael ", length_row)
				const rowspan = `
				<tr>
					<tr>
						<td  colspan="1" class="last_year weight" >Performance appraisal  Year  ${new Date().getFullYear() - 1}</td>
						<td class=" weight"> ${(parseFloat(r.message.f_employee[5][0].kpi_weight) + parseFloat(r.message.f_employee[5][0].competencies_weight)).toFixed(2)						}% </td>
						<td class="last_year weight"> ${parseFloat(Number(r.message.f_employee[5][0].kpi_total_weight).toFixed(2)) + parseFloat(Number(r.message.f_employee[5][0].competencies_total_weight).toFixed(2))}% </td>
						<td class=" weight"> ${(parseFloat(r.message.s_employee[5][0].kpi_weight) + parseFloat(r.message.s_employee[5][0].competencies_weight)).toFixed(2)						}%</td>
						<td class="last_year weight"> ${parseFloat(Number(r.message.s_employee[5][0].kpi_total_weight).toFixed(2)) + parseFloat(Number(r.message.s_employee[5][0].competencies_total_weight).toFixed(2))}%</td>
					</tr>
					<tr>
						<td  colspan="1"  class="last_year weight">Total score of achieved  KPIs Year  ${new Date().getFullYear() - 1}</td>
						<td class=" weight"> 	${parseFloat(Number(r.message.f_employee[5][0].kpi_weight)).toFixed(2)}% </td>
						<td class="last_year weight"> 	${parseFloat(Number(r.message.f_employee[5][0].kpi_total_weight)).toFixed(2)}% </td>
						<td class=" weight"> 	${parseFloat(Number(r.message.s_employee[5][0].kpi_weight)).toFixed(2)}% </td>
						<td class="last_year weight" >	${parseFloat(Number(r.message.s_employee[5][0].kpi_total_weight)).toFixed(2)}% </td>
					</tr>
					<tr>
						<td  colspan="1" class="last_year weight" >Total score of achieved  competencies  ${new Date().getFullYear() - 1}</td>
						<td class=" weight"> 	${parseFloat(Number(r.message.f_employee[5][0].competencies_weight)).toFixed(2)}% </td>
						<td class="last_year weight"> 	${parseFloat(Number(r.message.f_employee[5][0].competencies_total_weight)).toFixed(2)}% </td>
						<td class=" weight">	${parseFloat(Number(r.message.s_employee[5][0].competencies_weight)).toFixed(2)}% </td>
						<td class="last_year weight">	${parseFloat(Number(r.message.s_employee[5][0].competencies_total_weight)).toFixed(2)}% </td>
					</tr>
					<td  class="this-year weight" colspan="1" >Performance appraisal  Year ${new Date().getFullYear()}</td>
					<td class="this-year weight" colspan="2"> 	${parseFloat(Number(r.message.f_employee[3][0].kpi_total_weight).toFixed(2)) + parseFloat(Number(r.message.f_employee[3][0].competencies_total_weight).toFixed(2))}% </td>
					<td  class="this-year weight" colspan="2">	${parseFloat(Number(r.message.s_employee[3][0].kpi_total_weight).toFixed(2)) + parseFloat(Number(r.message.s_employee[3][0].competencies_total_weight).toFixed(2))}% </td>
				</tr>
				<td class="this-year weight" rowspan="${length_row + 1}"> Total score of achieved KPIs Year ${new Date().getFullYear()}</td>`
				const total_achieve_row = `<tr>
								${rowspan}
							<td class=" weight" colspan="1" class="total_achieve_1"> ${Number(r.message.f_employee[3][0].kpi_weight).toFixed(2)}% </td>
							<td class="this-year weight" colspan="1" class="total_achieve_1"> ${Number(r.message.f_employee[3][0].kpi_total_weight).toFixed(2)}% </td>
							<td class=" weight" colspan="1" class="total_achieve_2">	${Number(r.message.s_employee[3][0].kpi_weight).toFixed(2)}%  </td>
							<td class="this-year weight" colspan="1" class="total_achieve_2">	${Number(r.message.s_employee[3][0].kpi_total_weight).toFixed(2)}%  </td>
							`
				$('tbody').append(total_achieve_row)
				let achieve_score = 0
				let achieve_score_2 = 0
				for (const key in r.message.goals_1) {
					if (r.message.goals_1.hasOwnProperty(key)) {
						const value = r.message.goals_1[key];
						const achieve_weight_1 = r.message.f_employee[0].hasOwnProperty(Number(key)+1)? r.message.f_employee[0][Number(key)+1].achieve_weight  / r.message.f_employee[2] : 0
						const achieve_weight_2 = r.message.s_employee[0].hasOwnProperty(Number(key)+1)? r.message.s_employee[0][Number(key)+1].achieve_weight  / r.message.s_employee[2] : 0
						achieve_score += achieve_weight_1
						achieve_score_2 += achieve_weight_2
						// console.log(r.message.f_employee[0][key+1].kpi, "       h ", key)
						const row = `<tr class = 'kpi-${key}'>
										<td class ='text-right'> 	${value.key_result_area}</td>
										<td  class="this-year weight" >${achieve_weight_1}% 	</td>
										
									</tr>
							`
						$('tbody').append(row)
					}
				  }
				  for (const key in r.message.goals_2) {
					if (r.message.goals_2.hasOwnProperty(key)) {
						console.log("fdsffdfdf")
						const value = r.message.goals_2[key];
						const achieve_weight_1 = r.message.f_employee[0].hasOwnProperty(Number(key)+1)? r.message.f_employee[0][Number(key)+1].achieve_weight  / r.message.f_employee[2] : 0
						const achieve_weight_2 = r.message.s_employee[0].hasOwnProperty(Number(key)+1)? r.message.s_employee[0][Number(key)+1].achieve_weight  / r.message.s_employee[2] : 0
						achieve_score += achieve_weight_1
						achieve_score_2 += achieve_weight_2
						// console.log(r.message.f_employee[0][key+1].kpi, "       h ", key)
						const row = `
										<td class ='text-right'> 	${value.key_result_area}</td>
										<td >${achieve_weight_1}% 	</td>
							`
						$(`.kpi-${key}`).append(row)
					}
				  }
				achieve_score /= r.message.goals_1.length
				achieve_score_2 /= r.message.goals_1.length
				// $('.total_achieve_1').append(`${achieve_score}%`)
				// $('.total_achieve_2').append(`${achieve_score_2}%`)
				length_row = r.message.competencies_template_1.length >  r.message.competencies_template_2.length? r.message.competencies_template_1.length :r.message.competencies_template_2.length
				const rowspan_2 = `<td rowspan="${length_row + 1}"> Total score of achieved Competencies Year ${new Date().getFullYear()}</td>`
				const total_competencies_row = `<tr>
						${rowspan_2}
						<td  > ${Number(r.message.f_employee[3][0].competencies_weight).toFixed(2)}%	 </td>
						<td > ${Number(r.message.f_employee[3][0].competencies_total_weight).toFixed(2)}%	 </td>
						<td  >	${Number(r.message.s_employee[3][0].competencies_weight).toFixed(2)}%</td>
						<td  >	${Number(r.message.s_employee[3][0].competencies_total_weight).toFixed(2)}%</td>
					`
				$('tbody').append(total_competencies_row)
				achieve_score = 0
				achieve_score_2 = 0
				for (const key in r.message.competencies_template_1) {
					if (r.message.competencies_template_1.hasOwnProperty(key)) {
						const value = r.message.competencies_template_1[key];
						const achieve_weight_1 = r.message.f_employee[1].hasOwnProperty(Number(key)+1)? r.message.f_employee[1][Number(key)+1].achieve_weight  / r.message.f_employee[2] : 0
						const achieve_weight_2 = r.message.s_employee[1].hasOwnProperty(Number(key)+1)? r.message.s_employee[1][Number(key)+1].achieve_weight  / r.message.s_employee[2] : 0
						achieve_score += achieve_weight_1
						achieve_score_2 += achieve_weight_2
						// console.log(r.message.f_employee[0][key+1].kpi, "       h ", key)
						const row = `<tr class = 'competencies-${key}'>
										<td class ='text-right'> ${value.competencies}</td>
										<td >${achieve_weight_1}% 	</td>
									</tr>
							`
						$('tbody').append(row)
					}
				  }

				for (const key in r.message.competencies_template_2) {
					if (r.message.competencies_template_2.hasOwnProperty(key)) {
						const value = r.message.competencies_template_2[key];
						const achieve_weight_1 = r.message.f_employee[1].hasOwnProperty(Number(key)+1)? r.message.f_employee[1][Number(key)+1].achieve_weight  / r.message.f_employee[2] : 0
						const achieve_weight_2 = r.message.s_employee[1].hasOwnProperty(Number(key)+1)? r.message.s_employee[1][Number(key)+1].achieve_weight  / r.message.s_employee[2] : 0
						achieve_score += achieve_weight_1
						achieve_score_2 += achieve_weight_2
						// console.log(r.message.f_employee[0][key+1].kpi, "       h ", key)
						const row = `
										<td class ='text-right'> ${value.competencies}</td>
										<td >${achieve_weight_2}% 	</td>
									
							`
						$(`.competencies-${key}`).append(row)
					}
				  }
				achieve_score /= r.message.competencies_template_1.length
				achieve_score_2 /= r.message.competencies_template_1.length

				length_row = r.message.evaluation_1.length >  r.message.evaluation_2.length? r.message.evaluation_1.length :r.message.evaluation_2.length
				const assosser_evaluation = `<tr>
						<td> Assessor Evaluation </td>
						<td colspan="2" style="border-right: none;"> 	 </td>
						<td colspan="2" style="border-right: none; border-left: none;">	 </td>
					`
				$('tbody').append(assosser_evaluation)

				const rowspan_3 = `<td rowspan="${length_row + 1}"> Total score of achieved Competencies}</td>`
				const total_competencies_assosser_evaluation = `<tr>
					${rowspan_3}
					<td colspan="2"> ${Number(r.message.f_employee[8][0].total_achieved_weight).toFixed(2)}%	 </td>
					<td colspan="2"> ${Number(r.message.s_employee[8][0].total_achieved_weight).toFixed(2)}%	 </td>

				`
				$('tbody').append(total_competencies_assosser_evaluation)

				for (const key in r.message.evaluation_1) {
					if (r.message.evaluation_1.hasOwnProperty(key)) {
						const value = r.message.evaluation_1[key];
						const achieve_weight_1 = r.message.f_employee[6].hasOwnProperty(Number(key)+1)? r.message.f_employee[6][Number(key)+1].percentage  / r.message.f_employee[7] : 0
						const achieve_weight_2 = r.message.s_employee[6].hasOwnProperty(Number(key)+1)? r.message.s_employee[6][Number(key)+1].percentage  / r.message.s_employee[7] : 0
						achieve_score += achieve_weight_1
						achieve_score_2 += achieve_weight_2
						// console.log(r.message.f_employee[0][key+1].kpi, "       h ", key)
						const row = `<tr class = 'assessor-${key}'>
										<td class ='text-right'> ${value.competencies}</td>
										<td >${achieve_weight_1}% 	</td>
									</tr>
							`
						$('tbody').append(row)
					}
				  }

				for (const key in r.message.evaluation_2) {
					if (r.message.evaluation_2.hasOwnProperty(key)) {
						const value = r.message.evaluation_2[key];
						const achieve_weight_1 = r.message.f_employee[6].hasOwnProperty(Number(key)+1)? r.message.f_employee[6][Number(key)+1].percentage  / r.message.f_employee[7] : 0
						const achieve_weight_2 = r.message.s_employee[6].hasOwnProperty(Number(key)+1)? r.message.s_employee[6][Number(key)+1].percentage  / r.message.s_employee[7] : 0
						achieve_score += achieve_weight_1
						achieve_score_2 += achieve_weight_2
						// console.log(r.message.f_employee[0][key+1].kpi, "       h ", key)
						const row = `
										<td class ='text-right'> ${value.competencies}</td>
										<td >${achieve_weight_2}% 	</td>
									
							`
						$(`.assessor-${key}`).append(row)
					}
				  }
				achieve_score /= r.message.competencies_template_1.length
				achieve_score_2 /= r.message.competencies_template_1.length
				$('.total_competencies_1').append(`${achieve_score}%`)
				$('.total_competencies_2').append(`${achieve_score_2}%`)
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

}
