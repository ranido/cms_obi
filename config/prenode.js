// prenode.js
// stub to include printf and scanf in javascript programs
// for cms, copy to /usr/local/etc/saci/
// and do npm -g install scanf-printf-obi

var scanf_stub = require('/usr/local/lib/node_modules/scanf-printf-obi').scanf,
    printf_stub = require('/usr/local/lib/node_modules/scanf-printf-obi').sprintf,
    fgets_stub = require('/usr/local/lib/node_modules/scanf-printf-obi').fgets

function scanf(format) {
    // scanf_stub returns an expression with variables passed and values read from stdin
    var res = scanf_stub.apply(this, Array.prototype.slice.call(arguments, 0));
    eval(res);
}

function printf(args){
    // printf_stub returns the formatted string to be output
    var res = printf_stub.apply(this, Array.prototype.slice.call(arguments, 0));
    process.stdout.write(res);
}

function fgets(args){
    // fgets_stub returns an expression with the variable and value read from stdin
    var res = fgets_stub.apply(this, Array.prototype.slice.call(arguments, 0));
    eval(res);
}

// end of stub
