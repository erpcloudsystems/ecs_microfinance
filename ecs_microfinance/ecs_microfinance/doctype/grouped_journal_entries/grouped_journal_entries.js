frappe.ui.form.on('Grouped Journal Entries', {
	onload: (frm) => {
		frm.set_query("party_type", function() {

			return {
				query: "erpnext.setup.doctype.party_type.party_type.get_party_type",
				filters: {
					'account': frm.doc.account
				}
			}
		});
	
		frm.set_df_property("grouped_journal_entries", "cannot_add_rows", true);
		frm.set_df_property("accounts_logs", "cannot_add_rows", true);
		// frm.set_df_property("items", "cannot_delete_rows", true);
		if (!frm.doc.posting_date) {
			frm.doc.posting_date = frappe.datetime.nowdate();
		}
		
		frm.events.filter_on_account_field(frm);
		frm.events.fill_parent_territory(frm);
	},
	button_11: (frm) => {
		frm.events.check_frm_params(frm);
		frm.events.create_account_logs(frm);
		general_calculate_percent_in_account_log(frm)
		
	},
	filter_on_account_field : (frm)=>{
		frm.set_query("account",  () => {
			return {
				"filters": {
					"is_group": 0,
				}
			};
		});
	},
	fill_parent_territory : (frm)=>{
		cur_frm.fields_dict['parent_territories'].grid.get_field("parent_territory").get_query = function(doc, cdt, cdn) {
            const selected_territories = frm.doc.parent_territories.map((item)=> item.parent_territory)
			return {
			filters:[
			["Territory","is_group", "=", 1],
			["Territory","name", "!=", "All Territories"],
			["Territory","name", "!=", "المحافظة"],
			["Territory","name", "!=", "وجه بحري"],
			["Territory","name", "!=", "وجه قبلي"],	
			["Territory","name", "NOT IN", selected_territories ],
			]
			};
		}
	},
	check_frm_params: (frm)=>{
		if (!(frm.doc.account || frm.doc.amount )) {
				frappe.throw("Check Account and Amount")
		}
		if (!frm.doc.child_territories.length) {
			frappe.throw("Child Territories Must Contain a Value")
	}
	},
	create_account_logs: (frm)=> {
		let account_logs_map = frm.doc.accounts_logs ? frm.doc.accounts_logs.map(account => account.account): []
		if (account_logs_map.includes(frm.doc.account)){
			add_account_log_check(frm)
		}else {
			let account_log_id = add_account_log(frm)
			calculate_debit_credit(frm)
			frm.events.create_grouped_journal_entries(frm, account_log_id);
			calculate_total_debit_credit_entries(frm)
		}
	},
	create_grouped_journal_entries: (frm, account_log_id)=>{
		frm.doc.child_territories.forEach((cur, idx, array)=>{
			if (cur.parent_territory) {
				let  grouped_journal_entry = frm.add_child("grouped_journal_entries");
				grouped_journal_entry.account=frm.doc.account
				grouped_journal_entry.child_territory=cur.child_territory	
				grouped_journal_entry.account_log_name=account_log_id
				grouped_journal_entry.percent= 100 /	frm.doc.child_territories.length 
				grouped_journal_entry.debit=frm.doc.debit_credit === "Debit" ? frm.doc.amount / frm.doc.child_territories.length  : 0
				grouped_journal_entry.credit=frm.doc.debit_credit === "Credit" ? frm.doc.amount / frm.doc.child_territories.length : 0
				grouped_journal_entry.total= frm.doc.amount 
				grouped_journal_entry.party_type= frm.doc.party_type
				grouped_journal_entry.party= frm.doc.party 
			}
		})
		frm.refresh_field('grouped_journal_entries');
		frm.events.clear_init_tables(frm)
		frm.save()
	

	},
	clear_init_tables: (frm)=> {
		frm.clear_table('child_territories');
		frm.clear_table('parent_territories');
		frm.doc.account = ""
		frm.doc.debit_credit = ""
		frm.doc.amount = 0
		frm.refresh();
	},
})

