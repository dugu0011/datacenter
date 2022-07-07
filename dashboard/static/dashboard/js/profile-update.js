$(document).ready(function(){	
    
    // firstname
    
    $("#edit-f_name").click(function(){
	
	var ro_old = $('input[name="input-f_name"]').attr('readonly')
	
	if (ro_old == "readonly"){
	    $('input[name="input-f_name"]').prop('readonly',false);
	    $('#edit-f_name').html("Cancel");
	}
	else{
	    ro_new = $('input[name="input-f_name"]').prop('readonly',true)
	    $('#edit-f_name').html('Edit It');
	}
    });
    
    // lastname
    
    $("#edit-l_name").click(function(){
	
	var ro_old = $('input[name="input-l_name"]').attr('readonly')
	
	if (ro_old == "readonly"){
	    $('input[name="input-l_name"]').prop('readonly',false);
	    $('#edit-l_name').html("Cancel");
	}
	else{
	    ro_new = $('input[name="input-l_name"]').prop('readonly',true)
	    $('#edit-l_name').html('Edit It');
	}
    });
    
    // BIO
    $("#edit-bio").click(function(){
	
	var ro_old = $('input[name="input-bio"]').attr('readonly')
	
	if (ro_old == "readonly"){
	    $('input[name="input-bio"]').prop('readonly',false);
	    $('#edit-bio').html("Cancel");
	}
	else{
	    ro_new = $('input[name="input-bio"]').prop('readonly',true)
	    $('#edit-bio').html('Edit It');
	}
    });
// IMAGE
$("#edit-img").click(function(){
	
	var ro_old = $('input[name="input-img"]').attr('readonly')
	
	if (ro_old == "readonly"){
	    $('input[name="input-img"]').prop('readonly',false);
	    $('#edit-img').html("Cancel");
	}
	else{
	    ro_new = $('input[name="input-img"]').prop('readonly',true)
	    $('#edit-img').html('Edit It');
	}
    });


    // end of document.load
});
