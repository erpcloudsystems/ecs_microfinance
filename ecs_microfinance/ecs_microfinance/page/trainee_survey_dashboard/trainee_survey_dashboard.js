
function check_role(){
	let role_value = false
	if(frappe.user.has_role("HR Manager"))
		role_value = true
	return role_value
}

frappe.pages['trainee-survey-dashboard'].on_page_load = async function(wrapper) {
	current_user = frappe.session.user	
	await  frappe.call({
		method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_employee',
		args: {
		  userId: current_user, 
		  role:check_role()
		},
		callback: async function(r) {
		  // Handle the response here
		
			await new MyPage(wrapper, r.message[0].name)
		}
	  });
	

}


MyPage = Class.extend({
	init:  function (wrapper, name){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Trainee Survey Dashboard',
			single_column: true
		});


		this.make(name)
	},
	make: async function(name){

		let me = this.page;

		id = undefined
		let body = frappe.test_app_page.body
		let model = frappe.test_app_page.model
		let model2 = frappe.test_app_page.model2
		await $(frappe.render_template(body,this)).appendTo(this.page.main)
		await $(frappe.render_template(model,this)).appendTo(this.page.main)
		await $(frappe.render_template(model2,this)).appendTo(this.page.main)
		await this.get_total_hours_training_events(name)
		await this.get_total_hours_completed_training_events(name)
		x = await this.get_training_events(name)
		y = await this.get_completed_training_events(name)
		this.dynamic_progress_blue(y / x)
		this.dynamic_progress_yellow()
		check_role() ? this.add_input_training_events_for_survey(me) : ''
		this.add_input_training_events_for_assessment(name, me)
		this.add_input_training_events_for_assignments(name, me)
		this.add_input_training_events_for_get_survey_link(me)


	},
	add_input_training_events_for_survey: function(me){
			const self = this;

			const field = me.add_field({
				label: 'Training Events',
				fieldtype: 'Link',
				fieldname: 'training_events',
				options:'Training Event',
				change(){
					self.get_feedback_survey(field.get_value())
				}
			});
			const training_event = document.querySelector('[data-fieldname="training_events"]');
			input = training_event.querySelector('input')

			input.name= "training_event"
			$('#input-survey').append(training_event)
			this.get_feedback_survey(input.value)
		
		}
	,
	add_input_training_events_for_assessment: async function(name, me){
		const self = this
		const field = await me.add_field({
			label: 'Training Events',
			fieldtype: 'Link',
			fieldname: 'training_events_assesment',
			options:'Training Event',
			change() {
				self.get_assesment(name, field.get_value());
			}
		});
		const training_event =  document.querySelector('[data-fieldname="training_events_assesment"]');
		input =  training_event.querySelector('input')
		input.name= "training_events_assesment"
		training_event.classList.remove('col-md-2')
		training_event.classList.add('p-0')

		$('#input-assessment').append(training_event)
		$('#add-assesment').on('click', async function() {
			console.log( field.get_value())
			frappe.call({
				method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.create_assesment',
				args: {
					employee: name,
					training_events: field.get_value()
				},
				callback: async function(r) {
				  // Handle the response here
					const Doctype = "Upload Assessment" 
					self.upload_attached(name, r.message, Doctype )
				}
			  });
		});
	},
	add_input_training_events_for_get_survey_link: async function( me){
		self = this;
		const field = await me.add_field({
			label: 'Training Events',
			fieldtype: 'Link',
			fieldname: 'training_events_survey_link',
			options:'Training Event',
			change(){
				self.get_survey_link(field.get_value())
			}
		});
		const training_event =   document.querySelector('[data-fieldname="training_events_survey_link"]');
		input =  training_event.querySelector('input')
		input.name= "training_events_survey_link"
		training_event.classList.remove('col-md-2')
		training_event.classList.add('p-0')

		$('#input-survey-link').append(training_event)

		
	},
	get_survey_link:function (training_events){
		frappe.call({
			method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_survey_link_for_training_event',
			args: {
				training_events: training_events
			},
			callback: async function(r) {
			  // Handle the response here
				x = r.message.length	
				console.log(r.message)
				$("#links-survey li").remove()
				if (r.message[0].custom_trainee_survey_link)
				{
						$("#links-survey").append(
							`<li> <a href="${r.message[0].custom_trainee_survey_link}">${r.message[0].name}</a> </li>`
						)
				}
				// self.upload_attached(name, r.message )
			}
		  });
	},
	add_input_training_events_for_assignments: async function(name, me){
		const self = this; 

		const field = await me.add_field({
			label: 'Training Events',
			fieldtype: 'Link',
			fieldname: 'training_events_assignment',
			options:'Training Event',
			change(){
				self.get_assignment_result(name, field.get_value())
			}
		});
		const training_event =  document.querySelector('[data-fieldname="training_events_assignment"]');
		input =  training_event.querySelector('input')
		training_event.classList.remove('col-md-2')
		training_event.classList.add('p-0')
		input.name= "training_events_assignment"
		$('#input-assignment').append(training_event)

		
			$('#add_image').on('click', async function() {
				frappe.call({
					method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.create_assignment',
					args: {
						employee: name,
						training_events: field.get_value()
					},
					callback: async function(r) {
					  // Handle the response here
						const Doctype = "Upload Assignment"	
						self.upload_attached(name, r.message, Doctype)
					}
				  });
			});
		
	},

	get_assignment_result: function(name, training_event ){
		frappe.call({
			method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_assements_for_employee',
			args: {
				employee: name,
				training_events: training_event, 
				role:check_role()
			},
			callback: async function(r) {
			  // Handle the response here
			
				$('.assignment-res tr').remove()
				$('.assignment-head tr').remove()
				if(r.message.length > 0){
					$('.assignment-head').append(
						`
							<tr>
								<th scope="col">Name</th>
								<th scope="col">Score</th>
							</tr>
						`
					)
				}
				r.message.forEach((assess)=>{
					$('.assignment-res').append(
						`
						<tr>
							<th scope="row">${assess.employee_name}</th>
							<td>${assess.score1}</td>
						</tr>
						`
					)
				})
			}
		  });
	},
	upload_attached :function(employee, name, Doctype){
		const input_file = document.querySelector('.input_file').files[0] || document.querySelector('.input_file_assesment').files[0];

		if (input_file) {
		const form_data = new FormData();
		form_data.append('file', input_file);
		form_data.append('doctype', Doctype);
		form_data.append('docname', name );

		fetch('/api/method/upload_file', {
			method: 'POST',
			headers: {
			'Accept': 'application/json',
			'X-Frappe-CSRF-Token': frappe.csrf_token
			},
			body: form_data
		})
		.then(response => {
			if (response.ok) {
				document.querySelector('.input_file').value = null;
				document.querySelector('.input_file_assesment').value = null;
				frappe.show_alert({
					message:__('Image Has Been Uploaded Successfully'),
					indicator:'green'
				}, 5);
			} else {
				console.log(response.statusText)
			throw new Error('Network response was not ok.');
			}
		})
		.then(data => {
			console.log('Upload successful:', data);
			
		})
		.catch(error => {
			console.error('Upload error:', error);
		});
		}

	},
	get_assesment:function(name, training_event){
		frappe.call({
			method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_assements_for_employee',
			args: {
				employee: name,
				training_events: training_event, 
				role:check_role()
			},
			callback: async function(r) {
			  // Handle the response here
			
				$('.assesment-res tr').remove()
				$('.assesment-head tr').remove()
				if(r.message.length > 0){
					$('.assesment-head').append(
						`
							<tr>
								<th scope="col">Name</th>
								<th scope="col">Score</th>
							</tr>
						`
					)
				}
				r.message.forEach((assess)=>{
					$('.assesment-res').append(
						`
						<tr>
							<th scope="row">${assess.employee_name}</th>
							<td>${assess.score1}</td>
						</tr>
						`
					)
				})
			}
		  });
	}
	,
	dynamic_progress_blue: async function(number_data){
		const progressBar = document.querySelector(".progress .progress-bar");
        const progressValue = document.querySelector(".blue .progress-value");
		progressValue.innerHTML = (number_data * 100).toFixed(2)+ "%"
		
		const deg = (number_data ) * 360
		const customKeyframesStyle = document.getElementById('customkeyframe');
		let diff_deg = 0
		if (deg > 180){
			diff_deg = deg - 180
			customKeyframesStyle.innerHTML = `
			@keyframes loading-1 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(180deg);
				}
			  }
			  @keyframes loading-2 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(${diff_deg}deg);
				}
			  }
			`
		}
		else{
			customKeyframesStyle.innerHTML = `
			@keyframes loading-1 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(${deg}deg);
				}
			  }
			  @keyframes loading-2 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(0deg);
				}
			  }
			`
		}
		// progressBar.style.transform = `rotate(${(progress / 100) * 180}deg)`;
	},
	dynamic_progress_yellow: function(){
		const progressBar = document.querySelector(".progress .progress-bar");
        const progressValue = document.querySelector(".yellow .progress-value");
		const deg = (Number(progressValue.innerHTML.replace(/%/g, '')) / 100 ) * 360
		const customKeyframesStyle = document.getElementById('keyframeyellow');

		let diff_deg = 0
		if (deg > 180){
			diff_deg = deg - 180
			customKeyframesStyle.innerHTML = `
			@keyframes loading-3 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(180deg);
				}
			  }
			  @keyframes loading-4 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(${diff_deg}deg);
				}
			  }
			`
		}
		else{
			customKeyframesStyle.innerHTML = `
			@keyframes loading-3 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(${deg}deg);
				}
			  }
			  @keyframes loading-4 {
				0% {
				  -webkit-transform: rotate(0deg);
				  transform: rotate(0deg);
				}
				100% {
				  -webkit-transform: rotate(180deg);
				  transform: rotate(0deg);
				}
			  }
			`
		}
		// progressBar.style.transform = `rotate(${(progress / 100) * 180}deg)`;
	}, 
	get_training_events:  async function(name){
		x= 0
		await frappe.call({
			method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_trainnig_event_for_employee',
			args: {
				employee: name,
				role:check_role()
			},
			callback: async function(r) {
			  // Handle the response here
				x = r.message.length	
			$('.total-courses').text(x)
			r.message.forEach(training_event=>{
					$('.training-events').append(

						`
							<li><a href="https://eaf.erpcloud.systems/app/training-event/${training_event.training_events}"> ${training_event.training_events} </a></li>
						`
					)
				})
			}
		  });
		return x 
	},
	get_completed_training_events:  async function(name){
		y = 0
		await frappe.call({
			method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_completed_trainnig_event_for_employee',
			args: {
				employee: name,
				role:check_role()
			},
			callback: async function(r) {
			  // Handle the response here
			  y = r.message[0].num_of_events	
			   $('.courses_completed').text(r.message[0].num_of_events)
			}
		  });
		return y
	},
	get_total_hours_training_events:  async function(name){
		y = 0
		await frappe.call({
			method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_total_hours_trainnig_event_for_employee',
			args: {
				employee: name,
				role:check_role()
			},
			callback: async function(r) {
			  // Handle the response here
			   $('.total_hours').text(r.message[0].total_hour)
			}
		  });
		return y
	},
	get_total_hours_completed_training_events:  async function(name){
		await frappe.call({
			method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_total_hours_completed_trainnig_event_for_employee',
			args: {
				employee: name,
				role:check_role()
			},
			callback: async function(r) {
			  // Handle the response here
			   $('.completed_hours').text(r.message[0].total_hour)
			}
		  });
	},
	get_feedback_survey: function(input_value_of_training){
		// grades.forEach(async grade=>{
			frappe.call({
				method: 'ecs_microfinance.ecs_microfinance.page.trainee_survey_dashboard.trainee_survey_dashboard.get_feedback_survey_data',
				args: {
					filters: input_value_of_training ? input_value_of_training : ""
				},
				callback: async function(r) {
				  // Handle the response here
				  excellent= []
				  very_good= []
				  good= []
				  intermediate= []
				  bad= []
				  r.message.forEach(res=>{
					excellent.push(res.excellent)
					very_good.push(res.very_good)
					good.push(res.good)
					intermediate.push(res.intermediate)
					bad.push(res.bad)
				  })
				new frappe.Chart( "#frost-chart", { // or DOM element
					data: {
					labels: ["درجة معرفة وإلمام المدرب بمواضيع البرنامج التدريبي", "قدرة  المدرب على توصيل المعلومات", "طريقة تنظيم العرض (من حيث الوضوح والكفاية)", "مدى تعاون المتدرب مع المتدربين و الإجابة على الاستفسارات",
						"قدرة المدرب على تحفيز المشاركين على التفاعل","تحقيق محتوى البرنامج التدريبي لتوقعاتك","ملائمة الوسائل التدريبية المستخدمة","تنظيم وسهولة محتوى المادة العلمية",
						"مدى تحقيق أهداف البرنامج التدريبي", "مستوى تنظيم البرنامج التدريبي","ملائمة مدة الزمنية للبرنامج التدريبي  و التوقيت","مدى مساهمة البرنامج التدريبي في تطوير معارفتك ومهاراتك",
						"ما هو تقييمك العام عن مدى فاعلية الدورة التدريبية"
					],
				
					datasets: [
						{
							name: "Excellent", chartType: 'bar',
							values: excellent
						},
						{
							name: "Very Good", chartType: 'bar',
							values: very_good
						},
						{
							name: "Good", chartType: 'bar',
							values: good
						},
						{
							name: "intermediate", chartType: 'bar',
							values: intermediate
						},
						{
							name: "bad", chartType: 'bar',
							values: bad
						}
					],
				
					
				
					},
				
					title: "Traning Events",
					type: 'axis-mixed', // or 'bar', 'line', 'pie', 'percentage'
					height: 300,
					colors: ['#049dff', '#fdba04'],
				
					tooltipOptions: {
						formatTooltipX: d => (d + '').toUpperCase(),
						formatTooltipY: d => d + ' pts',
					}
				  });
				}
			  });
		// })
		
	},
	clearInputs: function () {
		// Get all input elements on the page
		const inputs = document.querySelectorAll('input');
	
		// Loop through the inputs and set their values to empty strings
		inputs.forEach(input => {
			input.value = '';
		});
	}
	
	// Add an event listener to clear inputs when the page finishes loading
});

