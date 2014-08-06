$(document).ready(function() {

    $('#file1').on('hover', function(){
        $('#fb-1').addClass('underline')
    });

    $('#fb-2').click(function(){
        $('#file2').click();
    });

    $('#file1').change(function(){
        var filename = this.value.replace(/\\/g, '/').replace(/.*\//, '')
        $('#filename1').text(filename);
    });

    $('#file2').change(function(){
        var filename = this.value.replace(/\\/g, '/').replace(/.*\//, '')
        $('#filename2').text(filename);
    });

    $('#meal-plan').hide();
    $('#workout-plan').hide();
    $('#trophies').hide();
    $('#my-trainer').hide();

    $('#meal-plan-link').click(function() {
        $('user-settings').css('display', 'none');
        $('#meal-plan').show();
    });

});