frappe.ui.form.on("Parent Territory", "parent_territory", function(frm, cdt, cdn) {
    let item = locals[cdt][cdn]; 
	// let account_logs_map = frm.doc.accounts_logs ? frm.doc.accounts_logs.map(account => account.account): []

	const selected_territories = frm.doc.child_territories ? frm.doc.child_territories.map((item)=> item.parent_territory) : []

	if (item.parent_territory && !selected_territories.includes(item.parent_territory)) {
			fill_child_territories(frm, item.parent_territory)
	}
});
frappe.ui.form.on("Accounts Logs", "credit", function(frm, cdt, cdn) {
	let item = locals[cdt][cdn]
	calculate_debit_credit(frm)
	calculate_current_percent_in_account_log(frm, item.log_name)
	frm.refresh_field("accounts_logs")
	frm.refresh()
});
frappe.ui.form.on("Accounts Logs", "debit", function(frm, cdt, cdn) {
	let item = locals[cdt][cdn]
	calculate_debit_credit(frm)
	calculate_current_percent_in_account_log(frm, item.log_name)
	frm.refresh_field("accounts_logs")
	frm.refresh()


});
frappe.ui.form.on('Parent Territory', { 
	parent_territories_remove(frm, cdt, cdn) { 
		let item = locals[cdt];	
		if (item === undefined){
			frm.clear_table('child_territories');
			frm.refresh();
		}else {
			clear_related_child_territories(frm)
		}
    }
});
frappe.ui.form.on('Child Territories', { 
	child_territories_remove(frm, cdt, cdn) { 
		let item = locals[cdt];	
		if (item === undefined){
			frm.clear_table('parent_territories');
			frm.refresh();
		}else {
			clear_related_parent_territories(frm)
		}
    }
});
frappe.ui.form.on('Accounts Logs', { 
	accounts_logs_remove(frm, cdt, cdn) { 

			clear_related_journal_entries(frm)
			calculate_debit_credit(frm)
			calculate_total_debit_credit_entries(frm)
    }
});
frappe.ui.form.on('Grouped Journal Entries Table', { 
	grouped_journal_entries_remove(frm, cdt, cdn) { 
			clear_related_account_logs(frm)
			calculate_debit_credit(frm)
			calculate_total_debit_credit_entries(frm)
		
    }
});
frappe.ui.form.on("Grouped Journal Entries Table", "percent", function(frm, cdt, cdn) {
		calculate_debit_credit_in_entries(frm, cdt, cdn)
});
frappe.ui.form.on("Grouped Journal Entries Table", "debit", function(frm, cdt, cdn) {
	calculate_percent_in_entries(frm, cdt, cdn)
});
frappe.ui.form.on("Grouped Journal Entries Table", "credit", function(frm, cdt, cdn) {
	calculate_percent_in_entries(frm, cdt, cdn)
});
let calculate_debit_credit = (frm) => {
	let debit_sum = 0
	let credit_sum = 0
	frm.doc.accounts_logs.forEach((cur, idx, array) =>{
		debit_sum += cur.debit ? cur.debit : 0 
		credit_sum += cur.credit ? cur.credit : 0 
	})
	frm.doc.total_debit = debit_sum
	frm.doc.total_credit = credit_sum
	frm.refresh();
}
let calculate_total_debit_credit_entries = (frm) => {
	let debit_sum = 0
	let credit_sum = 0
	frm.doc.grouped_journal_entries.forEach((cur, idx, array) =>{
		debit_sum += cur.debit ? cur.debit : 0 
		credit_sum += cur.credit ? cur.credit : 0 
	})
	frm.doc.total_debit_entries = debit_sum
	frm.doc.total_credit_entries = credit_sum
	frm.refresh();
}

let checkIfParentDuplicate = (frm, parent_territory)=>{
	let duplicates = true
	frm.doc.parent_territories.forEach((value, idx, array)=>{
		if(value.parent_territory == parent_territory) {
			duplicates= false
		}
	})
	return duplicates
}
let fill_child_territories =  (frm, parent_territory) => {
	frappe.call(
			{
			method: 'frappe.client.get_list',
			args: {
					'doctype': 'Territory',
					'filters': {'parent_territory': parent_territory},
					'fieldname': [
						'name',
					]
				},
			callback:  (r) =>{
				if (r.message) {
					r.message.forEach((value, idx, arr)=>{
						let child_territories = frm.add_child("child_territories");
						child_territories.parent_territory=parent_territory
						child_territories.child_territory=value.name
					})
					frm.refresh_field('child_territories');
					// frm.save()
				}
				
			},
			freeze: true,
			freeze_message: __(`Filling Child Territories for ${parent_territory}......`)
		});


};

let clear_related_child_territories = (frm) =>{
const parent_territories = frm.doc.parent_territories.map((cur)=> cur.parent_territory)
			const new_items = []
			frm.doc.child_territories.forEach((cur ,idx, array)=> {
				if (parent_territories.includes(cur.parent_territory)  ) {
					new_items.push(cur)
				}
			})
				frm.doc.child_territories = new_items ;

	frm.refresh_field('child_territories');
}

let clear_related_parent_territories = (frm) =>{
	const parent_territories = frm.doc.parent_territories.map((cur)=> cur.parent_territory)
	const child_territories = frm.doc.child_territories.map((cur)=> cur.parent_territory)
				const new_items = [] 
				frm.doc.parent_territories.forEach((cur ,idx, array)=> {
					if (child_territories.includes(cur.parent_territory)  ) {
						new_items.push(cur)

					}
				})
				frm.doc.parent_territories = new_items ;

	
		frm.refresh_field('parent_territories');
	}

	let clear_related_journal_entries = (frm) =>{
		const logs_names = frm.doc.accounts_logs.map(account => account.log_name)
		const journal_entries = frm.doc.grouped_journal_entries.filter((cur, idx, array)=> {
			return logs_names.includes(cur.account_log_name)  
		})
					frm.doc.grouped_journal_entries = journal_entries ;

			frm.refresh_field('grouped_journal_entries');
		}

	let clear_related_account_logs = (frm) =>{
			const journal_entries = frm.doc.grouped_journal_entries.map(account => account.account_log_name)
			const logs_names = frm.doc.accounts_logs.filter((cur, idx, array)=> {
				return journal_entries.includes(cur.log_name)  
			})
						frm.doc.accounts_logs = logs_names ;
	
				frm.refresh_field('accounts_logs');
			}
	const add_account_log_check = function (frm) {
		frappe.confirm(__(`This will Add Duplicate Entry of Account ${frm.doc.account}. Are you sure?`),
			function () {
				let account_log_id = add_account_log(frm)
				calculate_debit_credit(frm)
				frm.events.create_grouped_journal_entries(frm, account_log_id);
				calculate_total_debit_credit_entries(frm)


			},
			function () {
					frm.events.onload(frm);
					frm.scroll_to_field('account');

				
			}
		);
	};