const row_one = ()=>`
	<div class="row">
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
			<div class="card-header bg-dark text-white">
				<h4 class="text-white"> Progress Overview </h4>
				<div class="row bg-dark text-white mt-0" style="  margin: -1.25rem;">
					<div class=" col-md-2 text-center">
  						<span class="d-block total-courses">-</span>
						<span class = "d-block"> Total Courses </span>
					</div>
					<div class=" col-md-2 text-center">
						<span class="d-block courses_completed">-</span>
						<span class="d-block"> Completed </span>
					</div>
					<div class=" col-md-3 text-center">
						<span class="d-block total_hours">-</span>
						<span class = "d-block"> Training Hours </span>
					</div>
					<div class=" col-md-2 text-center">
						<span class="d-block completed_hours">-</span>
						<span class = "d-block">Completed Hours</span>
					</div>
					<div class=" col-md-3 text-center">
						<span class="d-block">100</span>
						<span class = "d-block"> Assignments </span>
					</div>
				</div>
			</div>
			<div class="card-body">
				<div class="row d-flex justify-content-center mt-100">
						<div>
							<h5 class="font-weight-bold text-center" >Traning plan <br>completion
							</h5>
							<div class="progress blue">
								<span class="progress-left">
									<span class="progress-bar"></span>
								</span>
								<span class="progress-right">
									<span class="progress-bar"></span>
								</span>
								<div class="progress-value">-</div>
							</div>
						</div>
						<div> 
							<h5 class="font-weight-bold text-center" >Assessments <br>Score rate</h5>
							<div class="progress yellow">
								<span class="progress-left">
									<span class="progress-bar"></span>
								</span>
								<span class="progress-right">
									<span class="progress-bar"></span>
								</span>
								<div class="progress-value">50%</div>
							</div>							
						</div>
				</div>
			</div>
		</div>
	</div>
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
			<h4 class="card-header bg-dark text-white">Training Calendar</h4>
			
			<div class="card-body">
				<div class="">
					<h5 class="font-weight-bold">Monthly traning calendar</h5>
					<a href="training-event/view/calendar/Training%20Event" target="_blank">
						<img src="/files/Screenshot 2023-09-21 110026.png" >	
					</a>		
					</div>			
				</div>
				<div class="mt-3">
				<!--
  					<h5 class="font-weight-bold">Next traning</h5>
  					<ul class="">
  						<li>Hi</li>
  						<li>No</li>
  						<li>Yes</li> -->
					</ul>
				</div>
			</div>
		</div>
	</div>
</div>
`

