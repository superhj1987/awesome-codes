var rvalidchars = /^[\],:{}\s]*$/
var rvalidescape = /\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g
var rvalidtokens = /"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g
var rvalidbraces = /(?:^|:|,)(?:\s*\[)+/g
