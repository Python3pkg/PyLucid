/* content from:
 * https://github.com/marijnh/CodeMirror/raw/master/contrib/python/js/parsepython.js
 * closure compiled 2011-05-17 */
var PythonParser=Editor.Parser=function(){function j(d){return RegExp("^(?:"+d.join("|")+")$")}function w(d){if(!d.hasOwnProperty("pythonVersion"))d.pythonVersion=2;if(!d.hasOwnProperty("strictErrors"))d.strictErrors=!0;if(d.pythonVersion!=2&&d.pythonVersion!=3)alert('CodeMirror: Unknown Python Version "'+d.pythonVersion+'", defaulting to Python 2.x.'),d.pythonVersion=2;d.pythonVersion==3?(k=I,p=/[\'\"rbRB]/,q=/[rb]/,x.push("\\-\\>")):(k=J,p=/[\'\"RUru]/,q=/[ru]/);r=d;s=j(K.concat(k.keywords));y=
j(L.concat(k.types));doubleDelimiters=j(x)}var t="py-delimiter",m="py-literal",g="py-error",u="py-operator",z="py-identifier",A="py-string",B="py-bytes",C="py-unicode",D="py-raw",n="normal",o="string",E="+-*/%&|^~<>",M=j(["==","!=","\\<=","\\>=","\\<\\>","\\<\\<","\\>\\>","\\/\\/","\\*\\*"]),F="()[]{}@,:`=;",x=["\\+=","\\-=","\\*=","/=","%=","&=","\\|=","\\^="],N=j(["//=","\\>\\>=","\\<\\<=","\\*\\*="]),O=E+F+"=!",P="=<>*/",G=/[_A-Za-z]/,Q=j(["and","or","not","is","in"]),K=["as","assert","break",
"class","continue","def","del","elif","else","except","finally","for","from","global","if","import","lambda","pass","raise","return","try","while","with","yield"],L=["bool","classmethod","complex","dict","enumerate","float","frozenset","int","list","object","property","reversed","set","slice","staticmethod","str","super","tuple","type"],J={types:["basestring","buffer","file","long","unicode","xrange"],keywords:["exec","print"],version:2},I={types:["bytearray","bytes","filter","map","memoryview","open",
"range","zip"],keywords:["nonlocal"],version:3},k,s,y,p,q,r,H=function(){function d(a,d){function h(b,c){if(!i.style&&!i.content)return b;else typeof b==o&&(b={content:a.get(),style:b});if(i.style||c)b.style=c?c:i.style;if(i.content)b.content=i.content+b.content;i={};return b}var b,e,i={};b=a.next();if(b=="#"){for(;!a.endOfLine();)a.next();return"py-comment"}if(b=="\\"){if(!a.endOfLine()){for(b=!0;!a.endOfLine();)/[\s\u00a0]/.test(a.next())||(b=!1);if(!b)return g}return"py-special"}if(O.indexOf(b)!=
-1||b=="."&&!a.matches(/\d/)){if(P.indexOf(a.peek())!=-1)if(e=b+a.peek(),M.test(e))return a.next(),(b=a.peek())&&N.test(e+b)?(a.next(),t):u;else if(doubleDelimiters.test(e))return a.next(),t;return E.indexOf(b)!=-1||b=="."?u:F.indexOf(b)!=-1?b=="@"&&a.matches(/\w/)?(a.nextWhileMatches(/[\w\d_]/),{style:"py-decorator",content:a.get()}):t:g}if(/\d/.test(b)||b=="."&&a.matches(/\d/)){if(b==="0"&&!a.endOfLine())switch(a.peek()){case "o":case "O":return a.next(),a.nextWhileMatches(/[0-7]/),h(m,g);case "x":case "X":return a.next(),
a.nextWhileMatches(/[0-9A-Fa-f]/),h(m,g);case "b":case "B":return a.next(),a.nextWhileMatches(/[01]/),h(m,g)}a.nextWhileMatches(/\d/);b!="."&&a.peek()=="."&&(a.next(),a.nextWhileMatches(/\d/));if(a.matches(/e/i))if(a.next(),(a.peek()=="+"||a.peek()=="-")&&a.next(),a.matches(/\d/))a.nextWhileMatches(/\d/);else return h(g);a.matches(/j/i)&&a.next();return h(m)}if(p.test(b)){var c=a.peek();e=A;if(q.test(b)&&(c=='"'||c=="'")){switch(b.toLowerCase()){case "b":e=B;break;case "r":e=D;break;case "u":e=C}b=
a.next();return a.peek()!=b?(d(f(e,b)),null):(a.next(),a.peek()==b?(a.next(),d(f(e,b+b+b)),null):e)}else if(b=="'"||b=='"')return a.peek()!=b?(d(f(e,b)),null):(a.next(),a.peek()==b?(a.next(),d(f(e,b+b+b)),null):e)}if(G.test(b)){a.nextWhileMatches(/[\w\d_]/);e=a.get();if(Q.test(e))b=u;else if(s.test(e))b="py-keyword";else if(y.test(e))b="py-type";else{for(b=z;a.peek()==".";)if(a.next(),a.matches(G))a.nextWhileMatches(/[\w\d]/);else{b=g;break}e+=a.get()}return h({style:b,content:e})}/\$\?/.test(b);
return h(g)}function f(a,f){return function(h,b){for(var e=[],i=!1;!i&&!h.endOfLine();){var c=h.next(),g=[];if(c=="\\"){if(h.peek()=="\n")break;c=h.next()}c==f.charAt(0)&&e.push(f);for(var v=0;v<e.length;v++){var l=e[v];if(l.charAt(0)==c)if(l.length==1){b(d);i=!0;break}else g.push(l.slice(1))}e=g}return a}}return function(a,f){return tokenizer(a,f||d)}}();return{make:function(d,f){function a(a,b){b=b?b:n;c={prev:c,endOfScope:!1,startNewScope:!1,level:a,next:null,type:b}}function j(a){if(c.prev)a&&
a?(c=c.prev,c.next=null):(c.prev.next=c,c=c.prev)}function h(a){var b;return function(c,e,d){if(d===null||d===void 0){if(c)for(;a.next;)a=a.next}else if(d===!0)if(e==a.level){if(a.next)return a.next.level}else{for(b=a;b.prev&&b.prev.level>e;)b=b.prev;return b.level}else if(d===!1&&!(e>a.level)&&a.prev){for(b=a;b.prev&&b.prev.level>=e;)b=b.prev;return b.prev?b.prev.level:b.level}return a.level}}s||w({});var f=f||0,b=H(d),e=null,i=f,c={prev:null,endOfScope:!1,startNewScope:!1,level:f,next:null,type:n},
k={next:function(){var d=b.next(),l=d.style,k=d.content;if(e){if(e.content=="def"&&l==z)d.style="py-func";if(e.content=="\n"){var m=c;if(l=="whitespace"&&c.type==n){if(d.value.length<c.level){for(;d.value.length<c.level;)j();if(d.value.length!=c.level){if(c=m,r.strictErrors)d.style=g}else c.next=null}}else if(c.level!==f&&c.type==n){for(;f!==c.level;)j();if(c.level!==f&&(c=m,r.strictErrors))d.style=g}}}switch(l){case A:case B:case D:case C:c.type!==o&&a(c.level+1,o);break;default:c.type===o&&j(!0)}switch(k){case ".":case "@":if(k!==
d.value)d.style=g;break;case ":":if(c.type===n)c.startNewScope=c.level+indentUnit;break;case "(":case "[":case "{":a(i+k.length,"sequence");break;case ")":case "]":case "}":j(!0);break;case "pass":case "return":if(c.type===n)c.endOfScope=!0;break;case "\n":i=f;if(c.endOfScope)c.endOfScope=!1,j();else if(c.startNewScope!==!1)l=c.startNewScope,c.startNewScope=!1,a(l,n);d.indentation=h(c)}k!="\n"&&(i+=d.value.length);return e=d},copy:function(){var a=c,d=b.state;return function(e){b=H(e,d);c=a;return k}}};
return k},electricChars:"",configure:w}}();