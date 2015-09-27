function show_file_name(){
    document.getElementById("fileName").value = document.getElementById('file').files[0].name;
    document.getElementById("fileName").className = "show-file-name";
    }

document.getElementById('file').onchange = show_file_name;


document.getElementById('switch').onclick = function(){
    window.location='/record';
};

document.getElementById('upload-file').onclick = function(){
    var xhr = new XMLHttpRequest();

document.getElementById("mask").className = "mask-display";
    var form = new FormData();
    var f = document.getElementById('file').files[0];
    form.append('file', f);
        
    $.ajax({
        type: 'POST',
        url: '/results',
        data: form,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            document.write(data)
        },
    });
};


document.getElementById('switch').onclick = function(){
    window.location='/record';
};
    
document.getElementById('upload-file').onclick = function(){
    var xhr = new XMLHttpRequest();

    document.getElementById("mask").className = "mask-display";
    var form = new FormData();
    var f = document.getElementById('file').files[0];
    form.append('file', f);
        
    $.ajax({
        type: 'POST',
        url: '/results',
        data: form,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            document.write(data)
        },
    });
};