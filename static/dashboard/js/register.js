$(document).ready(function() {
    $("#view_button3").bind("mousedown touchstart", function() {
        $("#password").attr("type", "text");
    }), $("#view_button3").bind("mouseup touchend", function() {
        $("#password").attr("type", "password");
    }), $("#view_button4").bind("mousedown touchstart", function() {
        $("#verifypassword").attr("type", "text");
    }), $("#view_button4").bind("mouseup touchend", function() {
        $("#verifypassword").attr("type", "password");
    }), $("#master_password_button").bind("mousedown touchstart", function() {
        $("#master_password").attr("type", "text");
    }), $("#master_password_button").bind("mouseup touchend", function() {
        $("#master_password").attr("type", "password");
    })
});
function passwordChecker(){
    $('#verifypassword').val('');
    $('#message1').html(''); $('#message8').html(''); $('#message10').html('');
    $('#message').html('');$('#message2').html('');$('#message3').html('');$('#message4').html('');$('#message5').html('');$('#message6').html('');$('#message7').html('');
    if($('#password').val().length>=4){
	if(newValPassPoilcy()===true ){
	    $('#message').css('color','green');
	    $('#message').html('Although looks like a good password, try to make it more stronger');
	    if($('#password').val().length>=9){
		$('#message').html('');
		$('#message1').html('');
	    } 
	    return true;
	}
    }
    
    
}
function NumAndWordRep(){
    var password = $('#password').val().toLowerCase();
    if(password.match(/(.)\1\1/)){
	//	alert("Your Password cannot contain Character or Number repetition");
	$('#message7').css('color','red');
	$('#message7').html('Your Password cannot contain Character or Number repetition.');
	return false;
    }
    return true;
}
function userNameAsPass(){
    var password = $('#password').val().toLowerCase();
    var uname=$('#username').val().toLowerCase();
    
    var uname1 = new RegExp(uname);
    if(null!==uname &&''!==uname){
	if( uname1.test(password)){
	    
	    $('#message6').css('color','red');
	    $('#message6').html('Your Password cannot contain your Username.');
	    return false;
	}}
    else{
	$('#message6').html('');
	$('#message10').css('color','red');
	$('#message10').css('font-weight','bold');
	$('#message10').html('Please enter your username first !!');
	return false;
    }
    return true;
    
}
function  newValPassPoilcy(){
    
    var password = $('#password').val();
    if(!password.match(/^(?=.{6,})(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&_+=\\*\\-\\(\\)\\{\\}\\:\\;\\<\\>\\|\\,\\.\\?\\/\\'\\"]).*$/) || userNameAsPass()===false || NumAndWordRep()===false){
	
	$('#message8').css('color','red');
	$('#message8').html('Your password must contain:-');
	if(!password.match(/^(?=.{6,}).*$/)){
	    $('#message').css('color','red');
	    $('#message').html(' - minimum 6 characters.');
	    
	}
	if(!password.match(/^(?=.*[0-9]).*$/)){
	    $('#message2').css('color','red');
	    $('#message2').html(' - at least 1 Number.');
	    
	}
	if(!password.match(/^(?=.*[a-z]).*$/))
	{
	    $('#message3').css('color','red');
	    $('#message3').html(' - at least 1 Lowercase character.');
	    
	}
	if(!password.match(/^(?=.*[A-Z]).*$/)){
	    $('#message4').css('color','red');
	    $('#message4').html(' - at least 1 Uppercase character.');
	    
	}
	if(!password.match(/^(?=.*[!@#$%^&_+=\\*\\-\\(\\)\\{\\}\\:\\;\\<\\>\\|\\,\\.\\?\\/\\'\\"]).*$/)){
	    
	    $('#message5').css('color','red');
	    $('#message5').html('	- at least 1 Special character.');
	    
	}
	if(userNameAsPass()===false){
	    if(password.match(/^(?=.{6,})(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&_+=\\*\\-\\(\\)\\{\\}\\:\\;\\<\\>\\|\\,\\.\\?\\/\\'\\"]).*$/)){
		$('#message8').html('');  
	    }
	    
	}
	if(NumAndWordRep()===false){
	    if(password.match(/^(?=.{6,})(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&_+=\\*\\-\\(\\)\\{\\}\\:\\;\\<\\>\\|\\,\\.\\?\\/\\'\\"]).*$/)){
		$('#message8').html('');  
	    }
	    
	} 
	return false;
    } 
    else{
	
	return true;
    }
    
}	
function submitForm(){
    
    var password=$('#password').val();
    var confirm=$('#verifypassword').val();
    
    //alert("fdsfs");
    if(document.getElementById("username").value.trim()==="" && document.getElementById("username").value!==null){
	$('#message1').css('color','red');
	$('#message1').html('Please enter your username');   
    }
    else if(document.getElementById("master_password").value.trim()==="" && document.getElementById("master_password").value!==null){
	$('#message1').css('color','red');
	$('#message1').html('Please enter your Master Password');   
    }
    else if(document.getElementById("yourEmail").value.trim()==="" && document.getElementById("yourEmail").value!==null){
	$('#message1').css('color','red');
	$('#message1').html('Please enter your Email ID');   
    }
    else if(checkEmail()===false){
	$('#message1').css('color','red');
	$('#message1').html('Enter a valid Email address'); 

    }
    else if(document.getElementById("password").value.trim()==="" && document.getElementById("password").value!==null){
	$('#message1').css('color','red');
	$('#message1').html('Please enter your Password');   
    }
    else if(document.getElementById("verifypassword").value.trim()==="" && document.getElementById("verifypassword").value!==null){
	$('#message1').css('color','red');
	$('#message1').html('Please confirm your password');   
    }
    
    else if(password!=confirm){
	$('#message1').css('color','red');
	$('#message1').html('Confirm password and password must be same');   
	
    }
	
    else{
    	document.getElementById("register-form").submit();
    }
    
}

function checkEmail(){
    var email=$('#yourEmail').val();
    if((email.indexOf(".") > 2) && (email.indexOf("@") > 0)){
	return true; 
    }
    else{
	return false;		 
    }
    
}