const row_two = ()=>`
<div class="row mt-2">
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
		<h4 class="card-header bg-dark text-white"> Courses </h4>
			
			<div class="card-body">
				<div class="mt-3">
  					<ul class="training-events">

					</ul>
				</div>
			</div>
		</div>
	</div>
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
			<h4 class="card-header bg-dark text-white">Assessment</h4>

			<div class="card-body">
				<div class="mt-3">
					
					<div class="row">
						<div class="col-6 col-md-6 mt-3">
							<div id="input-assessment" class="mb-4"></div>
							<button id="upload-assessment" type="button" class="btn btn-secondary" data-toggle="modal" data-target="#exampleModal2">
								Upload Assessment
							</button>
						</div>
						<div class="col-6 col-md-6 mt-3">
							<h5 class="font-weight-bold">Assessment Score</h5>
							<table class="table table-striped">
								<thead class="assesment-head">
								
								</thead>
								<tbody class="assesment-res">
								
								</tbody>
								</table>
							
						</div>

					</div>
				</div>
			</div>
		</div>
	</div>
</div>
`


const row_three = ()=>`
<div class="row mt-2">
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
			<h4 class="card-header bg-dark text-white">Assignments</h4>
			<div class="card-body row">
				<div class="col-6 col-md-6 mt-3">
					<div id="input-assignment" class="mb-4"></div>
					<button id="upload" type="button" class="btn btn-secondary" data-toggle="modal" data-target="#exampleModal">
						Upload Assignment
					</button>
				
				</div>
				<div class="col-6 col-md-6 mt-3">
					<h5 class="font-weight-bold">Assignment Score</h5>
					<table class="table table-striped">
						<thead class="assignment-head">
						
						</thead>
						<tbody class="assignment-res">
						
						</tbody>
					</table>
					
				</div>
			</div>
		</div>
	</div>
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
		<h4 class="card-header bg-dark text-white"> Job Aid </h4>
			
			<div class="card-body">
				<div class="mt-3">
  					<ul class="">
  						<li>Manuals, Guides, Instructions</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</div>
`

