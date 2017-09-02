var canvas = document.querySelector("canvas");

var signaturePad = new SignaturePad(canvas);

// // Returns signature image as data URL (see https://mdn.io/todataurl for the list of possible parameters)
// signaturePad.toDataURL(); // save image as PNG
// signaturePad.toDataURL("image/jpeg"); // save image as JPEG
// signaturePad.toDataURL("image/svg+xml"); // save image as SVG
//
// // Draws signature image from data URL
// signaturePad.fromDataURL("data:image/png;base64,iVBORw0K...");
//
// // Returns signature image as an array of point groups
// const data = signaturePad.toData();
//
// // Draws signature image from an array of point groups
// signaturePad.fromData(data);
//
// // Clears the canvas
// signaturePad.clear();
//
// // Returns true if canvas is empty, otherwise returns false
// signaturePad.isEmpty();
//
// // Unbinds all event handlers
// signaturePad.off();
//
// // Rebinds all event handlers
// signaturePad.on();


$(function() {

    c = $('canvas');
    // Obtain a graphics context on the canvas element for drawing.
    htmlCanvas = document.getElementById('canvas');
    // Obtain a graphics context on the canvas element for drawing.
    context = htmlCanvas.getContext('2d');

    initialize();

    function initialize() {
        window.addEventListener('resize', resizeCanvas, false);
        resizeCanvas();
    }

    function resizeCanvas() {
        htmlCanvas.width = c.parent().width();
        htmlCanvas.height = c.parent().width() / 4 * 1;
        // redraw();
    }

    function redraw() {
        context.strokeStyle = 'blue';
        context.lineWidth = '5';
        context.strokeRect(0, 0, window.innerWidth, window.innerHeight);
    }
    $('.btn-clearSign').click(function() {
      signaturePad.clear();
    });
    $('.btn-saveSign').click(function() {
        var test = signaturePad.toDataURL();

        $.ajax({
          type: "POST",
          url: "/set_sign",
          data:JSON.stringify({
            imageBase64: test
          })
        }).done(function(resp) {
          location.reload();
        });
    });
});
