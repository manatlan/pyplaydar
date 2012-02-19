<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<script>
var POOL={};

String.prototype.trim=function(){return this.replace(/^\s\s*/, '').replace(/\s\s*$/, '');};
function log(m) {
    if(console.log) console.log(m);
}

function ajax(url, callback) {
    log("AJAX Q:"+url);
    var x = new XMLHttpRequest();
    x.open('GET', url, true);
    x.onreadystatechange = function() {
        if (x.readyState == 4 && x.status == 200 && callback) {
            log("AJAX R:"+x.responseText);
            callback( eval("("+x.responseText+")" ));
        }
    }
    x.send(null);
}



function search(frm) {
    var a=frm["q_artist"].value.trim();
    var t=frm["q_track"].value.trim();
    if(a && t) {
        var url="/api/?method=resolve&auth=test"; // AUTH !!!!!!!!!!!!!!!
        url+="&artist="+escape(a);
        url+="&track="+escape(t);
        ajax(url,function(data) {
            POOL[data.qid] = {
                artist:     a,
                track:      t,
                isSolved:   false,
                results:    [],
            };
            frm["q_artist"].value="";
            frm["q_track"].value="";
        });
    }
}


// mainloop ;-)
setInterval( function() {
        var hres=document.getElementById("result");
        hres.innerHTML="";

        // fetch/check unsolved query
        for(var qid in POOL) {
            var query=POOL[qid];
            if(!query.isSolved) {
                var url="/api/?method=get_results&auth=test&qid="+qid;
                ajax(url,function(data) {
                    POOL[data.qid].results = data.results;
                    POOL[data.qid].isSolved=data.query.solved;
                });
            }
        }

        // draw results
        for(var qid in POOL) {
            var query=POOL[qid];

            var liste="";
            for(var idr in query.results) {
                var result=query.results[idr];
                liste+="<li><a href='/sid/"+result.sid+"'>"+result.artist+" - "+result.track+" (score:"+result.score+", time:"+result.duration+", src:"+result.source+")</a></li>";
            }
            hres.innerHTML+="<div>SEARCH"+(query.isSolved?"":"'ing")+" : "+query.artist+" - "+query.track+" : "+(liste || "?")+"</div>";
        }
    },1000
);
</script>
</head>
<body>
    <h3>{{msg}}</h3>
    <form onsubmit="search(this); return false">
        Artist:<input name="q_artist" type="text" />
        Track:<input name="q_track" type="text" />
        <input type="submit" value="ok"/>
    </form>

    <div id="result">
    </div>

</body>
</html>
