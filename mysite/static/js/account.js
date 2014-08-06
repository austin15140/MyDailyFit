$(document).ready(function(){

    $('.file-input').hover(function() {
        $('.btn-file').addClass('btn-file-hover');
    }, function() {
        $('.btn-file').removeClass('btn-file-hover');
    });

    $('.file-input2').hover(function() {
        $('.btn-file2').addClass('btn-file-hover');
    }, function() {
        $('.btn-file2').removeClass('btn-file-hover');
    });

    $('#file1').change(function(){
        var filename = this.value.replace(/\\/g, '/').replace(/.*\//, '')
        $('#filename1').text(filename);
    });

    $('#file2').change(function(){
        var filename = this.value.replace(/\\/g, '/').replace(/.*\//, '')
        $('#filename2').text(filename);
    });

});