const add_account_log = (frm) => {
	let generated_id = generate_id(frm.doc.accounts_logs === undefined ? 4: frm.doc.accounts_logs.length + 4)
	let account_logs = frm.add_child("accounts_logs");
	account_logs.account=frm.doc.account
	account_logs.log_name=generated_id
	account_logs.debit=frm.doc.debit_credit === "Debit" ? frm.doc.amount : 0
	account_logs.credit=frm.doc.debit_credit === "Credit" ? frm.doc.amount : 0
	frm.refresh_field('accounts_logs');
	return generated_id
}

let calculate_debit_credit_in_entries = (frm, cdt, cdn) =>{
	let item = locals[cdt][cdn]; 
	let [{credit, debit}] = frm.doc.accounts_logs.filter((cur, idx, array)=>
		cur.log_name === item.account_log_name
	)
	item.debit=item.debit? debit * item.percent / 100 : 0
	item.credit=item.credit? credit * item.percent / 100 : 0
	frm.refresh_field('grouped_journal_entries');
	calculate_total_debit_credit_entries(frm)
	calculate_percent_in_account_log(frm, item.account_log_name)

}
let calculate_percent_in_entries = (frm, cdt, cdn) =>{
	let item = locals[cdt][cdn]; 
	let [{credit, debit}] = frm.doc.accounts_logs.filter((cur, idx, array)=>
	cur.log_name === item.account_log_name
)
	
	item.percent =item.debit? Math.round(((item.debit *100) /(credit || debit) ) * 100000) / 100000  : Math.round(((item.credit *100) /(credit || debit) ) * 100000) / 100000
	frm.refresh_field('grouped_journal_entries');
	calculate_total_debit_credit_entries(frm)
	calculate_percent_in_account_log(frm, item.account_log_name)

}

let generate_id =  (length) => {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

let calculate_percent_in_account_log = (frm, account_log_name)=> {
		let percent = 0
		frm.doc.grouped_journal_entries.forEach(
			(cur,idx,array)=> {
				if (cur.account_log_name === account_log_name) {
					percent += cur.percent 
				}
			})
		let accounts_percent = frm.doc.accounts_logs.map((cur,idx,array)=> {
				if(cur.log_name === account_log_name){
					cur_frm.get_field("accounts_logs").grid.grid_rows[idx].doc.percent = percent
					cur_frm.get_field("accounts_logs").grid.grid_rows[idx].refresh_field("percent")	
				}
				return cur
			})	

		// frm.doc.accounts_logs = accounts_percent
		frm.refresh_field('accounts_logs');

		
}

let calculate_current_percent_in_account_log = (frm, account_log_name)=> {
	let creditDebit = 0
	frm.doc.grouped_journal_entries.forEach(
		(cur,idx,array)=> {
			if (cur.account_log_name === account_log_name) {
				creditDebit +=  cur.debit? cur.debit  : 0
				creditDebit +=  cur.credit? cur.credit  : 0 
			}
		})
	frm.doc.accounts_logs.forEach((cur,idx,array)=> {
			if(cur.log_name === account_log_name){
	

				cur_frm.get_field("accounts_logs").grid.grid_rows[idx].doc.percent = (cur.credit || cur.debit) / creditDebit * 100
				cur_frm.get_field("accounts_logs").grid.grid_rows[idx].refresh_field("percent")	
			}
			// return cur
		
		})	
		// return percent
	// frm.doc.accounts_logs = accounts_percent
	frm.refresh_field('accounts_logs');

	
}

let general_calculate_percent_in_account_log = (frm)=> {
	frm.doc.accounts_logs.forEach((log, index, arr) =>{
		let percent = 0
		frm.doc.grouped_journal_entries.forEach(
			(cur,idx,array)=> {
				if (cur.account_log_name === log.log_name) {
					percent += cur.percent 
				}
			})
			console.log(percent)
			cur_frm.get_field("accounts_logs").grid.grid_rows[index].doc.percent = percent
			cur_frm.get_field("accounts_logs").grid.grid_rows[index].refresh_field("percent")	
	})
	
	frm.refresh_field('accounts_logs');

	
}
