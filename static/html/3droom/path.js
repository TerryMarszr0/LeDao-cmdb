//// www.hightopo.com - ht for web
roam = (function(){      
    function easing(t){
        return t;
    }            
    function doTasks(g3d, params, tasks){
        if(tasks.length){
            var task = tasks.splice(0, 1)[0];
            if(task.p2){
                rotate(g3d, params, task, tasks);
            }else{
               walk(g3d, params, task, tasks);
            }
        }
    }
    function walk(g3d, params, task, tasks){
        var y = params.y,
            x0 = task.p0[0],
            z0 = task.p0[1],
            x1 = task.p1[0],
            z1 = task.p1[1],
            dist = ht.Default.getDistance(task.p0, task.p1);           
        g3d.setEye([x0, y, z0]);
        g3d.setCenter([x1, y, z1]);        
        g3d.walk(dist, {
            //frames: Math.ceil((dist / params.speed) * 1000 / 20),
            //interval: 20,
            duration: dist,
            easing: easing,
            finishFunc: function() {
                doTasks(g3d, params, tasks);
            }
        });          
    }
    function rotate(g3d, params, task, tasks){
        var angle1 = Math.atan2(task.p1[1]-task.p0[1], -(task.p1[0]-task.p0[0])),
            angle2 = Math.atan2(task.p2[1]-task.p1[1], -(task.p2[0]-task.p1[0])),
            angle = angle2 - angle1;

        if(angle > Math.PI){
            angle += -Math.PI * 2;
        }
        if(angle < -Math.PI){
            angle += Math.PI * 2;
        }
        g3d.rotate(angle, 0, {
            easing: easing,
            duration: 300,
            finishFunc: function() {
                doTasks(g3d, params, tasks);
            }
        }, true);
    }        
    return function(g3d, params, points){
        var size = points.length;
        if(size < 2){
            return;
        }
        params = params ? params : {};
        params.speed = params.speed || 500;
        params.y = params.y == null ? g3d.getEye()[1] : params.y;
        var i = 2,
            p0 = points[0],
            p1 = points[1],
            p2,
            tasks = [{
                p0: p0,
                p1: p1
            }];
        while(i < size){
            p2 = points[i];
            tasks.push({
                p0: p0,
                p1: p1,
                p2: p2
            }); 
            if(i === size-1 && params.rotateAtLast){
                // last point just for rotate
            }else{
                tasks.push({
                    p0: p1,
                    p1: p2
                });                
            }        
            p0 = p1;
            p1 = p2;
            i++;
        }
        doTasks(g3d, params, tasks);        
    };
})();