const row_four = ()=>`
<div class="row mt-2">
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
			<h4 class="card-header bg-dark text-white">FAQ</h4>
			<div class="card-body">
				<div class="mt-3">
  					<ul class="">
  						<li>Submitting (upload) </li>

					</ul>
				</div>
			</div>
		</div>
	</div>
	

</div>
`

const row_five=()=>`
<div class="row mt-2">
	<div class="col-12 col-md-12 mt-3">
		<div class="card">
			<h4 class="card-header bg-dark text-white">Feedback (survey) </h4>
			<div class="card-body">
				<div class="mt-3">
					<div id="input-survey"></div>
					<div id="frost-chart" ></div>
				</div>
			</div>
		</div>
	</div>
</div>

`

const row_survey_link=()=>`
<div class="row mt-2">
	<div class="col-12 col-md-6 mt-3">
		<div class="card">
			<h4 class="card-header bg-dark text-white">Survey </h4>
			<div class="card-body">
				<div class="mt-3">
					<div class= "d-flex">
						<div id="input-survey-link"></div>
					</div>
					<div >
						<ul id="links-survey"></ul>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

`
const body = `
<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
  }

  .progress {
	width: 150px;
	height: 150px !important;
	float: left; 
	line-height: 150px;
	background: none;
	margin: 20px;
	box-shadow: none;
	position: relative;
  }
  .progress:after {
	content: "";
	width: 100%;
	height: 100%;
	border-radius: 50%;
	border: 12px solid #fff;
	position: absolute;
	top: 0;
	left: 0;
  }
  .progress>span {
	width: 50%;
	height: 100%;
	overflow: hidden;
	position: absolute;
	top: 0;
	z-index: 1;
  }
  .progress .progress-left {
	left: 0;
  }
  .progress .progress-bar {
	width: 100%;
	height: 100%;
	background: none;
	border-width: 12px;
	border-style: solid;
	position: absolute;
	top: 0;
  }
  .progress .progress-left .progress-bar {
	left: 100%;
	border-top-right-radius: 80px;
	border-bottom-right-radius: 80px;
	border-left: 0;
	-webkit-transform-origin: center left;
	transform-origin: center left;
  }
  .progress .progress-right {
	right: 0;
  }
  .progress .progress-right .progress-bar {
	left: -100%;
	border-top-left-radius: 80px;
	border-bottom-left-radius: 80px;
	border-right: 0;
	-webkit-transform-origin: center right;
	transform-origin: center right;
	animation: loading-1 1.8s linear forwards;
  }
  .progress .progress-value {
	width: 90%;
	height: 90%;
	border-radius: 50%;
	background: #000;
	font-size: 24px;
	color: #fff;
	line-height: 135px;
	text-align: center;
	position: absolute;
	top: 5%;
	left: 5%;
  }
  .progress.blue .progress-bar {
	border-color: #049dff;
  }
  .progress.blue .progress-left .progress-bar {
	animation: loading-2 1.5s linear forwards 1.8s;
  }
  .progress.yellow .progress-bar {
	border-color: #fdba04;
  }
  .progress.yellow .progress-right .progress-bar {
	animation: loading-3 1.8s linear forwards;
  }
  .progress.yellow .progress-left .progress-bar {
	animation: loading-4 1.8s linear forwards;
  }
  

</>
</style>
<style id="customkeyframe">
	
</style>
<style id="keyframeyellow">

</style>

${row_one() +
	row_two()+
	row_three()+
	row_four()+
	row_survey_link()
}
${frappe.user.has_role("HR Manager") ? row_five() : ""}

`

model =`
<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Upload File</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
	   <input type="file" class="input_file" name="file">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" id="add_image" class="btn btn-primary">Upload</button>
      </div>
    </div>
  </div>
</div>
` 

model2 =`
<div class="modal fade" id="exampleModal2" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Upload File</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
	   <input type="file" class="input_file_assesment" name="file">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" id="add-assesment" class="btn btn-primary">Upload assesment</button>
      </div>
    </div>
  </div>
</div>
` 
frappe.test_app_page = {
	body:body,
	model: model,
	model2:model2
}


const survey_handler = ()=>{

}