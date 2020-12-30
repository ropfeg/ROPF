// Below function changes all fileds to required in update menu when status is changed to done
function setFieldsToRequired(){
  let inputVal = document.getElementById("updateStatus").value;
  let inputs = document.querySelectorAll("#updateForm input");
  if (inputVal == "done") {
      for(i = 0; i < inputs.length; i++){
      inputs[i].required="required";
      }
  } 
  else {
      for(i = 0; i < inputs.length; i++){
      inputs[i].required="";
      }
  }
}



// Below is an event listener to be triggered whenever the adding form is submitted
// function includes all dates validation when adding a record
// function outputs all errors to an empty (h2) tag set in HTML with the id errs
var addForm = document.forms["addForm"];
addForm.addEventListener('submit', (e) => {
    let feedback = document.forms["addForm"]["feedback"];                
    let request_date = document.forms["addForm"]["request_date"];  
    let last_visit = document.forms["addForm"]["last_visit"];                
    let status = document.forms["addForm"]["status"].value; 
    let errorElement = document.getElementById('errs');
    let messages = [];
    feedback.style.borderColor = "rgb(206, 212, 218)";
    last_visit.style.borderColor = "rgb(206, 212, 218)";
    request_date.style.borderColor = "rgb(206, 212, 218)";

    if (status == "in-progress") {
        let prognow = new Date().toLocaleDateString('en-CA');
        if (feedback.value < request_date.value && feedback.value != "") {
            messages.push("Feedback date can't be before request date");
            feedback.style.border = "medium solid #FF0000";
            feedback.focus(); 
        }
        if (last_visit.value < request_date.value && last_visit.value != "") {
            messages.push("Last visit date can't be before request date");
            last_visit.style.border = "medium solid #FF0000";
            last_visit.focus(); 
        } 
        if( request_date.value > prognow){
            messages.push("Request date can't be in a future date");
            request_date.style.border = "medium solid #FF0000";
            request_date.focus();  
          }
    }
    if (messages.length > 0) {
        e.preventDefault();
        errorElement.innerText = messages.join(', ');
    }
    })

    
// Below is an event listener to be triggered whenever the updating form is submitted
// function includes all dates validation when updating a record
// function outputs all errors to an empty (h2) tag set in HTML with the id errs
var updateForm = document.forms["updateForm"];
updateForm.addEventListener('submit', (e) => {
    let feedback = document.forms["updateForm"]["update_feedback"];                
    let request_date = document.forms["updateForm"]["update_request_date"];  
    let last_visit = document.forms["updateForm"]["update_last_visit"];
    let status = document.forms["updateForm"]["update_status"].value; 
    let inprogress_date = new Date(document.forms["updateForm"]["update_inprogress_date"].value).toLocaleDateString('en-CA');
    let errorElement = document.getElementById('errs');
    let messages = [];
    feedback.style.borderColor = "rgb(206, 212, 218)";
    last_visit.style.borderColor = "rgb(206, 212, 218)";
    request_date.style.borderColor = "rgb(206, 212, 218)";

    if (status == "done") {
        let updatenow = new Date().toLocaleDateString('en-CA');
        if (feedback.value > updatenow) {
            messages.push("Feedback date can't be after done date");
            feedback.style.border = "medium solid #FF0000";
            feedback.focus(); 
        }
        if (last_visit.value > updatenow) {
            messages.push("Last Visit date can't be after done date");
            last_visit.style.border = "medium solid #FF0000";
            last_visit.focus(); 
        } 
    }

    if (feedback.value < request_date.value) {
        messages.push("Feedback date can't be before request date");
        feedback.style.border = "medium solid #FF0000";
        feedback.focus(); 
    }
    if (last_visit.value < request_date.value) {
        messages.push("Last visit date can't be before request date");
        last_visit.style.border = "medium solid #FF0000";
        last_visit.focus(); 
    } 
    if( inprogress_date < request_date.value){
        messages.push("Request date can't be in a future date");
        request_date.style.border = "medium solid #FF0000";
        request_date.focus();  
      }

    if (messages.length > 0) {
        e.preventDefault();
        errorElement.innerText = messages.join(', ');
    }
    })
