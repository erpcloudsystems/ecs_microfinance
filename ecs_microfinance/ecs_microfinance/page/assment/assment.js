frappe.pages['assment'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'التقييم',
        single_column: true
    });

    // Check if countdown time is stored in sessionStorage
    var countdownTime = sessionStorage.getItem('countdownTime');
    // If countdownTime is not null, parse it to an integer
    countdownTime = countdownTime ? parseInt(countdownTime) : 30;

    // Create a container for the information and timer
    var infoContainer = $('<div id="info-container"></div>').appendTo(wrapper);

    // Get the Training Event name
    var trainingEventName = frappe.route_options.training_event;
    // Get today's date
    var todayDate = frappe.datetime.get_today();
    // Get the user session ID
    var sessionId = frappe.session.user;

    // Add the information to the container
    var infoText = 'Training Event: ' + trainingEventName + ' | Today\'s Date: ' + todayDate + ' | Session ID: ' + sessionId;
    infoContainer.text(infoText);

    // Add countdown timer
    var countdownTimer = $('<div id="countdown-timer"></div>').appendTo(infoContainer);

    function startCountdown() {
        var timer = setInterval(function() {
            countdownTime--;
            countdownTimer.text('Time left: ' + countdownTime + ' seconds');

            // Store countdownTime in sessionStorage
            sessionStorage.setItem('countdownTime', countdownTime);

            if (countdownTime <= 0) {
                clearInterval(timer);
                // Automatically submit the assessment
                submitAssessment();
                sessionStorage.clear();
            }
        }, 1000); // Update timer every second
    }

    startCountdown();

    // Check if the questions container exists, if not, create it
    if ($('#questions-container').length === 0) {
        $('<div id="questions-container"></div>').appendTo('body'); // Or any appropriate parent element
    }

    // Fetch random questions from the server and display them
    frappe.call({
        method: 'ecs_microfinance.doctype_triggers.hr.training_event.training_event.get_random_questions',
        args: {
            custom_training_event: trainingEventName,
            today_date: todayDate,
            session_id: sessionId
        },
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                // Get the questions container
                var questionsContainer = $('#questions-container');

                // Loop through each question and create HTML elements
                r.message.forEach(function(question, index) {
                    var questionElement = $(`<div class="question" data-question-type="${question.type}" data-name-question ='${question.name}' ></div>`);

                    // Append question heading with underline
                    questionElement.append('<h2>السؤال رقم ' + (index + 1) + '</h2>');

                    // Append question text
                    questionElement.append('<p>' + question.question + '</p>');

                    // Append input field if question type is "User Input"
                    if (question.type === "User Input") {
                        var inputField = $('<input type="text" name="user-answer-' + index + '">');
                        questionElement.append(inputField);
                    }

                    // Append options if question type is "Choices"
                    if (question.type === "Choices") {
                        var optionsGrid = $('<div class="options-grid"></div>'); // Create a container for the options
                        // Collect options from option_1 to option_4
                        for (var i = 1; i <= 4; i++) {
                            var option = question['option_' + i];
                            if (option) {
                                var optionElement = $('<label><input type="radio" name="question' + index + '" value="' + option + '"> ' + option + '</label>');
                                optionsGrid.append(optionElement);
                            }
                        }
                        // Append options grid to question element
                        questionElement.append(optionsGrid);
                    }

                    // Append question element to questions container
                    questionsContainer.append(questionElement);
                });

                // Append submit button
                var submitButton = $('<button id="submit-button">إرسال</button>');
                questionsContainer.append(submitButton);

                // Submit button click event
                submitButton.on('click', function() {
                    // Implement your submit logic here
                    submitAssessment(); // Call the function to submit the assessment
                });
            } else {
                // Handle case when no questions are returned
                console.error('لم يتم العثور على أي أسئلة.');
            }
        },
        error: function(xhr, status, error) {
            console.error('حدث خطأ أثناء جلب الأسئلة:', error);
        }
    });

    // Function to submit the assessment
    function submitAssessment() {
        var assessmentData = {
            training_event: trainingEventName,
            submitting_datetime: frappe.datetime.now_datetime(),
            user: frappe.session.user,
            assessment_results: []  // Array to store assessment results for each question
        };

        // Loop through each question and collect assessment results
        $(".question").each(function(index) {
            var questionId = $(this).data("name-question"); // Adjust to the correct attribute name
            var userAnswer = "";  // Initialize user's answer

            // Determine user's answer based on question type
            if ($(this).data("question-type") === "User Input") {
                userAnswer = $(this).find("input[name='user-answer-" + index + "']").val();
            } else if ($(this).data("question-type") === "Choices") {
                userAnswer = $(this).find("input[name='question" + index + "']:checked").val();
            }

            // Create assessment result object for the current question
            var assessmentResult = {
                name: questionId, // Correct the attribute name if necessary
                trainee_answer: userAnswer,
                question_type: $(this).data("question-type")
            };

            // Push assessment result to the assessment data array
            assessmentData.assessment_results.push(assessmentResult);
        });

        console.log('Assessment Data:', assessmentData);

        // Make AJAX call to submit assessment data to server
        frappe.call({
            method: 'ecs_microfinance.doctype_triggers.hr.training_event.training_event.process_assessment_results',
            args: {
                assessment_data: JSON.stringify(assessmentData)
            },
            callback: function(response) {
                console.log(response.message);
                alert('تم حفظ نتائج التقييم بنجاح!');
                sessionStorage.clear();

                window.location.href = 'https://microfinance.erpnext.cloud/assessment-submission';

            },
            error: function(xhr, status, error) {
                console.error('حدث خطأ أثناء حفظ نتائج التقييم:', error);
                alert('حدث خطأ أثناء حفظ نتائج التقييم. يرجى المحاولة مرة أخرى.');
            }
        });
    }

    // CSS Styles
    var style = `
    #info-container {
        background-color: #f0f0f0;
        padding: 10px 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    #countdown-timer {
        font-weight: bold;
        color: #ed1f1f;
        margin-top: 5px;
    }
    #questions-container {
        margin: 20px auto;
        padding: 20px;
        width: 45%;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }

    .question {
        margin-bottom: 30px;
        padding: 20px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        direction: rtl; /* Set text direction to right-to-left */
        text-align: right; /* Align text to the right */
    }

    .question h2 {
        font-weight: bold;
        font-size: 24px;
        color: #ed1f1f;
        margin-bottom: 15px;
        direction: rtl; /* Set text direction to right-to-left */
        text-align: right; /* Align text to the right */
        text-decoration: underline;
    }

    .question p {
        font-size: 18px;
        line-height: 1.6;
        font-weight: bold;
        color: #666;
        margin-bottom: 20px;
        direction: rtl; /* Set text direction to right-to-left */
        text-align: right; /* Align text to the right */
    }

    .options-grid {
        display: grid;
        grid-template-columns: auto auto; /* Adjust the number of columns as needed */
        grid-gap: 10px;
        direction: rtl; /* Set text direction to right-to-left */
        text-align: right; /* Align text to the right */
    }

    input[type="text"] {
        width: 75%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box;
        font-size: 16px;
        margin-top: 10px;
    }

    #submit-button {
        display: block;
        width: 100%;
        padding: 12px;
        background-color: #007bff;
        color: #fff;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        font-size: 18px;
        transition: background-color 0.3s ease;
    }

    #submit-button:hover {
        background-color: #0056b3;
    }

    `;

    // Append styles to head
    $('head').append('<style>' + style + '</style>');
};
